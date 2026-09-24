# MCIF — Repositório de Conhecimento Colaborativo

Repositório aberto e colaborativo de notas de estudo, resumos técnicos e artefactos de investigação para os estudantes do **Mestrado em Cibersegurança e Informática Forense .

O objetivo deste projeto é disponibilizar à comunidade de estudantes uma base de conhecimento fiável, estruturada, limpa e modular, onde todos possam estudar, consultar e contribuir para expandir a qualidade dos conteúdos ao longo do curso.

---

## 🧭 Como Funciona e Como Navegar no Vault

Este repositório foi construído para ser utilizado nativamente com o [Obsidian](https://obsidian.md/), mas a sua estrutura foi desenhada para ser igualmente legível e navegável diretamente através do GitHub ou de qualquer visualizador de Markdown.

### O Conceito de MOC (*Map of Content*)
Em vez de depender apenas de árvores de pastas profundas e rígidas, a navegação assenta no conceito de **MOC (*Map of Content* / Mapa de Conteúdo)**:
* Uma **MOC** é uma nota-índice ou mapa de navegação que reúne, contextualiza e encadeia ligações (`[[...]]`) para notas atómicas.
* Cada MOC funciona como o plano de estudos ou o índice de um livro, fornecendo a **ordem cronológica e pedagógica** dos tópicos lecionados.

### Arquitetura de Navegação em Níveis

```text
[README.md (GitHub) / Home.md (Obsidian)]  <- Nível 0: Portal Geral do Mestrado
                     │
                     ▼
             [00 <SIGLA>.md]              <- Nível 1: Landing Page / MOC da UC (ex: 00 ASSI.md)
                     │
                     ▼
          [Capítulo X - MOC.md]           <- Nível 2: MOC do Capítulo (ordem sequencial das aulas)
                     │
                     ▼
             [[Notas Atómicas]]           <- Nível 3: Conceitos, Ferramentas e Procedimentos
```

1. **Nível 0 — Portal Geral**:
   * No GitHub, este `README.md` é a porta de entrada.
   * No Obsidian, a nota [[Home]] serve como painel central de controlo do vault.
2. **Nível 1 — Diretoria da UC**:
   * Cada cadeira tem a sua pasta própria identificada pela sigla oficial (ex.: `ASSI/`).
   * No topo de cada pasta reside uma *landing page* com o prefixo `00` (ex.: `ASSI/00 ASSI.md`), garantindo que fica sempre ordenada no início da lista. Esta nota apresenta o docente, o programa da cadeira e os links para os capítulos.
3. **Nível 2 — MOC do Capítulo**:
   * Dentro da pasta de cada capítulo (ex.: `Capítulo 01 - Sistemas Operativos, Serviços e Artefactos/`) existe a nota MOC do capítulo, estruturada em tabelas que espelham a sequência dos diapositivos e sessões letivas.
4. **Nível 3 — Notas Atómicas**:
   * Cada ficheiro foca-se exclusivamente num conceito, ferramenta, serviço ou artefacto forense, contendo comandos exatos, detalhes de baixo nível e hiperligações para as notas relacionadas.

---

## 📚 Unidades Curriculares (1.º Semestre)

| Sigla | Unidade Curricular | Docente | Semestre | Estado |
| :--- | :--- | :--- | :--- | :--- |
| **[[00 ASSI]]** | **Administração Segura de Sistemas Informáticos** | Patrício Domingues | S1 | Concluído (Capítulo 1 — 180 slides) |
| **PARSI** | Políticas e Análise de Risco na Segurança de Informação | Nuno Salvador | S1 | Planeado |
| **AFD1** | Análise Forense Digital I | Miguel Frade | S1 | Planeado |
| **SRC** | Segurança em Redes de Computadores | Luís Frazão | S1 | Planeado |
| **COD1** | Cibersegurança Ofensiva e Defensiva I | Leonel Santos | S1 | Planeado |

---

## 🛠️ Guia de Contribuição para Colegas

Para assegurar que o repositório mantém um nível elevado de rigor académico e consistência estrutural, qualquer contribuição deve observar as seguintes regras:

### 1. Fidelidade Estrita às Fontes (Regra de Ouro)
* **Nunca inventar ou extrapolar**: os apontamentos devem basear-se fielmente nas apresentações de slides, demonstrações laboratoriais e bibliografia oficial da UC.
* Caso pretendas adicionar aprofundamentos, investigações pessoais ou ferramentas alternativas, fá-lo obrigatoriamente sob uma secção designada `## Além da aula`, preservando o núcleo lecionado sem ruído.

### 2. Princípio da Atomicidade
* Desenvolve notas pequenas, focadas e especializadas (*uma ideia por nota*). Notas atómicas são muito mais fáceis de ligar e reutilizar entre diferentes disciplinas (por exemplo, um artefacto do Windows estudado em ASSI pode ser referenciado em AFD1).

### 3. Uso do Modelo Padrão (*Template*)
* Todas as novas notas devem ser criadas a partir do modelo existente em `_templates/Nota de estudo.md`.
* Mantém o cabeçalho YAML preenchido (`mestrado`, `uc`, `sigla_uc`, `capitulo`, `tipo`, `tags`, `fonte_aula`, `atualizado`).

### 4. Convenções Visuais e de Escrita
* **Sem emojis decorativos** no corpo de notas técnicas.
* Callouts (`> [!NOTE]`, `> [!WARNING]`, `> [!IMPORTANT]`, `> [!CAUTION]`) apenas para avisos factuais, armadilhas forenses ou boas práticas de segurança.
* As ligações internas devem usar o formato de wikilink: `[[Nome Exato do Ficheiro]]`.

---

## ⚙️ Configuração Recomendada no Obsidian

Ao clonares este repositório para o teu computador e abrires a pasta no Obsidian:
1. Acede a **Definições (Settings)** $\rightarrow$ **Ficheiros e Ligações (Files and links)**.
2. Em **Local predefinido para novas notas (Default location for new notes)**, seleciona:
   * **"Mesma pasta do ficheiro atual" (Same folder as current file)**.
   * *Porquê?* Isto impede que cliques acidentais em links ainda não criados gerem ficheiros vazios perdidos na raiz do repositório.
3. Em **Formato da ligação de novas notas (New link format)**, seleciona:
   * **"Caminho relativo mais curto" (Shortest path when possible)**.

---

## 🤖 Uso de Agentes de IA (Cursor, Claude, Copilot, etc.)

Se utilizares assistentes ou agentes de IA para criar ou editar notas neste repositório, estão incluídos na raiz os ficheiros de instruções [`.agentrules`](.agentrules) e [`.cursorrules`](.cursorrules). 

Estes ficheiros instruem automaticamente os agentes a:
* Seguir escrupulosamente a taxonomia de pastas e o modelo `_templates/Nota de estudo.md`.
* **Zero alucinações**: proibir a invenção de passos práticos, enunciados ou informações inexistentes nos materiais oficiais fornecidos.
* Preservar o estilo sóbrio (sem emojis) e validar a integridade de todas as ligações internas.
