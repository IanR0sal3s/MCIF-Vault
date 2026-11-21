---
title: Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 5
tipo: conceito
tags:
  - assi
  - windows
  - registry
  - wow64
  - pe
  - arquitetura
  - forense
aliases:
  - WOW6432Node
  - Registry Redirection
  - PE Architecture Identification
  - 32 vs 64 bits
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
fontes:
  - "https://exiftool.org/"
  - "https://mark0.net/soft-trid-e.html"
atualizado: 2026-11-21
---

# Arquitetura 32 vs 64 bits no Registry (`WOW6432Node`) e Executáveis PE

Num Windows de 64 bits, o subsistema **WOW64** (*Windows 32-bit on Windows 64-bit*) separa as chaves de aplicações de 32 bits e 64 bits para evitar colisões. Em forense, esta separação afeta tanto onde procurar persistência como a escolha da arquitetura das próprias ferramentas de triagem.

## 1. O Nó `WOW6432Node` e a Cegueira de Ferramentas 32 bits

* **Chaves 64 bits (nativas)**: `HKEY_LOCAL_MACHINE\Software\...`
* **Chaves 32 bits (redirecionadas)**: `HKEY_LOCAL_MACHINE\Software\WOW6432Node\...`

| Ferramenta em Windows 64 bits | Acesso a `WOW6432Node` (32 bits) | Acesso ao ramo nativo (64 bits) |
| :--- | :---: | :---: |
| **Software de 32 bits** | Sim (redirecionado automaticamente) | **Não** (cego ao espaço de 64 bits) |
| **Software de 64 bits** | Sim (sem limitações) | **Sim** |

> [!WARNING] Regra Prática em Sistemas 64 bits
> Em triagem *live*, usar sempre **ferramentas forenses de 64 bits** (uma ferramenta de 32 bits não vê o espaço nativo de 64 bits). Em análise *offline*, auditar **ambos** os ramos (`Software\...\Run` e `Software\WOW6432Node\...\Run`).

---

## 2. Identificar se um `.exe` é 32 bits, 64 bits ou ARM64

### A) Cabeçalho PE (Editor Hexadecimal)
Os executáveis Windows começam com `MZ` (`4D 5A`), apontam (offset `0x3C`) para a assinatura **`PE\0\0` (`50 45 00 00`)**, e os **2 bytes seguintes** (em [[Endianness e Ordem de Armazenamento|Little-Endian]]) identificam a arquitetura:

| Arquitetura | Bytes após `PE\0\0` (Little-Endian) | Valor Nominal | Tipo PE (`exiftool`) |
| :--- | :---: | :---: | :---: |
| **x86 (32 bits)** | **`4C 01`** | `0x014C` | `PE32` (`Win32 EXE`) |
| **x64 / AMD64 (64 bits)** | **`64 86`** | `0x8664` | `PE32+` (`Win64 EXE`) |
| **ARM64** | **`64 AA`** | `0xAA64` | `PE32+` (`ARM64`) |

### B) Ferramentas CLI: `exiftool` e `trid`
* **`exiftool`**: extrai metadados do cabeçalho PE (`File Type`, `Machine Type` — ex.: `x86` / `AMD64` / `ARM64 little endian`, `PE Type` — `PE32` vs `PE32+`).
* **`trid`**: identifica o tipo real de ficheiro por assinaturas binárias (>18 000 definições), revelando compilador, linguagem ou *packers* (ex.: UPX) mesmo com extensão alterada.

---

## Perguntas de revisão

1. **Qual a limitação crítica de executar uma ferramenta forense de 32 bits num Windows de 64 bits?**

> [!success]- Ver Resposta
> O subsistema WOW64 redireciona os seus pedidos a `HKLM\Software` para `WOW6432Node`, deixando a ferramenta **cega ao espaço de Registry nativo de 64 bits**. Já software de 64 bits acede sem limitações a ambos.

2. **Que bytes imediatamente após `50 45 00 00` (`PE\0\0`) distinguem um executável x86 (32 bits), x64 (64 bits) e ARM64?**

> [!success]- Ver Resposta
> Em Little-Endian: **`4C 01`** (x86 / 32 bits), **`64 86`** (x64 / 64 bits) e **`64 AA`** (ARM64).

3. **Como se complementam o `exiftool` e o `trid` na análise de um binário suspeito?**

> [!success]- Ver Resposta
> O `exiftool` lê os metadados estruturais do cabeçalho (`Win32`/`Win64`, `PE32`/`PE32+`, `Machine Type`), enquanto o `trid` identifica heuristicamente o tipo de ficheiro, compilador ou empacotador a partir de mais de 18 000 assinaturas binárias.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Ferramentas de Análise e Extração do Registry]] | `mesmo bloco` |
| **Seguinte** | [[Ficha Prática e Questionário - Windows Registry e Artefactos Forenses]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 05` |

### Conceitos Relacionados

* [[Estrutura e Hives do Windows Registry]] · `mesmo bloco`
* [[Registry em Aplicações Modernas (MSIX e Helium)]] · `Bloco 06`
* [[Endianness e Ordem de Armazenamento]] · `AFD1 · Cap. 3`
* [[Sistemas de Numeração e Conversão entre Bases]] · `AFD1 · Cap. 3`
