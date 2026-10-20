---
title: Artefacto Forense do Bloco de Notas (Notepad Windows 11)
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 15
fonte_aula: Artefactos Windows OS (Prof. Patrício Domingues)
tags:
  - assi
  - windows
  - notepad
  - tabstate
  - windowstate
  - uleb128
  - forense
aliases:
  - Bloco de Notas Windows 11
  - Notepad Forense
  - TabState
  - WindowState
  - Ficha 10 Windows Notepad
atualizado: 2026-10-07
---

# Artefacto Forense do Bloco de Notas (Notepad Windows 11)

Na modernização do Windows 11, o clássico Bloco de Notas Win32 foi substituído por uma aplicação moderna empacotada em arquitetura UWP / MSIX (`Microsoft.WindowsNotepad`).

Entre as novas funcionalidades, destaca-se o suporte a múltiplos **separadores (*tabs*)** e um mecanismo avançado de **tolerância a falhas e restauro de sessão**: o Bloco de Notas grava continuamente em segundo plano o conteúdo dos separadores abertos, **incluindo texto nunca gravado pelo utilizador (*unsaved text*)**, sobrevivendo a encerramentos forçados, falhas de energia e reinícios do sistema (*reboots*).

Em investigações forenses, este artefacto permite recuperar rascunhos, credenciais copiadas temporariamente, chaves privadas ou notas voláteis que o suspeito acreditava nunca terem sido escritas no disco.

---

## 1. Localização Física no Sistema de Ficheiros

Os ficheiros de estado do Bloco de Notas residem no contentor privado do pacote UWP do utilizador:

```text
%LOCALAPPDATA%\Packages\Microsoft.WindowsNotepad_8wekyb3d8bbwe\LocalState\
```
*(Caminho expandido: `C:\Users\<User>\AppData\Local\Packages\Microsoft.WindowsNotepad_8wekyb3d8bbwe\LocalState\`)*

```mermaid
flowchart TD
    LocalState["LocalState\\ (Microsoft.WindowsNotepad_8wekyb3d8bbwe)"] --> TabState["<b>TabState\\</b><br/>Um ficheiro <code>{GUID}.bin</code> por cada separador aberto<br/>(Conteúdo do documento e texto não guardado)"]
    LocalState --> WindowState["<b>WindowState\\</b><br/>Um ficheiro <code>{GUID}.bin</code> por janela aberta<br/>(Posicionamento, dimensões, disposição no ecrã)"]
    LocalState --> RestartMgr["<b>RestartManager\\</b><br/>Ficheiros de controlo e recuperação de sessões anómalas"]
```

---

## 2. Anatomia Binária dos Ficheiros `TabState` (`.bin`)

Cada separador ativo ou recuperável é representado por um ficheiro nomeado pelo seu GUID exclusivo (ex.: `04b74c4a-5e1b-46ec-9a90-0eb68371af75.bin`).

O ficheiro segue uma especificação binária proprietária rigorosa (conforme mapeado na biblioteca *Notepad-State-Library*), cuja estrutura varia consoante o separador corresponda a um **ficheiro gravado em disco (`TypeFlag = 1`)** ou a um **separador de rascunho não gravado (`TypeFlag = 0`)**:

```text
Offset (h)  00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F  Decoded Text
00000000    4E 50 00 01 6F 43 00 3A 00 5C 00 55 00 73 00 65  NP..oC.:.\.U.s.e
            [Magic]  [T][L][Caminho UTF-16LE: C:\Use...]
```
*(No exemplo acima, `0x01` no offset `0x03` indica separador gravado em disco, `0x6F` indica um caminho de 111 carateres em `uLEB128`, seguido de `C:\Users\patri\OneDrive...` em UTF-16LE).*

### Estrutura de Campos: Separador Gravado (`TypeFlag = 1`) vs. Não Gravado (`TypeFlag = 0`)

| Campo | Tamanho / Tipo | Presente em | Descrição e Função Técnica |
| :--- | :--- | :---: | :--- |
| **Signature / Magic Bytes** | 2 bytes | Ambos | Assinatura mágica constante: **`0x4E 0x50`** (carateres ASCII **`NP`** de Notepad). |
| **Sequence Number** | `uLEB128` | Ambos | Inteiro de sequência (frequentemente `0x00`). |
| **TypeFlag** | `uLEB128` | Ambos | **`0x01`** = Ficheiro associado no disco; **`0x00`** = Separador não gravado (*unsaved tab*). |
| **FilePathLength** | `uLEB128` | Apenas `TypeFlag = 1` | Comprimento do caminho do ficheiro em carateres (ex.: `0x6F` = 111 carateres). |
| **FilePath** | Variável (**UTF-16LE**) | Apenas `TypeFlag = 1` | Caminho completo do ficheiro no disco codificado em UTF-16LE (`2 × FilePathLength` bytes). |
| **FileSize** | `uLEB128` | Apenas `TypeFlag = 1` | Tamanho do ficheiro original em bytes no disco. |
| **Encoding & CR Type** | 2 bytes (`1B + 1B`) | Apenas `TypeFlag = 1` | Tipo de codificação de texto (ex.: `0x05` = UTF-8) e tipo de quebra de linha (`0x01` = CRLF). |
| **LastWriteTimestamp** | `uLEB128` | Apenas `TypeFlag = 1` | Carimbo temporal **FILETIME** da última gravação em disco, comprimido em `uLEB128`. |
| **FileHash** | 32 bytes | Apenas `TypeFlag = 1` | Hash SHA-256 do ficheiro em disco. |
| **Unknown Bytes / Flag** | `2 bytes` (`Type=1`) ou `1 byte` (`Type=0`) | Ambos | Bytes de controlo (terminando em `0x01` antes dos índices do cursor). |
| **SelectionStartIndex** | `uLEB128` | Ambos | Posição de início da seleção de texto (cursor). |
| **SelectionEndIndex** | `uLEB128` | Ambos | Posição de fim da seleção de texto. |
| **Configuration Block** | Bloco variável | Ambos | Parâmetros de quebra de linha (*word wrap*), flags de estado e codificação. |
| **ContentLength** | `uLEB128` | Ambos | Comprimento do texto do documento em carateres. |
| **Content** | Variável (**UTF-16LE**) | Ambos | O **conteúdo textual integral do separador** codificado em UTF-16 Little-Endian. |
| **Unsaved Flag** | 1 byte | Ambos | Flag de conteúdo pendente não gravado (`0` se salvo/sincronizado, `1` se conter edições não gravadas). |
| **Checksum CRC32** | 4 bytes (Big-Endian) | Ambos | Valor de integridade CRC-32 calculado sobre os dados desde o início do cabeçalho. |
| **Unsaved Buffer Chunks** | Bloco dinâmico | Ambos | Fragmentos de adições/remoções em memória pendentes antes do fecho formal da app. |

> [!IMPORTANT] Codificação Numérica e Textual
> O ficheiro combina dois formatos técnicos distintos:
> 1. **Texto**: Todas as strings (caminhos de ficheiros e conteúdo das notas) estão codificadas em **UTF-16LE** (2 bytes por caráter).
> 2. **Inteiros Numéricos**: Todos os contadores, comprimentos e até o *FILETIME* são codificados no formato de compressão **`uLEB128`**, detalhado em [[Codificação uLEB128 em Estruturas de Dados do Windows]].

---

## 3. Ferramentas Forenses de Extração

Para converter os ficheiros `{GUID}.bin` em relatórios legíveis, existem duas ferramentas de referência desenvolvidas pela comunidade de segurança:

```mermaid
flowchart LR
    BinFiles["Ficheiros TabState\\*.bin<br/>(Bytes brutos NP + uLEB128)"] --> ParserChoice{"Ferramenta de Extração"}
    
    ParserChoice --> AlFaifi["<b>notepad_parser</b> (Python)<br/>AbdulRhman Alfaifi"]
    ParserChoice --> Ogmini["<b>Notepad-State-Library</b> (C#)<br/>ogmini"]

    AlFaifi --> OutJSON["Exportação JSONL / CSV<br/>(info_notepad_data.jsonl)"]
    Ogmini --> OutChunks["Exportação por Pastas<br/>(UnsavedBufferChunks.csv)"]
```

### 1. `notepad_parser` (AbdulRhman Alfaifi)
Utilitário em Python de elevado desempenho e estabilidade:
```cmd
REM Exportar o histórico do Bloco de Notas para formato JSONL estruturado
notepad_parser.exe -f jsonl -o info_notepad_data.jsonl

REM Exportar diretamente para folha de cálculo CSV
notepad_parser.exe -f csv -o info_notepad_data.csv
```
*O utilitário processa automaticamente o diretório `LocalState\TabState`, valida a assinatura `NP`, descodifica o `uLEB128` e extrai o texto original.*

### 2. `Notepad-State-Library` (ogmini)
Biblioteca em C# (.NET) que decompõe cada separador e reconstrói os fragmentos não comitados (*Unsaved Buffer Chunks*):
```cmd
WindowsNotepadParser.exe -o C:\Temp\Notepad_Export
```
*Gera múltiplos ficheiros CSV com o conteúdo recuperado (com a ressalva de poder apresentar alguma instabilidade em formatos de compilações muito recentes do Windows).*

---

## 4. Enquadramento Laboratorial

A aquisição física da pasta `LocalState`, dissecação da estrutura binária `{GUID}.bin`, cálculo do checksum CRC32 e recuperação de texto não gravado é lecionada na **Ficha 10 – Windows Notepad**.

---

## Navegação

- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses|Voltar ao Índice do Capítulo 1]]
- [[Codificação uLEB128 em Estruturas de Dados do Windows]]
- [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]]
- [[Registry em Aplicações Modernas (MSIX e Helium)]]
- [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]]
- [[Organização de Estruturas de Dados em Binário]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Endianness e Ordem de Armazenamento]]
