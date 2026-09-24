---
title: Tipos de Dados e Associação de Ficheiros no Registry
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
  - windows
  - registry
  - associacoes
  - forense
aliases:
  - Registry Data Types
  - File Associations
  - assoc
  - ftype
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://posts.specterops.io/the-defenders-guide-to-the-windows-registry-febe241abc75"
atualizado: 2026-09-23
---

# Tipos de Dados e Associação de Ficheiros no Registry

Cada entrada no Windows Registry armazena um valor tipificado segundo formatos padrão reconhecidos pelas APIs Win32 e pelo kernel. Para além da configuração do sistema, o Registry (particularmente sob `HKCR`) governa a forma como o Windows reage à interação com qualquer tipo de ficheiro através de associações.

## Tipos de Dados do Registry

O sistema define identificadores numéricos e simbólicos para cada tipo de dado:

| ID | Nome do Tipo | Descrição e Comportamento |
| :---: | :--- | :--- |
| `0` | `REG_NONE` | Sem tipo definido. Utilizado por aplicações para guardar blobs sem validação. |
| `1` | `REG_SZ` | String de texto terminada em nulo (armazenada em UTF-16LE em APIs Unicode). |
| `2` | `REG_EXPAND_SZ` | String extensível contendo variáveis de ambiente não expandidas (ex.: `%PATH%`, `%SystemRoot%`), resolvidas em tempo de execução. |
| `3` | `REG_BINARY` | Dados binários puros de tamanho arbitrário (ex.: chaves criptográficas, estruturas empacotadas). |
| `4` | `REG_DWORD` | Inteiro de 32 bits em formato **Little-Endian** (o mais comum para booleanos, contadores e portas). |
| `5` | `REG_DWORD_BIG_ENDIAN` | Inteiro de 32 bits armazenado em formato **Big-Endian**. |
| `6` | `REG_LINK` | Ligação simbólica Unicode para outra chave do Registry. |
| `7` | `REG_MULTI_SZ` | Vetor de strings; cada string termina em nulo (`\0`) e a lista fecha com um nulo duplo. |
| `8` | `REG_RESOURCE_LIST` | Lista de recursos de hardware empregue por controladores Plug-and-Play (PnP). |
| `9` | `REG_FULL_RESOURCE_DESCRIPTOR` | Descritores completos de recursos de hardware PnP. |
| `10` | `REG_RESOURCE_REQUIREMENTS_LIST` | Lista de requisitos de recursos de hardware para dispositivos. |
| `11` | `REG_QWORD` | Inteiro de 64 bits em formato Little-Endian (comum em marcas temporais de alta precisão). |

## Associação de Ficheiros (`HKEY_CLASSES_ROOT`)

O hive `HKEY_CLASSES_ROOT` (HKCR) gere a relação entre extensões de ficheiros (`.ext`) e os binários responsáveis pelo seu tratamento, abertura e ícones associados:
* Uma subchave de extensão (ex.: `HKCR\.docx`) aponta para uma classe de documento (ex.: `Word.Document.12`).
* A classe de documento define os comandos do menu de contexto na subchave `shell\open\command`.

### Utilitários CLI Nativos: `assoc` e `ftype`

A administração e auditoria destas associações pode ser efetuada rapidamente na linha de comandos:

#### 1. Utilitário `assoc`
Exibe ou modifica o mapeamento de uma extensão para um identificador de tipo de ficheiro:

```cmd
assoc .txt
REM Resultado: .txt=txtfilelegacy

assoc .zip
REM Resultado: .zip=CompressedFolder

assoc
REM Lista todas as associações de extensões registadas no sistema
```

#### 2. Utilitário `ftype`
Exibe ou define a linha de comandos exata que o sistema operativo invoca ao abrir o tipo de ficheiro associado:

```cmd
ftype | findstr /i "mp3"
```

Exemplo de saídas típicas:
```text
VLC.mp3="C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" --started-from-file "%1"
WMP11.AssocFile.MP3="%ProgramFiles(x86)%\Windows Media Player\wmplayer.exe" /prefetch:6 /Open "%L"
```

* Os modificadores `%1` ou `"%L"` indicam onde o caminho do ficheiro clicado pelo utilizador é injetado como argumento do executável.

## Implicações Forenses e de Segurança

1. **Persistência por Abuso de Associações (*File Association Hijacking*)**:
   * Uma técnica comum de persistência (MITRE ATT&CK T1546.001) consiste em adulterar o executável configurado no comando `ftype` ou alterar o manipulador sob `HKCU\Software\Classes\<ext>`.
   * Como o utilizador abre rotineiramente documentos (`.txt`, `.pdf`, `.docx`), o atacante assegura a execução do seu payload sem necessidade de recorrer às chaves convencionais de arranque `Run`/`RunOnce`.
2. **Prioridade de Resolução**:
   * O hive `HKCR` é uma fusão entre `HKLM\SOFTWARE\Classes` (definições de máquina) e `HKCU\Software\Classes` (definições do utilizador).
   * O Windows atribui prioridade às chaves de `HKCU`. Um utilizador sem privilégios de administrador pode criar uma entrada em `HKCU\Software\Classes` que sobrepõe a associação global, permitindo a execução de binários maliciosos sem elevar privilégios.

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Artefactos Forenses de Execução e Persistência no Registry]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
