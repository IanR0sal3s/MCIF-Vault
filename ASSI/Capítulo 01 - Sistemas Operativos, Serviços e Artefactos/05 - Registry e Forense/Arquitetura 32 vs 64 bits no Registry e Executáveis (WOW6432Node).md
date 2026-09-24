---
title: Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
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
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://exiftool.org/"
  - "https://mark0.net/soft-trid-e.html"
atualizado: 2026-09-23
---

# Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)

Em sistemas operativos Windows de 64 bits, a compatibilidade com programas legados de 32 bits é assegurada pelo subsistema **WOW64** (*Windows 32-bit on Windows 64-bit*). Esta emulação tem impacto direto na estrutura do Registry e exige métodos rigorosos para identificação da arquitetura de binários suspeitos.

## O Nó `WOW6432Node` no Registry

Aplicações de 32 bits não operam de forma idêntica em 64 bits e requerem configurações e caminhos adaptados. Para evitar conflitos entre bibliotecas e chaves com o mesmo nome, o Windows divide o Registry em duas visões:
* **Chaves de 64 bits (Nativas)**: residem diretamente na raiz convencional, como `HKEY_LOCAL_MACHINE\Software`.
* **Chaves de 32 bits (Redirecionadas)**: residem debaixo do nó:

```text
HKEY_LOCAL_MACHINE\Software\WOW6432Node
```

(Existe mapeamento análogo sob `HKCU\Software\Classes\WOW6432Node` para registo de componentes COM de 32 bits).

### Limitação Pericial Crítica

> [!WARNING] Risco em Ferramentas Forenses de 32 bits
> * **Software forense compilado em 32 bits** executado num sistema Windows de 64 bits é sujeito ao redirecionamento automático do WOW64: as suas chamadas a `HKLM\Software` são redirecionadas transparentemente para `WOW6432Node`, ficando **cego ao espaço de 64 bits** (a menos que a ferramenta use especificamente a flag de API `KEY_WOW64_64KEY`).
> * **Software forense compilado em 64 bits** acede sem qualquer limitação tanto ao espaço nativo de 64 bits como ao nó `WOW6432Node`.
> * *Regra pericial*: em triagem *live* em máquinas de 64 bits, deve-se usar sempre ferramentas nativas de 64 bits.

## Identificação da Arquitetura de Ficheiros Executáveis (PE)

Determinar se um binário é de 32 bits, 64 bits ou ARM é indispensável para selecionar o ambiente de desassemblagem/sandbox correto.

### 1. Análise Hexadecimal do Cabeçalho PE

Todo o executável Windows segue a especificação *Portable Executable* (PE). Após o cabeçalho DOS (`MZ` / `4D 5A`) e a transição indicada no offset `0x3C`, encontra-se a assinatura do cabeçalho PE (`PE\0\0` ou `50 45 00 00` em hex).

Os dois bytes imediatamente seguintes (offset `+4` após a assinatura PE) definem o campo `Machine` da estrutura `IMAGE_FILE_HEADER`:

| Arquitetura | Assinatura ASCII | Magic Bytes (Hex) | Especificação PE |
| :--- | :---: | :---: | :--- |
| **x86 (32 bits)** | `PE..L.` | `4C 01` | `IMAGE_FILE_MACHINE_I386` |
| **x64 / AMD64 (64 bits)** | `PE..d†` | `64 86` | `IMAGE_FILE_MACHINE_AMD64` |
| **ARM64 (Little-Endian)** | `PE....` | `64 AA` | `IMAGE_FILE_MACHINE_ARM64` (valor nominal `AA64`) |

### 2. Ferramenta `exiftool`
O `exiftool` efetua a leitura rápida dos metadados do cabeçalho PE sem necessidade de carregar o binário num depurador:

```cmd
exiftool.exe trid.exe
```

Campos chave inspecionados:
* `File Type`: `Win32 EXE` vs `Win64 EXE`
* `Machine Type`: `Intel 386 or later` vs `AMD AMD64` vs `ARM64 little endian`
* `PE Type`: `PE32` (32 bits) vs `PE32+` (64 bits)

### 3. Ferramenta `trid`
Utilitário de análise heurística por assinaturas binárias (mais de 18.000 definições suportadas). Identifica a probabilidade de tipo de ficheiro, linguagem de programação e compilador empregue:

```cmd
trid.exe ficheiro_analisado.exe
```

Permite distinguir binários desenvolvidos em FreeBASIC, MS Visual C++, Delphi, compiladores .NET ou executáveis empacotados (*packers*).

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Registry em Aplicações Modernas (MSIX e Helium)]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
