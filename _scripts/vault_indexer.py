#!/usr/bin/env python3
"""
MCIF Vault Indexer & Link Suggester
===================================
Gera um índice semântico compacto do vault (Markdown + JSON + JSONL),
valida a integridade de wikilinks e cabeçalhos YAML, e sugere conexões
entre Unidades Curriculares (Unlinked Mentions, Tags Partilhadas e
Ligações Assimétricas).

Uso:
  python3 _scripts/vault_indexer.py             # Atualiza _index/ e exibe resumo
  python3 _scripts/vault_indexer.py --check     # Valida integridade (exit 1 se houver erros)
  python3 _scripts/vault_indexer.py --query X   # Pesquisa rápida no índice por termo/tag
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

# Pastas e ficheiros ignorados na indexação de notas de estudo
IGNORE_DIRS = {".git", ".obsidian", ".trash", "_templates", "_index", "_scripts", ".gemini"}
IGNORE_FILES = {"README.md"}

# Tags genéricas ignoradas no cálculo de pontes específicas entre UCs
GENERIC_TAGS = {
    "moc",
    "mcif",
    "assi",
    "afd1",
    "parsi",
    "src",
    "cod1",
    "forense",
    "windows",
    "exercicio",
    "conceito",
    "procedimento",
    "analise",
    "ferramenta",
    "cheatsheet",
    "indice",
}

# Termos demasiado genéricos/curtos para sugerir como Unlinked Mention automático
STOP_ALIASES = {
    "Home",
    "ASSI",
    "AFD1",
    "00 ASSI",
    "00 AFD1",
    "Timestamps",
    "Windows",
    "Registry",
    "Processos Windows",
    "Linha de Comandos",
    "ASCII",
    "Unicode",
    "Services",
    "Bags",
    "Date and Time",
    "Ethical Code",
    "Live Analysis",
    "Post-Mortem Analysis",
}


def parse_yaml_frontmatter(content: str) -> dict[str, Any]:
    """Analisa cabeçalhos YAML simples sem dependências externas (PyYAML)."""
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
    if not match:
        return {}

    yaml_block = match.group(1)
    data: dict[str, Any] = {}
    current_list_key: str | None = None

    for raw_line in yaml_block.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        # Item de lista YAML
        if re.match(r"^\s*-\s+", line) and current_list_key:
            val = re.sub(r"^\s*-\s+", "", line).strip().strip("\"'")
            if val:
                data[current_list_key].append(val)
            continue

        # Par chave: valor
        kv_match = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
        if kv_match:
            key = kv_match.group(1).strip()
            val = kv_match.group(2).strip()
            if val == "" or val == "[]":
                data[key] = []
                current_list_key = key if val == "" else None
            elif val.startswith("[") and val.endswith("]"):
                items = [
                    x.strip().strip("\"'")
                    for x in val[1:-1].split(",")
                    if x.strip().strip("\"'")
                ]
                data[key] = items
                current_list_key = None
            else:
                cleaned_val = val.strip("\"'")
                if cleaned_val.isdigit():
                    data[key] = int(cleaned_val)
                else:
                    data[key] = cleaned_val
                current_list_key = None

    return data


def extract_first_paragraph(content: str) -> str:
    """Extrai o primeiro parágrafo descritivo após o título H1."""
    # Remove YAML frontmatter e blocos de código cercados (ex.: mermaid)
    body = re.sub(r"^---\r?\n.*?\r?\n---\r?\n", "", content, flags=re.DOTALL)
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    lines = body.splitlines()

    paragraph_lines: list[str] = []
    started = False

    for line in lines:
        stripped = line.strip()
        if not started:
            # Ignora títulos, linhas horizontais, tabelas, callouts ou linhas vazias iniciais
            if (
                not stripped
                or stripped.startswith("#")
                or stripped.startswith("---")
                or stripped.startswith(">")
                or stripped.startswith("|")
                or stripped.startswith("```")
            ):
                continue
            started = True
            paragraph_lines.append(stripped)
        else:
            if (
                not stripped
                or stripped.startswith("#")
                or stripped.startswith("---")
                or stripped.startswith(">")
                or stripped.startswith("|")
                or stripped.startswith("*")
                or stripped.startswith("-")
                or stripped.startswith("1.")
            ):
                break
            paragraph_lines.append(stripped)

    text = " ".join(paragraph_lines)
    # Limpa formatação markdown excessiva mantendo legibilidade
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) > 220:
        text = text[:217].rsplit(" ", 1)[0] + "..."
    return text


def extract_wikilinks(content: str) -> list[str]:
    """Extrai o destino de todos os wikilinks [[Destino|Texto]] fora de blocos de código."""
    cleaned = re.sub(r"^---\r?\n.*?\r?\n---\r?\n", "", content, flags=re.DOTALL)
    cleaned = re.sub(r"```.*?```", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"`[^`\n]+`", "", cleaned)

    raw_links = re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", cleaned)
    targets: list[str] = []
    for raw in raw_links:
        target = raw.rstrip("\\").split("#")[0].strip()
        if target and target != "{{title}}":
            targets.append(target)
    return targets


def strip_for_text_search(content: str) -> str:
    """Remove YAML, blocos de código e wikilinks existentes para procurar menções não ligadas."""
    cleaned = re.sub(r"^---\r?\n.*?\r?\n---\r?\n", "", content, flags=re.DOTALL)
    cleaned = re.sub(r"```.*?```", "", cleaned, flags=re.DOTALL)
    cleaned = re.sub(r"\[\[[^\]]+\]\]", " ", cleaned)
    return cleaned


def scan_vault(vault_root: Path) -> dict[str, Any]:
    notes: dict[str, dict[str, Any]] = {}
    alias_to_id: dict[str, str] = {}
    zero_byte_files: list[str] = []
    yaml_warnings: list[dict[str, str]] = []

    for root, dirs, files in os.walk(vault_root):
        dirs[:] = sorted([d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")])
        for file in sorted(files):
            if file.startswith("."):
                continue
            full_path = Path(root) / file
            rel_path = full_path.relative_to(vault_root).as_posix()

            if full_path.stat().st_size == 0:
                zero_byte_files.append(rel_path)

            if not file.endswith(".md") or file in IGNORE_FILES:
                continue

            content = full_path.read_text(encoding="utf-8")
            note_id = full_path.stem
            yaml_data = parse_yaml_frontmatter(content)

            # Determina UC a partir do YAML ou da pasta de topo
            parts = Path(rel_path).parts
            top_folder = parts[0] if len(parts) > 1 else "ROOT"
            sigla_uc = str(yaml_data.get("sigla_uc", top_folder if top_folder != "ROOT" else "GERAL"))

            tags = [str(t).lower() for t in yaml_data.get("tags", []) if t]
            aliases = [str(a) for a in yaml_data.get("aliases", []) if a]
            tipo = str(yaml_data.get("tipo", ""))
            capitulo = yaml_data.get("capitulo")
            bloco = yaml_data.get("bloco")
            title = str(yaml_data.get("title", note_id))

            # Validação de YAML Frontmatter
            if not yaml_data:
                yaml_warnings.append({"path": rel_path, "issue": "Sem cabeçalho YAML frontmatter"})
            else:
                missing_fields = [k for k in ("title", "tipo", "tags") if k not in yaml_data]
                if top_folder in ("ASSI", "AFD1", "PARSI", "SRC", "COD1") and "sigla_uc" not in yaml_data:
                    missing_fields.append("sigla_uc")
                if missing_fields:
                    yaml_warnings.append(
                        {
                            "path": rel_path,
                            "issue": f"Campos YAML em falta: {', '.join(missing_fields)}",
                        }
                    )

            summary = extract_first_paragraph(content)
            raw_links = extract_wikilinks(content)

            notes[note_id] = {
                "id": note_id,
                "title": title,
                "path": rel_path,
                "uc": sigla_uc,
                "capitulo": capitulo,
                "bloco": bloco,
                "tipo": tipo,
                "tags": tags,
                "aliases": aliases,
                "summary": summary,
                "raw_links": raw_links,
                "out_links": [],
                "in_links": [],
                "cross_uc_links": [],
                "_searchable_text": strip_for_text_search(content),
            }

            alias_to_id[note_id.lower()] = note_id
            alias_to_id[title.lower()] = note_id
            for alias in aliases:
                alias_to_id[alias.lower()] = note_id

    # Resolver ligações, detetar broken links e construir grafo
    broken_links: list[dict[str, str]] = []
    for note_id, info in notes.items():
        resolved_out: list[str] = []
        for target in info["raw_links"]:
            target_key = target.lower()
            if target_key in alias_to_id:
                resolved_id = alias_to_id[target_key]
                if resolved_id != note_id and resolved_id not in resolved_out:
                    resolved_out.append(resolved_id)
            else:
                # Verifica se aponta para README
                if target_key == "readme":
                    continue
                broken_links.append(
                    {"source": info["path"], "target": target}
                )
        info["out_links"] = sorted(resolved_out)

    for note_id, info in notes.items():
        for dst_id in info["out_links"]:
            if dst_id in notes:
                if note_id not in notes[dst_id]["in_links"]:
                    notes[dst_id]["in_links"].append(note_id)
                if info["uc"] in ("ASSI", "AFD1", "PARSI", "SRC", "COD1") and notes[dst_id]["uc"] in (
                    "ASSI",
                    "AFD1",
                    "PARSI",
                    "SRC",
                    "COD1",
                ):
                    if info["uc"] != notes[dst_id]["uc"]:
                        info["cross_uc_links"].append(dst_id)

    for info in notes.values():
        info["in_links"].sort()
        info["cross_uc_links"].sort()

    # Notas órfãs (sem in_links e sem out_links ou sem in_links exceto Home)
    orphan_notes = [
        info["path"]
        for nid, info in notes.items()
        if nid != "Home" and len(info["in_links"]) == 0
    ]

    # Sugestões 1: Ligações inter-UCs unidirecionais (A -> B existe, mas B -> A não)
    asymmetric_cross_uc: list[dict[str, str]] = []
    seen_asym: set[tuple[str, str]] = set()
    for nid, info in notes.items():
        if info["tipo"] == "indice":
            continue
        for dst_id in info["cross_uc_links"]:
            dst_info = notes[dst_id]
            if dst_info["tipo"] == "indice":
                continue
            if nid not in dst_info["out_links"] and (nid, dst_id) not in seen_asym:
                seen_asym.add((nid, dst_id))
                asymmetric_cross_uc.append(
                    {
                        "from_id": nid,
                        "from_uc": info["uc"],
                        "to_id": dst_id,
                        "to_uc": dst_info["uc"],
                    }
                )

    # Sugestões 2: Pontes por tags técnicas partilhadas entre UCs diferentes (ainda não ligadas)
    tag_to_notes: dict[str, list[str]] = defaultdict(list)
    for nid, info in notes.items():
        if info["tipo"] == "indice" or info["uc"] == "GERAL":
            continue
        for t in info["tags"]:
            if t not in GENERIC_TAGS:
                tag_to_notes[t].append(nid)

    shared_tag_pairs: dict[tuple[str, str], list[str]] = defaultdict(list)
    for tag, nids in tag_to_notes.items():
        for i in range(len(nids)):
            for j in range(i + 1, len(nids)):
                a, b = sorted((nids[i], nids[j]))
                if notes[a]["uc"] != notes[b]["uc"]:
                    if b not in notes[a]["out_links"] and a not in notes[b]["out_links"]:
                        shared_tag_pairs[(a, b)].append(tag)

    shared_tag_bridges = [
        {
            "note_a": a,
            "uc_a": notes[a]["uc"],
            "note_b": b,
            "uc_b": notes[b]["uc"],
            "shared_tags": sorted(tags_list),
        }
        for (a, b), tags_list in sorted(
            shared_tag_pairs.items(), key=lambda x: (-len(x[1]), x[0][0], x[0][1])
        )
    ]

    # Sugestões 3: Menções não ligadas (Unlinked Mentions) entre UCs diferentes
    candidate_terms: dict[str, list[tuple[str, re.Pattern[str]]]] = defaultdict(list)
    for nid, info in notes.items():
        if info["tipo"] == "indice" or info["uc"] == "GERAL":
            continue
        terms = {nid} | set(info["aliases"])
        for term in terms:
            clean_t = term.strip()
            if len(clean_t) < 5 or clean_t in STOP_ALIASES:
                continue
            pattern = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(clean_t) + r"(?![A-Za-z0-9_])", re.IGNORECASE)
            candidate_terms[nid].append((clean_t, pattern))

    unlinked_mentions: list[dict[str, str]] = []
    for src_id, src_info in notes.items():
        if src_info["tipo"] == "indice" or src_info["uc"] == "GERAL":
            continue
        text = src_info["_searchable_text"]
        for dst_id, patterns in candidate_terms.items():
            dst_info = notes[dst_id]
            if src_info["uc"] == dst_info["uc"]:
                continue
            if dst_id in src_info["out_links"] or src_id in dst_info["out_links"]:
                continue
            for term_str, pat in patterns:
                if pat.search(text):
                    unlinked_mentions.append(
                        {
                            "source_id": src_id,
                            "source_uc": src_info["uc"],
                            "target_id": dst_id,
                            "target_uc": dst_info["uc"],
                            "matched_term": term_str,
                        }
                    )
                    break

    # Limpar campo interno _searchable_text e raw_links
    for info in notes.values():
        info.pop("_searchable_text", None)
        info.pop("raw_links", None)

    # Estatísticas globais
    uc_counts: dict[str, int] = defaultdict(int)
    total_links = 0
    total_cross_uc = 0
    for info in notes.values():
        uc_counts[info["uc"]] += 1
        total_links += len(info["out_links"])
        total_cross_uc += len(info["cross_uc_links"])

    return {
        "generated_at": datetime.date.today().isoformat(),
        "stats": {
            "total_notes": len(notes),
            "notes_by_uc": dict(sorted(uc_counts.items())),
            "total_internal_links": total_links,
            "total_cross_uc_links": total_cross_uc,
            "broken_links_count": len(broken_links),
            "orphan_notes_count": len(orphan_notes),
            "yaml_warnings_count": len(yaml_warnings),
            "zero_byte_files_count": len(zero_byte_files),
        },
        "health": {
            "broken_links": broken_links,
            "orphan_notes": orphan_notes,
            "yaml_warnings": yaml_warnings,
            "zero_byte_files": zero_byte_files,
        },
        "suggestions": {
            "unlinked_mentions": unlinked_mentions[:40],
            "shared_tag_bridges": shared_tag_bridges[:40],
            "asymmetric_cross_uc_links": asymmetric_cross_uc[:40],
        },
        "notes": [notes[k] for k in sorted(notes.keys(), key=lambda x: (notes[x]["uc"], notes[x]["path"]))],
    }


def render_markdown_index(index_data: dict[str, Any]) -> str:
    stats = index_data["stats"]
    health = index_data["health"]
    suggestions = index_data["suggestions"]
    notes: list[dict[str, Any]] = index_data["notes"]

    lines: list[str] = [
        "---",
        "title: Índice Semântico e Mapa de Contexto do Vault",
        "tipo: indice",
        "tags:",
        "  - indice-sistema",
        f"atualizado: {index_data['generated_at']}",
        "---",
        "",
        "# Índice Semântico e Mapa de Contexto do Vault (MCIF)",
        "",
        "> [!NOTE] Ficheiro Gerado Automaticamente (`_scripts/vault_indexer.py`)",
        "> Este catálogo fornece a visão global e compacta de todas as notas, metadados, resumos e ligações inter-UCs do repositório para consulta rápida por estudantes e agentes de IA.",
        "> **Nota de Design**: As referências a notas neste ficheiro utilizam formatação de código (`` `Nome da Nota` ``) em vez de wikilinks para **não poluir o Graph View do Obsidian** com um super-nó artificial.",
        "",
        "---",
        "",
        "## 1. Estatísticas e Saúde do Vault",
        "",
        "| Métrica | Valor |",
        "| :--- | :---: |",
        f"| **Total de Notas Mapeadas** | `{stats['total_notes']}` |",
    ]

    for uc, count in stats["notes_by_uc"].items():
        lines.append(f"| Notas em **{uc}** | `{count}` |")

    lines.extend(
        [
            f"| **Total de Ligações Internas (Wikilinks Únicos)** | `{stats['total_internal_links']}` |",
            f"| **Ligações Cruzadas entre UCs Diferentes** | `{stats['total_cross_uc_links']}` |",
            f"| **Links Quebrados (*Broken Links*)** | `{stats['broken_links_count']}` |",
            f"| **Notas Órfãs (Sem Ligações de Entrada)** | `{stats['orphan_notes_count']}` |",
            f"| **Avisos de YAML Frontmatter** | `{stats['yaml_warnings_count']}` |",
            f"| **Ficheiros Vazios (0 bytes)** | `{stats['zero_byte_files_count']}` |",
            "",
        ]
    )

    if (
        health["broken_links"]
        or health["orphan_notes"]
        or health["yaml_warnings"]
        or health["zero_byte_files"]
    ):
        lines.append("### Alertas de Integridade Detetados")
        for b in health["broken_links"]:
            lines.append(f"* **Link Quebrado**: `{b['source']}` aponta para `{b['target']}`")
        for o in health["orphan_notes"]:
            lines.append(f"* **Nota Órfã**: `{o}`")
        for w in health["yaml_warnings"]:
            lines.append(f"* **Aviso YAML**: `{w['path']}` — {w['issue']}")
        for z in health["zero_byte_files"]:
            lines.append(f"* **Ficheiro 0 Bytes**: `{z}`")
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## 2. Catálogo Compacto de Notas por Unidade Curricular",
            "",
        ]
    )

    by_uc: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for n in notes:
        by_uc[n["uc"]].append(n)

    for uc in sorted(by_uc.keys()):
        uc_notes = sorted(
            by_uc[uc],
            key=lambda x: (
                x["capitulo"] if isinstance(x["capitulo"], int) else 0,
                x["bloco"] if isinstance(x["bloco"], int) else 0,
                x["path"],
            ),
        )
        lines.append(f"### Unidade Curricular: `{uc}` ({len(uc_notes)} notas)")
        lines.append("")
        lines.append("| Cap.Bloco | Nota (`ID` de Wikilink) | Tipo | Tags & Aliases | Resumo Central e Pontes Inter-UCs |")
        lines.append("| :---: | :--- | :---: | :--- | :--- |")
        for n in uc_notes:
            cap_str = str(n["capitulo"]) if n["capitulo"] is not None else "-"
            bloco_str = f".{n['bloco']}" if n["bloco"] is not None else ""
            loc = f"`{cap_str}{bloco_str}`"
            tags_str = ", ".join(f"`#{t}`" for t in n["tags"][:6])
            aliases_str = ", ".join(f"*{a}*" for a in n["aliases"][:4])
            meta_col = tags_str + (f"<br/>Aliases: {aliases_str}" if aliases_str else "")
            cross_str = ""
            if n["cross_uc_links"]:
                cross_list = ", ".join(f"`{c}`" for c in n["cross_uc_links"][:5])
                if len(n["cross_uc_links"]) > 5:
                    cross_list += f" (+{len(n['cross_uc_links']) - 5})"
                cross_str = f"<br/>**Pontes Inter-UCs ({len(n['cross_uc_links'])})**: {cross_list}"
            summary_col = (n["summary"] or "—").replace("|", "\\|") + cross_str
            lines.append(
                f"| {loc} | **`{n['id']}`**<br/><small>`{n['path']}`</small> | `{n['tipo']}` | {meta_col} | {summary_col} |"
            )
        lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## 3. Motor de Sugestões de Novas Conexões Inter-UCs",
            "",
            "### 3.1. Menções de Conceitos/Aliases Ainda Não Ligadas (*Unlinked Mentions*)",
            "",
        ]
    )

    if suggestions["unlinked_mentions"]:
        lines.append("| Nota de Origem | UC | Conceito / Alias Detetado no Texto | Nota de Destino Sugerida | UC |")
        lines.append("| :--- | :---: | :---: | :--- | :---: |")
        for m in suggestions["unlinked_mentions"][:25]:
            lines.append(
                f"| `{m['source_id']}` | `{m['source_uc']}` | `{m['matched_term']}` | `{m['target_id']}` | `{m['target_uc']}` |"
            )
    else:
        lines.append("*Nenhuma menção óbvia não ligada detetada entre UCs.*")
    lines.append("")

    lines.extend(
        [
            "### 3.2. Pares de Notas com Tags Técnicas Partilhadas (Sem Ligação Direta)",
            "",
        ]
    )
    if suggestions["shared_tag_bridges"]:
        lines.append("| Nota A | UC | Nota B | UC | Tags Técnicas em Comum |")
        lines.append("| :--- | :---: | :--- | :---: | :--- |")
        for s in suggestions["shared_tag_bridges"][:25]:
            t_str = ", ".join(f"`#{t}`" for t in s["shared_tags"])
            lines.append(
                f"| `{s['note_a']}` | `{s['uc_a']}` | `{s['note_b']}` | `{s['uc_b']}` | {t_str} |"
            )
    else:
        lines.append("*Todas as notas com tags técnicas específicas partilhadas já se encontram ligadas.*")
    lines.append("")

    lines.extend(
        [
            "### 3.3. Ligações Inter-UCs Unidirecionais (Oportunidades de Reciprocidade)",
            "",
        ]
    )
    if suggestions["asymmetric_cross_uc_links"]:
        lines.append("| Nota que Liga (`A -> B`) | UC | Nota que Ainda Não Retribui (`B -x-> A`) | UC |")
        lines.append("| :--- | :---: | :--- | :---: |")
        for a in suggestions["asymmetric_cross_uc_links"][:25]:
            lines.append(
                f"| `{a['from_id']}` | `{a['from_uc']}` | `{a['to_id']}` | `{a['to_uc']}` |"
            )
    else:
        lines.append("*Todas as ligações inter-UCs entre notas atómicas são totalmente bidirecionais (`A <-> B`)!*")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="MCIF Vault Indexer & Link Suggester")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Executa apenas a validação de integridade (retorna código != 0 em caso de erro).",
    )
    parser.add_argument(
        "--query",
        type=str,
        default=None,
        help="Pesquisa rápida no índice por palavra-chave, título, alias ou tag.",
    )
    args = parser.parse_args()

    vault_root = Path(__file__).resolve().parent.parent
    index_data = scan_vault(vault_root)
    stats = index_data["stats"]

    if args.query:
        q = args.query.lower()
        matches = [
            n
            for n in index_data["notes"]
            if q in n["id"].lower()
            or q in n["title"].lower()
            or q in n["summary"].lower()
            or any(q in t.lower() for t in n["tags"])
            or any(q in a.lower() for a in n["aliases"])
        ]
        print(f"Resultados para '{args.query}': {len(matches)} nota(s)")
        for m in matches:
            print(f"\n- [{m['uc']}] [[{m['id']}]] ({m['path']})")
            print(f"  Tags: {', '.join(m['tags'])} | Aliases: {', '.join(m['aliases'])}")
            print(f"  Resumo: {m['summary']}")
            if m["cross_uc_links"]:
                print(f"  Pontes Inter-UCs: {', '.join(m['cross_uc_links'])}")
        return 0

    index_dir = vault_root / "_index"
    index_dir.mkdir(exist_ok=True)

    json_path = index_dir / "vault_index.json"
    jsonl_path = index_dir / "vault_catalog.jsonl"
    md_path = index_dir / "Vault-Index.md"

    json_path.write_text(
        json.dumps(index_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    with jsonl_path.open("w", encoding="utf-8") as fp:
        for n in index_data["notes"]:
            compact = {
                "id": n["id"],
                "uc": n["uc"],
                "cap": n["capitulo"],
                "bloco": n["bloco"],
                "tipo": n["tipo"],
                "tags": n["tags"],
                "aliases": n["aliases"],
                "summary": n["summary"],
                "cross_uc_links": n["cross_uc_links"],
                "path": n["path"],
            }
            fp.write(json.dumps(compact, ensure_ascii=False) + "\n")

    md_path.write_text(render_markdown_index(index_data), encoding="utf-8")

    print("=== MCIF Vault Indexer ===")
    print(f"Notas indexadas       : {stats['total_notes']} {stats['notes_by_uc']}")
    print(f"Ligações internas     : {stats['total_internal_links']}")
    print(f"Ligações inter-UCs    : {stats['total_cross_uc_links']}")
    print(f"Links quebrados       : {stats['broken_links_count']}")
    print(f"Notas órfãs           : {stats['orphan_notes_count']}")
    print(f"Avisos YAML           : {stats['yaml_warnings_count']}")
    print(f"Ficheiros 0 bytes     : {stats['zero_byte_files_count']}")
    print(f"Índices atualizados   : _index/Vault-Index.md, _index/vault_index.json, _index/vault_catalog.jsonl")

    if args.check and (
        stats["broken_links_count"] > 0 or stats["zero_byte_files_count"] > 0
    ):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
