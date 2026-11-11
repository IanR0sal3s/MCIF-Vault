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
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://exiftool.org/"
  - "https://mark0.net/soft-trid-e.html"
atualizado: 2026-09-23
---

# Arquitetura 32 vs 64 bits no Registry e Executáveis (WOW6432Node)

Subsistema de emulação **WOW64** (*Windows 32-bit on Windows 64-bit*), redirecionamento de chaves do Registry para o nó `WOW6432Node` e identificação forense da arquitetura de binários PE (`x86`, `x64`, `ARM64`).

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Num sistema Windows de 64 bits, aplicações legadas de 32 bits precisam de aceder a caminhos como `HKLM\Software` sem colidir nem corromper parâmetros ou DLLs de programas nativos de 64 bits com o mesmo nome. O subsistema **WOW64** interceta chamadas de processos de 32 bits e redireciona-as de forma transparente para a subchave isolada `WOW6432Node`.
> * **Porque importa (Forense)**: Primeiro, *malware* de 32 bits instala a sua persistência dentro de `WOW6432Node` (ex.: `HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run`). Segundo, **ferramentas forenses de 32 bits** executadas num sistema de 64 bits sofrem redirecionamento automático e ficam **cegas às chaves nativas de 64 bits**. Além disso, identificar a arquitetura exata de um executável PE no cabeçalho hexadecimal é essencial para escolher o desassemblador/depurador correto.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Cegueira de Ferramentas 32 bits**: Uma ferramenta de triagem de 32 bits a correr em Windows 64 bits vê o seu pedido a `HKLM\Software` desviado para `WOW6432Node` (exceto se usar explicitamente a flag `KEY_WOW64_64KEY`). Em sistemas de 64 bits, usar sempre ferramentas nativas de 64 bits.
>   * **Magic Bytes no Cabeçalho PE (Little-Endian)**: Logo após a assinatura `PE\0\0` (`50 45 00 00`), os 2 bytes do campo `Machine` distinguem a arquitetura: `4C 01` (**x86 / 32 bits**), `64 86` (**x64 / AMD64**) e `64 AA` (**ARM64**).

---

## O Nó `WOW6432Node` e o Redirecionamento do Registry

Para evitar conflitos entre bibliotecas e configurações de arquiteturas distintas, o Windows de 64 bits divide o Registry em duas visões lógicas:

* **Chaves de 64 bits (Nativas)**: residem diretamente na raiz convencional, como `HKEY_LOCAL_MACHINE\Software`.
* **Chaves de 32 bits (Redirecionadas)**: residem debaixo do nó:

```text
HKEY_LOCAL_MACHINE\Software\WOW6432Node
```

(Existe mapeamento análogo sob `HKCU\Software\Classes\WOW6432Node` e `HKLM\Software\Classes\WOW6432Node` para registo de componentes COM e classes de 32 bits).

### Impacto na Triagem Forense (*Live Analysis*)

| Arquitetura da Ferramenta Forense (em SO 64 bits) | Quando pede `HKLM\Software`, o que lê na realidade? | Visibilidade sobre `WOW6432Node` (32 bits) | Visibilidade sobre o ramo nativo 64 bits |
| :--- | :--- | :---: | :---: |
| **Compilada em 32 bits** (sem flag `KEY_WOW64_64KEY`) | É redirecionada pelo WOW64 para `HKLM\Software\WOW6432Node` | Total (transparente) | **Nenhuma (Cega ao espaço de 64 bits)** |
| **Compilada em 64 bits** (Nativa) | Lê diretamente o ramo nativo `HKLM\Software` | Total (acedendo explicitamente a `\WOW6432Node`) | **Total** |

> [!WARNING] Regra Pericial de Ouro em Sistemas de 64 bits
> Em triagem *live* em máquinas de 64 bits, o perito deve utilizar sempre versões nativas de **64 bits** das ferramentas de extração e análise, sob pena de produzir falsos negativos por omissão de todas as chaves nativas de 64 bits. No exame *offline* de hives, o perito deve inspecionar **ambos** os ramos (`Software\Microsoft\Windows\CurrentVersion\Run` e `Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run`).

---

## Identificação da Arquitetura de Ficheiros Executáveis (PE)

Determinar se um binário recolhido é de 32 bits, 64 bits ou ARM64 é indispensável para selecionar o ambiente de engenharia reversa, *sandbox* ou desassemblagem adequado.

### 1. Análise Hexadecimal do Cabeçalho PE (`IMAGE_FILE_HEADER`)

Todo o executável Windows respeita a especificação *Portable Executable* (PE):

1. O ficheiro inicia no offset `0x00` com o cabeçalho DOS (`MZ` em ASCII, `4D 5A` em hexadecimal).
2. No offset `0x3C` (`e_lfanew`), reside um ponteiro de 4 bytes Little-Endian que indica o offset onde começa a assinatura PE.
3. A assinatura do cabeçalho PE consiste em 4 bytes: `PE\0\0` (`50 45 00 00` em hex).
4. Os **dois bytes imediatamente seguintes** (offset `+4` após o início de `50 45 00 00`) formam o campo `Machine` da estrutura `IMAGE_FILE_HEADER` (armazenado em [[Endianness e Ordem de Armazenamento|Little-Endian]]):

| Arquitetura do Binário | Sequência Completa (Hex) | Campo `Machine` (Hex Little-Endian) | Valor Nominal (Big-Endian) | Assinatura ASCII Visível | Constante Oficial PE (`IMAGE_FILE_MACHINE_`) | Tipo PE (`exiftool`) |
| :--- | :---: | :---: | :---: | :---: | :--- | :---: |
| **x86 (32 bits)** | `50 45 00 00 4C 01` | **`4C 01`** | `0x014C` | `PE..L.` | `IMAGE_FILE_MACHINE_I386` | `PE32` (`Win32 EXE`) |
| **x64 / AMD64 (64 bits)** | `50 45 00 00 64 86` | **`64 86`** | `0x8664` | `PE..d†` | `IMAGE_FILE_MACHINE_AMD64` | `PE32+` (`Win64 EXE`) |
| **ARM64 (Little-Endian)** | `50 45 00 00 64 AA` | **`64 AA`** | `0xAA64` | `PE..dª` (`PE....`) | `IMAGE_FILE_MACHINE_ARM64` | `PE32+` (ARM64) |

---

## Anatomia das Ferramentas de Identificação (`exiftool` e `trid`)

Para evitar a inspeção manual em editor hexadecimal, utilizam-se duas ferramentas de análise estática:

### 1. Ferramenta `exiftool` (Leitura de Metadados do Cabeçalho PE)
Lê e formata os campos estruturais do cabeçalho PE sem carregar nem executar o binário:

```cmd
exiftool.exe trid.exe
```

* **Campos-chave a inspecionar no output**:
  * `File Type`: distingue `Win32 EXE` (32 bits) de `Win64 EXE` (64 bits).
  * `Machine Type`: traduz o código hexadecimal `Machine` para texto legível (`Intel 386 or later`, `AMD AMD64` ou `ARM64 little endian`).
  * `PE Type`: distingue o formato de cabeçalho opcional **`PE32`** (32 bits) de **`PE32+`** (64 bits).

### 2. Ferramenta `trid` (Identificação Heurística por Assinaturas Binárias)
Utilitário de linha de comandos que compara padrões binários do ficheiro contra uma base de dados com mais de 18.000 definições:

```cmd
trid.exe ficheiro_analisado.exe
```

* **Valor Forense**: Calcula as probabilidades percentuais do tipo real do ficheiro (mesmo que a extensão tenha sido alterada), identificando a linguagem de programação, o compilador utilizado (ex.: FreeBASIC, MS Visual C++, Borland Delphi, .NET) ou a presença de compressores/ofuscadores de código (*packers* como UPX).

---

## Perguntas de revisão

1. **Qual o problema pericial que ocorre se um investigador executar uma ferramenta forense compilada em 32 bits numa máquina suspeita com Windows 11 de 64 bits para auditar a chave `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`?**

> [!success]- Ver Resposta
> O subsistema **WOW64** interceta a chamada da ferramenta de 32 bits e redireciona-a de forma transparente para `HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run`. A menos que a ferramenta utilize explicitamente a flag de API `KEY_WOW64_64KEY`, ficará completamente cega às entradas nativas de 64 bits, falhando a deteção de *malware* de 64 bits ali configurado.

2. **Ao inspecionar um ficheiro executável num editor hexadecimal, encontra-se a assinatura `50 45 00 00` (`PE\0\0`) seguida imediatamente pelos bytes `64 86`. Qual é a arquitetura deste executável e por que razão os bytes surgem nesta ordem?**

> [!success]- Ver Resposta
> Trata-se de um executável de **64 bits (x64 / AMD64)**, correspondente à constante `IMAGE_FILE_MACHINE_AMD64` (`0x8664`). Os bytes surgem na ordem `64 86` porque os campos do cabeçalho PE são armazenados em formato **Little-Endian** (o byte menos significativo `0x64` é gravado primeiro). Se fosse de 32 bits (`x86`), os bytes seriam `4C 01` (`0x014C`), e se fosse `ARM64`, seriam `64 AA` (`0xAA64`).

3. **No output da ferramenta `exiftool`, qual a diferença entre os valores `PE32` e `PE32+` no campo `PE Type`?**

> [!success]- Ver Resposta
> `PE32` identifica um executável Windows com cabeçalho opcional de **32 bits**, enquanto `PE32+` identifica um executável com cabeçalho opcional de **64 bits** (onde os campos de endereçamento virtual foram alargados para 64 bits).

4. **Que informação adicional fornece a ferramenta `trid.exe` que complementa os metadados extraídos pelo `exiftool.exe`?**

> [!success]- Ver Resposta
> Enquanto o `exiftool` lê os campos estáticos declarados na estrutura do cabeçalho PE, o `trid` realiza uma análise heurística de padrões binários que permite identificar o **compilador**, a **linguagem de programação** (ex.: Visual C++, Delphi, FreeBASIC, .NET) e se o executável foi comprimido ou ofuscado com um *packer* (como o UPX).

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Registry em Aplicações Modernas (MSIX e Helium)]]
- [[Endianness e Ordem de Armazenamento]]
- [[Sistemas de Numeração e Conversão entre Bases]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
