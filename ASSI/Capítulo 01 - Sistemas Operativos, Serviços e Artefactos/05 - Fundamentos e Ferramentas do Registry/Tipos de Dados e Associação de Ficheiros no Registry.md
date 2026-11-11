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
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://posts.specterops.io/the-defenders-guide-to-the-windows-registry-febe241abc75"
atualizado: 2026-09-23
---

# Tipos de Dados e Associação de Ficheiros no Registry

Tipificação binária dos valores armazenados no Windows Registry e mecanismo de resolução de extensões e classes de ficheiros sob o ramo `HKEY_CLASSES_ROOT` (`assoc` e `ftype`).

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: As APIs Win32 e o *kernel* necessitam de saber como interpretar os bytes de cada valor no Registry (texto fixo, variáveis de ambiente dinâmicas, inteiros de 32/64 bits ou *blobs* binários). Em paralelo, a *shell* do Windows consulta `HKCR` para saber que executável e argumentos invocar quando o utilizador faz duplo clique num ficheiro (`.txt`, `.mp3`, `.docx`).
> * **Porque importa (Forense)**: A compreensão dos tipos de dados evita erros de interpretação (como endianness em `REG_DWORD`/`REG_QWORD` ou estruturas complexas em `REG_BINARY`). Já as associações de ficheiros em `HKCU\Software\Classes` constituem um vetor clássico de persistência furtiva sem privilégios de administrador (*File Association Hijacking*).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Prioridade `HKCU` sobre `HKLM` em `HKCR`**: `HKCR` funde `HKLM\SOFTWARE\Classes` e `HKCU\Software\Classes`. Caso exista conflito, **vence a definição de `HKCU`**, permitindo a um atacante sem privilégios administrativos sequestrar a abertura de extensões comuns.
>   * **Cadeia `assoc` $\rightarrow$ `ftype`**: A extensão (`.ext`) não aponta diretamente para o executável; aponta primeiro para um *ProgID* / classe (`assoc`), e é essa classe que define a linha de comandos de abertura (`ftype`).

---

## Tipos de Dados do Registry

Cada entrada de valor no Windows Registry possui um identificador numérico e simbólico que dita o seu formato de armazenamento:

| ID | Nome do Tipo | Tamanho / Endianness | Descrição e Comportamento Forense |
| :---: | :--- | :---: | :--- |
| `0` | `REG_NONE` | Variável | Sem tipo definido. Utilizado por aplicações para guardar *blobs* binários sem validação de estrutura. |
| `1` | `REG_SZ` | Variável (UTF-16LE) | String de texto de comprimento fixo terminada em nulo (`\0`), armazenada em Unicode (UTF-16LE). |
| `2` | `REG_EXPAND_SZ` | Variável (UTF-16LE) | String extensível contendo variáveis de ambiente não expandidas (ex.: `%PATH%`, `%SystemRoot%`), resolvidas dinamicamente em tempo de execução. |
| `3` | `REG_BINARY` | Arbitrário | Dados binários puros de tamanho arbitrário (ex.: chaves criptográficas, estruturas `SYSTEMTIME`, `MRUListEx`, contadores `UserAssist`). |
| `4` | `REG_DWORD` | 32 bits (4 bytes) **Little-Endian** | Inteiro de 32 bits em formato Little-Endian (o mais comum para flags booleanas `0`/`1`, contadores e portas). |
| `5` | `REG_DWORD_BIG_ENDIAN` | 32 bits (4 bytes) **Big-Endian** | Inteiro de 32 bits armazenado com o byte mais significativo primeiro (Big-Endian). |
| `6` | `REG_LINK` | Variável (Unicode) | Ligação simbólica (*symbolic link*) Unicode que aponta internamente para outra chave do Registry (ex.: `CurrentControlSet` $\rightarrow$ `ControlSet001`). |
| `7` | `REG_MULTI_SZ` | Variável (UTF-16LE) | Vetor/lista de strings; cada string individual termina em nulo (`\0`) e a lista completa encerra com um nulo duplo (`\0\0`). |
| `8` | `REG_RESOURCE_LIST` | Variável | Lista de recursos de hardware empregue por controladores *Plug-and-Play* (PnP). |
| `9` | `REG_FULL_RESOURCE_DESCRIPTOR` | Variável | Descritores completos de recursos físicos de hardware PnP (interrupts, portas I/O, DMA). |
| `10` | `REG_RESOURCE_REQUIREMENTS_LIST` | Variável | Lista de requisitos de recursos de hardware necessários para um controlador de dispositivo. |
| `11` | `REG_QWORD` | 64 bits (8 bytes) **Little-Endian** | Inteiro de 64 bits em formato Little-Endian (muito comum em marcas temporais `FILETIME64` de alta precisão). |

---

## Associação de Ficheiros (`HKEY_CLASSES_ROOT`)

O hive lógico `HKEY_CLASSES_ROOT` (**HKCR**) gere a relação entre extensões de ficheiros (`.ext`) e os binários responsáveis pelo seu tratamento, abertura e ícones associados. O processo ocorre em dois passos encadeados:

1. **Mapeamento da Extensão (`assoc`)**: Uma subchave de extensão (ex.: `HKCR\.docx` ou `HKCR\.txt`) aponta no seu valor padrão `(Default)` para um identificador programático de classe de documento (*ProgID*, ex.: `Word.Document.12` ou `txtfilelegacy`).
2. **Comando de Execução da Classe (`ftype`)**: A subchave correspondente à classe de documento (ex.: `HKCR\Word.Document.12\shell\open\command`) define a linha de comandos exata que o sistema operativo invoca para abrir o ficheiro.

---

## Anatomia dos Comandos Nativos: `assoc` e `ftype`

A administração, auditoria e deteção de anomalias nestas associações pode ser efetuada na consola (`cmd.exe`) através de dois comandos internos:

### 1. Utilitário `assoc` (Extensão $\rightarrow$ Classe)
Exibe ou modifica o mapeamento entre uma extensão de ficheiro e o respetivo identificador de tipo de ficheiro (*ProgID*):

```cmd
assoc .txt
REM Resultado: .txt=txtfilelegacy

assoc .zip
REM Resultado: .zip=CompressedFolder

assoc
REM Executado sem argumentos, lista todas as associações de extensões registadas no sistema
```

### 2. Utilitário `ftype` (Classe $\rightarrow$ Linha de Comandos do Executável)
Exibe ou define a linha de comandos exata que o Windows executa quando abre um tipo de ficheiro associado:

```cmd
ftype | findstr /i "mp3"
```

* **`ftype`**: lista todos os tipos de ficheiro (*ProgIDs*) e respetivos comandos de execução configurados em `shell\open\command`.
* **`| findstr /i "mp3"`**: redireciona a saída via *pipe* para o filtro de texto `findstr`, procurando de forma insensível a maiúsculas/minúsculas (`/i`) pela string `"mp3"`.

Exemplo de saídas típicas:

```text
VLC.mp3="C:\Program Files (x86)\VideoLAN\VLC\vlc.exe" --started-from-file "%1"
WMP11.AssocFile.MP3="%ProgramFiles(x86)%\Windows Media Player\wmplayer.exe" /prefetch:6 /Open "%L"
```

* **Anatomia dos Marcadores de Argumento**: Os modificadores **`"%1"`** ou **`"%L"`** (versão de nome longo de ficheiro) indicam a posição exata onde o Windows injeta o caminho completo do ficheiro clicado pelo utilizador como argumento para o executável.

---

## Implicações Forenses e de Segurança

| Vetor / Mecanismo | Chave Envolvida | Explicação Técnica e Impacto Pericial |
| :--- | :--- | :--- |
| **File Association Hijacking** (MITRE ATT&CK T1546.001) | `...\<Classe>\shell\open\command` | Adulteração do executável configurado no comando `ftype` (ou substituição do `ProgID` associado à extensão). Como o utilizador abre rotineiramente documentos (`.txt`, `.pdf`, `.docx`), o atacante garante a execução do seu *payload* sempre que um ficheiro é aberto, sem usar chaves óbvias como `Run` ou `RunOnce`. |
| **Sequestro sem Privilégios (Prioridade `HKCU`)** | `HKCU\Software\Classes\<ext>` vs. `HKLM\SOFTWARE\Classes\<ext>` | O hive `HKCR` é uma vista resultante da fusão entre `HKLM\SOFTWARE\Classes` (máquina) e `HKCU\Software\Classes` (utilizador, guardado em `USRCLASS.DAT`). **O Windows atribui prioridade às chaves de `HKCU`**. Um utilizador ou *malware* sem privilégios de administrador pode criar uma chave em `HKCU\Software\Classes` que sobrepõe a associação global da máquina, intercetando a abertura de ficheiros. |

---

## Perguntas de revisão

1. **Qual a diferença estrutural e funcional entre os tipos de dados `REG_SZ`, `REG_EXPAND_SZ` e `REG_MULTI_SZ` no Windows Registry?**

> [!success]- Ver Resposta
> `REG_SZ` (ID 1) armazena uma única string de texto estática terminada num carácter nulo (`\0`). `REG_EXPAND_SZ` (ID 2) armazena uma string contendo variáveis de ambiente (como `%SystemRoot%` ou `%ProgramFiles%`) que são expandidas dinamicamente pelo sistema quando lidas. `REG_MULTI_SZ` (ID 7) armazena um vetor/lista de múltiplas strings, onde cada elemento é separado por um nulo simples (`\0`) e a lista completa termina com um nulo duplo (`\0\0`).

2. **Como se articulam os comandos `assoc` e `ftype` para determinar que programa é executado quando o utilizador faz duplo clique num ficheiro `.txt`?**

> [!success]- Ver Resposta
> O processo ocorre em duas fases: primeiro, o comando `assoc .txt` consulta `HKCR\.txt` para descobrir a que classe de documento (*ProgID*) a extensão está associada (ex.: `.txt=txtfilelegacy`). Em seguida, o comando `ftype txtfilelegacy` consulta `HKCR\txtfilelegacy\shell\open\command` para obter o caminho exato do binário executável e os seus parâmetros (ex.: `notepad.exe "%1"`).

3. **Numa saída do comando `ftype`, qual o significado dos parâmetros `"%1"` ou `"%L"` no final da linha de comandos do executável?**

> [!success]- Ver Resposta
> Representam os marcadores de substituição (*placeholders*) onde a *shell* do Windows injeta o caminho completo do ficheiro que o utilizador clicou para abrir, passando-o como argumento de entrada para o executável associado.

4. **Porque é que a arquitetura do hive `HKEY_CLASSES_ROOT` (`HKCR`) permite a um processo malicioso sem privilégios de administrador realizar um ataque de *File Association Hijacking*?**

> [!success]- Ver Resposta
> Porque `HKCR` é uma vista virtual que combina `HKLM\SOFTWARE\Classes` (que exige privilégios administrativos para escrita) e `HKCU\Software\Classes` (gravado no hive `USRCLASS.DAT` do utilizador, editável sem elevação). Como o Windows dá precedência às entradas de `HKCU` sobre as de `HKLM`, qualquer chave criada em `HKCU\Software\Classes` sobrepõe a associação global do sistema para esse utilizador.

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Artefactos Forenses de Execução e Persistência no Registry]]
- [[Endianness e Ordem de Armazenamento]]
- [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
