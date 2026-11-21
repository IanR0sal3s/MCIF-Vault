---
title: Tipos de Dados e Associação de Ficheiros no Registry
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
  - associacoes
  - forense
aliases:
  - Registry Data Types
  - File Associations
  - assoc
  - ftype
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
fontes:
  - "https://posts.specterops.io/the-defenders-guide-to-the-windows-registry-febe241abc75"
atualizado: 2026-11-21
---

# Tipos de Dados e Associação de Ficheiros no Registry

Cada valor no Windows Registry possui um **tipo de dados** que define como interpretar os seus bytes. Por sua vez, o ramo `HKEY_CLASSES_ROOT` (`HKCR`) controla como o Windows associa extensões de ficheiros a executáveis (`assoc` e `ftype`).

## 1. Os 6 Tipos de Dados Essenciais em Forense

| ID | Tipo | Formato | Uso Típico no Registry |
| :---: | :--- | :--- | :--- |
| `1` | **`REG_SZ`** | String fixa (`UTF-16LE`, termina em `\0`) | Caminhos, nomes de aplicações, `MRUList`. |
| `2` | **`REG_EXPAND_SZ`** | String com variáveis de ambiente | Caminhos dinâmicos como `%SystemRoot%\System32\...` ou `%PATH%`. |
| `3` | **`REG_BINARY`** | Bytes brutos de tamanho arbitrário | Estruturas binárias (`UserAssist` 72 B, `SYSTEMTIME` 16 B, `MRUListEx`). |
| `4` | **`REG_DWORD`** | Inteiro 32 bits (4 B, Little-Endian) | Flags booleanas (`0`/`1`), contadores, portas. |
| `7` | **`REG_MULTI_SZ`** | Lista de strings (`\0` entre itens, `\0\0` no fim) | Listas de serviços em `Svchost`, dependências de drivers. |
| `11` | **`REG_QWORD`** | Inteiro 64 bits (8 B, Little-Endian) | Marcas temporais `FILETIME64`. |

---

## 2. Associação de Ficheiros (`HKCR`, `assoc` e `ftype`)

A abertura de um ficheiro por duplo clique resolve-se em **dois passos encadeados** sob `HKEY_CLASSES_ROOT`:

1. **Extensão → Classe (`assoc`)**: `HKCR\.txt` aponta para um *ProgID* (ex.: `txtfilelegacy`).
2. **Classe → Comando (`ftype`)**: `HKCR\txtfilelegacy\shell\open\command` define o executável e argumentos (onde **`"%1"`** ou **`"%L"`** recebe o caminho completo do ficheiro clicado).

```cmd
assoc .txt                    :: .txt=txtfilelegacy
assoc .zip                    :: .zip=CompressedFolder
ftype | findstr /i "mp3"      :: VLC.mp3="C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" --started-from-file "%1"
```

> [!WARNING] Prioridade `HKCU` > `HKLM` (*File Association Hijacking*)
> O `HKCR` é a fusão virtual de `HKLM\SOFTWARE\Classes` (global, exige Admin) com `HKCU\Software\Classes` (utilizador, em `USRCLASS.DAT`). Em caso de conflito, **prevalece `HKCU`** — permitindo a um atacante **sem privilégios de administrador** sequestrar a abertura de ficheiros comuns (ex.: `.txt`, `.docx`) para obter persistência.

---

## Além da aula

* **Outros tipos internos do Registry (raros em forense)**: `REG_NONE` (`0`, sem tipo), `REG_DWORD_BIG_ENDIAN` (`5`), `REG_LINK` (`6`, ligação simbólica interna como `CurrentControlSet`), e os descritores de hardware PnP `REG_RESOURCE_LIST` (`8`), `REG_FULL_RESOURCE_DESCRIPTOR` (`9`) e `REG_RESOURCE_REQUIREMENTS_LIST` (`10`).

---

## Perguntas de revisão

1. **Qual a diferença entre `REG_SZ`, `REG_EXPAND_SZ` e `REG_MULTI_SZ`?**

> [!success]- Ver Resposta
> `REG_SZ` guarda uma única string fixa; `REG_EXPAND_SZ` guarda uma string com variáveis de ambiente (ex.: `%SystemRoot%`) expandidas em tempo de execução; `REG_MULTI_SZ` guarda uma lista de múltiplas strings separadas por `\0` e terminada por `\0\0`.

2. **Como se articulam `assoc` e `ftype`, e qual o papel de `"%1"` / `"%L"`?**

> [!success]- Ver Resposta
> `assoc` mapeia a extensão (`.txt`) para um tipo/classe (`txtfilelegacy`); `ftype` mapeia essa classe para a linha de comandos do executável. `"%1"` ou `"%L"` marca onde o Windows injeta o caminho completo do ficheiro aberto.

3. **Porque é que um atacante sem privilégios de administrador consegue sequestrar associações de ficheiros?**

> [!success]- Ver Resposta
> Porque `HKCR` funde `HKLM\SOFTWARE\Classes` com `HKCU\Software\Classes` (no `USRCLASS.DAT` do utilizador) dando **prioridade a `HKCU`**, onde o utilizador pode escrever sem elevação.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Estrutura e Hives do Windows Registry]] | `mesmo bloco` |
| **Seguinte** | [[Ferramentas de Análise e Extração do Registry]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 05` |

### Conceitos Relacionados

* [[Artefactos Forenses de Execução e Persistência no Registry]] · `Bloco 07`
* [[Endianness e Ordem de Armazenamento]] · `AFD1 · Cap. 3`
* [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]] · `AFD1 · Cap. 3`
