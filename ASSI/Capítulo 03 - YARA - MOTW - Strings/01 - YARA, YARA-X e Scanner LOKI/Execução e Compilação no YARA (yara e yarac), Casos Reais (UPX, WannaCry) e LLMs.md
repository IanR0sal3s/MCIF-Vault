---
title: Execução e Compilação no YARA (yara e yarac), Casos Reais (UPX, WannaCry) e LLMs
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 3
bloco: 1
fonte_aula: YARA & LOKI (Prof. Patrício Domingues)
tags:
  - assi
  - forense
  - yara
  - yarac
  - upx
  - wannacry
  - mitre-attack
  - llm
aliases:
  - Execução do YARA
  - yarac
  - Regras compiladas YARA
  - YARA UPX
  - YARA WannaCry
atualizado: 2026-11-11
---

# Execução e Compilação no YARA (`yara` e `yarac`), Casos Reais (UPX, WannaCry) e LLMs

O YARA clássico disponibiliza dois executáveis — `yara` para análise direta e `yarac` para pré-compilação binária de regras — aplicando assinaturas sobre ficheiros, diretorias ou processos em execução.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Deteção)**: Interpretar regras em texto a cada invocação consome tempo de *parsing*; o `yarac` pré-compila as regras para formato binário (carregado via `yara -C`), otimizando execuções repetidas ou contínuas em *gateways*, *firewalls* e sistemas de monitorização.
> * **Porque importa (Forense / IR)**: Permite varrimentos recursivos multi-thread (`-r`, `-p`), listagem negativa de ficheiros não correspondentes (`-n`), extração exata de *offsets* (`-s`) para confirmar empacotamento (`UPX`) e deteção multi-indicador de famílias como o *WannaCry*.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **`-C` vs. `-c`**: **`-C`** (maiúscula) carrega regras pré-compiladas pelo `yarac`; **`-c`** (minúscula) imprime apenas a contagem de correspondências por ficheiro.
>   * **Regra `upx_packed`**: exige `"MZ"` exatamente no offset `0` (`$mz at 0`), secções `UPX0`/`UPX1` em `(0..1024)` e `"UPX!"` em `(1..1024)`.
>   * **Armadilha de LLM (`T1055.002`)**: usar `any of ($dll_name, ...)` incluindo `"kernel32.dll"` produz falsos positivos em praticamente todos os executáveis legítimos do Windows (*"One needs to validate and test the rule!"*).

---

## 1. Os Dois Executáveis (`yara` vs. `yarac`) e Regras Compiladas

**1. `yara`:** utilitário de linha de comandos para **executar as regras** contra um conjunto de ficheiros, diretorias ou identificadores de processos (`PID`).

**2. `yarac`:** utilitário de linha de comandos para **compilar as regras** num ficheiro binário pré-compilado.

* **Vantagem de desempenho**: uma regra compilada é executada muito mais rapidamente porque evita o passo de análise sintática (*parsing*) e compilação da regra de texto em cada execução.
* **Quando usar**: recomenda-se compilar uma regra sempre que esta vá ser **empregue várias vezes ou de forma contínua** (por exemplo, numa *firewall*, num *gateway* de correio ou num sistema de monitorização permanente).

**Procedimento de Compilação e Utilização:**

```bash
# 1. Compilar a regra de texto (rule.yar) para o ficheiro compilado (rule.yarac / rule.yarc)
yarac rule.yar rule.yarac

# 2. Executar o yara carregando a regra compilada com a flag -C (maiúscula)
yara -C rule.yarac INPUT
```

---

## 2. Anatomia do Comando `yara` / `yarac` e Opções Essenciais

### Anatomia do Comando `yara` e `yarac`

```text
yarac rule.yar rule.yarac
│     │        └─ Ficheiro binário de saída com as regras pré-compiladas
│     └────────── Ficheiro(s) fonte de regras YARA em texto
└──────────────── Compilador de regras YARA

yara [options] [NAMESPACE:]RULES_FILE... FILE | DIR | PID
│    │         │           │             └─ Alvo da análise: ficheiro, diretoria (com -r) ou PID
│    │         │           └─────────────── Ficheiro(s) de regras (.yar ou .yarac com -C)
│    │         └─────────────────────────── Namespace opcional para isolar identificadores de regras
│    └───────────────────────────────────── Flags de execução, output e desempenho
└────────────────────────────────────────── Motor executor de regras YARA
```

### Exemplos Fundamentais dos Diapositivos

**Analisar subdiretorias recursivamente (`-r`):**

```cmd
yara exemplo.yara -r c:\windows
```

**Negar as condições (`-n`) — listar apenas os ficheiros que NÃO cumprem a regra:**

```cmd
yara exemplo.yara -n -r DIRS_to_SEARCH
```

**Contagem de correspondências por ficheiro (`-c`):**

```cmd
yara suspicious_strings.yar -c -r DIR
```

### Opções Essenciais do `yara` (Aulas e Ficha 14)

| Opção Curta / Longa | Descrição Técnica |
| :--- | :--- |
| **`-r`, `--recursive`** | Pesquisa diretorias de forma **recursiva**. |
| **`-C`, `--compiled-rules`** | Carrega ficheiros de **regras pré-compiladas** com o `yarac`. |
| **`-n`, `--negate`** | Imprime apenas as regras **não satisfeitas**. |
| **`-c`, `--count`** | Imprime **apenas o número (contagem)** de correspondências por ficheiro. |
| **`-s`, `--print-strings`** | Imprime as **strings exatas e respetivos *offsets*** que dispararam na regra. |
| **`-m`, `--print-meta`** | Imprime os **metadados** (`meta:`) das regras que dispararam (Ficha 14). |
| **`-L`, `--print-string-length`** | Imprime o **comprimento** e *offset* das strings correspondidas (Ficha 14). |
| **`-g`, `--print-tags`** | Imprime as *tags* associadas à regra. |
| **`-p`, `--threads=NUMBER`** | Define o número de *threads* para varrer diretorias em paralelo. |
| **`-t`, `--tag=TAG`** | Filtra a saída para regras marcadas com a `TAG` indicada. |

---

## 3. Casos de Estudo Reais Analisados em Aula

### Caso 1: `suspicious_strings.yar` (Deteção de Engenharia Inversa, Depuração e Anti-VM)

* **Fonte**: [Regra `suspicious_strings.yar` (Yara-Rules)](https://raw.githubusercontent.com/Yara-Rules/rules/master/utils/suspicious_strings.yar).
* **Objetivo**: contém regras para identificar ferramentas de engenharia inversa, depuração (*debugging*) e deteção de máquinas virtuais para o sistema operativo Windows.

**Execução normal vs. Contagem (`-c`) demonstradas no Slide 16:**

**1.** `yara suspicious_strings.yar -r DIR` imprime o nome da regra disparada seguido do caminho do ficheiro:

```text
Misc_Suspicious_Strings c:\users\Public\Portable\android\commandlinetools-winADB\tools\bin\apkanalyzer.bat
Qemu_Detection c:\users\Public\Portable\android\...\guava-28.1-jre.jar
VMWare_Detection c:\users\Public\Portable\android\...\api-versions.xml
```

**2.** `yara suspicious_strings.yar -c -r DIR` imprime o caminho de cada ficheiro seguido do número total de regras que dispararam (`: 1`, `: 0`, etc.).

---

### Caso 2: Deteção de Executáveis Comprimidos com UPX (`upx_packed`)

* **O que é o UPX (*Ultimate Packer for eXecutables*)**: empacotador que comprime executáveis (reduzindo o seu tamanho) e que se **descompacta automaticamente em memória quando o programa é executado**. Embora legítimo, é frequentemente usado por *malware* para ocultar as suas strings em repouso no disco.

**Regra YARA para detetar arquivos UPX (`upx.yara`):**

```yara
rule upx_packed {
    meta:
        description = "detect a UPX file"
    strings:
        $mz = "MZ"
        $upx0 = {55505830000000}
        $upx1 = {55505831000000}
        $upx_sig = "UPX!"
    condition:
        $mz at 0 and $upx0 in (0..1024) and $upx1 in (0..1024) and $upx_sig in (1..1024)
}
```

* **Requisitos de Correspondência**:
  1. `$mz` (`"MZ"` $\to$ `4D5A`) tem de estar exatamente no início do ficheiro (`$mz at 0`);
  2. `$upx0` (`55 50 58 30 00 00 00` = `"UPX0\0\0\0"`) e `$upx1` (`55 50 58 31 00 00 00` = `"UPX1\0\0\0"`) têm de ocorrer nos primeiros 1024 bytes (`in (0..1024)`);
  3. A assinatura `$upx_sig` (`"UPX!"`) tem de ocorrer nos primeiros 1024 bytes (`in (1..1024)`).

**Execução e saída detalhada dos *offsets*:**

Ao executar `yara -r upx.yara DiretoriaAnalisar` (com exibição de strings), o YARA devolve os *offsets* exatos onde cada elemento foi encontrado no cabeçalho PE:

```text
0x0:2:$mz
0x188:7:$upx0
0x1b0:7:$upx1
0x205:4:$upx_sig
```

---

### Caso 3: Regra Completa do Ransomware *WannaCry* (`WannaCry_Ransomware`)

* **Contexto**: o **WannaCry** (maio de 2017) foi um *worm* de ransomware que explorou uma vulnerabilidade de *Remote Code Execution* (RCE) no protocolo SMBv1 do Windows (*EternalBlue*), causando prejuízos globais estimados em 4 mil milhões de dólares (incluindo mais de 100 milhões no NHS britânico).

**Regra Oficial de Florian Roth Analisada no Slide 18:**

```yara
rule WannaCry_Ransomware {
    meta:
        description = "Detects WannaCry Ransomware"
        author = "Florian Roth (with the help of binar.ly)"
        reference = "https://goo.gl/HG2j5T"
        date = "2017-05-12"
        hash1 = "ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa"
    strings:
        $x1 = "icacls . /grant Everyone:F /T /C /Q" fullword ascii
        $x2 = "taskdl.exe" fullword ascii
        $x3 = "tasksche.exe" fullword ascii
        $x4 = "Global\\MsWinZonesCacheCounterMutexA" fullword ascii
        $x5 = "WNcry@2ol7" fullword ascii
        $x6 = "www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com" ascii
        $x7 = "mssecsvc.exe" fullword ascii
        $x8 = "C:\\%s\\qeriuwjhrf" fullword ascii
        $x9 = "icacls . /grant Everyone:F /T /C /Q" fullword ascii

        $s1 = "C:\\%s\\%s" fullword ascii
        $s2 = "<!-- Windows 10 -->" fullword ascii
        $s3 = "cmd.exe /c \"%s\"" fullword ascii
        $s4 = "msg/m_portuguese.wnry" fullword ascii
        $s5 = "\\\\192.168.56.20\\IPC$" fullword wide
        $s6 = "\\\\172.16.99.5\\IPC$" fullword wide

        $op1 = { 10 ac 72 0d 3d ff ff 1f ac 77 06 b8 01 00 00 00 }
        $op2 = { 44 24 64 8a c6 44 24 65 0e c6 44 24 66 80 c6 44 }
        $op3 = { 18 df 6c 24 14 dc 64 24 2c dc 6c 24 5c dc 15 88 }
        $op4 = { 09 ff 76 30 50 ff 56 2c 59 59 47 3b 7e 0c 7c }
        $op5 = { c1 ea 1d c1 ee 1e 83 e2 01 83 e6 01 8d 14 56 }
        $op6 = { 8d 48 ff f7 d1 8d 44 10 ff 23 f1 23 c1 }
    condition:
        uint16(0) == 0x5a4d and filesize < 10000KB and ( 1 of ($x*) and 1 of ($s*) or 3 of ($op*) )
}
```

* **Dissecação Pericial dos Indicadores da Regra**:
  * **Strings críticas (`$x1` a `$x9`)**:
    * Comando [[Gestão e Manipulação de VSS (CLI, PowerShell e Permissões)|icacls]] (`icacls . /grant Everyone:F /T /C /Q`) para assumir permissões totais sobre os ficheiros antes da cifragem;
    * Executáveis do *dropper* e do serviço (`taskdl.exe`, `tasksche.exe`, `mssecsvc.exe`);
    * Nome do *Mutex* (`Global\MsWinZonesCacheCounterMutexA`) e password do arquivo ZIP interno (`WNcry@2ol7`);
    * Domínio de *killswitch* (`www.iuqerfsodp9ifjaposdfjhgosurijfaewrwergwea.com`).
  * **Strings secundárias (`$s1` a `$s6`)**:
    * Ficheiro de mensagem de resgate em português (`msg/m_portuguese.wnry`);
    * Caminhos UNC de partilhas de rede `IPC$` hardcoded do ambiente de laboratório dos atacantes (`\\192.168.56.20\IPC$` e `\\172.16.99.5\IPC$` em `fullword wide`).
  * **Sequências de *opcodes* (`$op1` a `$op6`)**: instruções máquina em hexadecimal que identificam a lógica binária do WannaCry mesmo que as strings sejam ofuscadas.
  * **Lógica da `condition:`**: exige cabeçalho PE (`uint16(0) == 0x5a4d`), tamanho inferior a 10 MB (`filesize < 10000KB`) e **`(1 of ($x*) and 1 of ($s*))` OU `3 of ($op*)`**.

---

## 4. Utilização de LLMs para Criar Regras YARA

Pode recorrer-se a um *Large Language Model* (ex.: ChatGPT) para gerar um rascunho de regra YARA mapeado a técnicas da matriz **MITRE ATT&CK**:

**Prompt exemplificado no Slide 20:**

> *"As a cybersecurity expert, write a YARA rule to detect MITRE ATT&CK sub-technique T1055.002"* (*Process Injection: Thread Execution Hijacking*).

**Regra gerada pelo ChatGPT (`detect_T1055_002`):**

```yara
rule detect_T1055_002 {
    meta:
        description = "Detects Process Injection: Thread Execution Hijacking (MITRE ATT&CK T1055.002)"
        author = "Your Name"
        reference = "https://attack.mitre.org/techniques/T1055/002/"
    strings:
        $dll_name = "kernel32.dll" wide ascii
        $create_remote_thread_api = "CreateRemoteThread" wide ascii
        $open_process_api = "OpenProcess" wide ascii
    condition:
        any of ($dll_name, $create_remote_thread_api, $open_process_api)
}
```

> [!WARNING] Alerta Crítico da Aula sobre Regras Geradas por LLMs
> **"One needs to validate and test the rule!"** — É indispensável validar e testar qualquer regra gerada por um LLM. Repare-se no defeito grave da condição gerada pelo ChatGPT no exemplo acima: ao usar `any of ($dll_name, ...)`, **qualquer executável legítimo do Windows que importe `kernel32.dll` (praticamente 100% dos programas Windows) dispararia esta regra como falso positivo.**

---

## Além da aula

* **Ponte com a Extração de Strings (Bloco 03) e VSS (Capítulo 1)**:
  * Quando uma amostra dispara a regra `upx_packed`, o perito sabe que deve descompactá-la (`upx -d ficheiro.exe`) antes de usar [[Conceito de Strings e Comando strings em Unix-Linux|strings]] ou [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios|bstrings]], pois o empacotador UPX comprime a tabela de strings original nas secções `UPX0`/`UPX1`.
  * Na regra do WannaCry, o indicador `$x1 = "icacls . /grant Everyone:F /T /C /Q"` complementa diretamente o estudo das permissões NTFS e eliminação de *Shadow Copies* visto em [[Gestão e Manipulação de VSS (CLI, PowerShell e Permissões)]].

---

## Perguntas de revisão

1. **Qual é a diferença entre os executáveis `yara` e `yarac`, em que cenários se recomenda usar o `yarac` e qual a flag obrigatória para carregar uma regra compilada?**

> [!success]- Ver Resposta
> O **`yara`** executa regras contra ficheiros, diretorias ou `PID`s, enquanto o **`yarac`** compila regras de texto para um ficheiro binário (`yarac rule.yar rule.yarac`). Recomenda-se o `yarac` quando as regras são usadas repetidamente ou em execução contínua (*firewalls*, *gateways* de correio, monitorização), pois evita re-analisar o texto em cada execução. Para carregar o binário resultante no `yara`, é obrigatória a flag **`-C`** (`--compiled-rules`).

2. **Distinga as flags `-r`, `-n`, `-c`, `-C`, `-m` e `-s` na linha de comandos do `yara`.**

> [!success]- Ver Resposta
> **`-r`** (`--recursive`) analisa diretorias recursivamente; **`-n`** (`--negate`) imprime apenas as regras não satisfeitas; **`-c`** (`--count`) imprime apenas a contagem de correspondências por ficheiro; **`-C`** (`--compiled-rules`) carrega regras pré-compiladas pelo `yarac`; **`-m`** (`--print-meta`) exibe os metadados da secção `meta:`; e **`-s`** (`--print-strings`) imprime as strings exatas e respetivos *offsets* correspondidos.

3. **Como funciona a regra `upx_packed` para identificar um executável comprimido com UPX e que implicação prática tem na análise de strings?**

> [!success]- Ver Resposta
> Exige o marcador `$mz` (`"MZ"`) exatamente no *offset* `0` (`$mz at 0`), as assinaturas das secções `$upx0` (`UPX0\0\0\0`) e `$upx1` (`UPX1\0\0\0`) nos primeiros `1024` bytes (`in (0..1024)`) e `$upx_sig` (`"UPX!"`) em `(1..1024)`. Quando dispara, indica que as strings originais do binário estão comprimidas em disco, devendo o analista descompactar o binário (`upx -d`) antes de executar `strings` ou `bstrings`.

4. **Na regra `WannaCry_Ransomware`, quais são os três grupos de indicadores usados e qual é a lógica da `condition:`?**

> [!success]- Ver Resposta
> Combina strings críticas de execução/killswitch/mutex (`$x1`–`$x9`, ex.: `icacls`, `taskdl.exe`, `WNcry@2ol7`, domínio `www.iuqerfsodp...`), strings secundárias/UNC de laboratório (`$s1`–`$s6`, ex.: `msg/m_portuguese.wnry`, `\\192.168.56.20\IPC$`) e sequências de *opcodes* (`$op1`–`$op6`). A `condition:` exige cabeçalho PE (`uint16(0) == 0x5a4d`), `filesize < 10000KB` e `(1 of ($x*) and 1 of ($s*))` OU `3 of ($op*)`.

5. **Na regra gerada por LLM para a técnica `T1055.002`, porque é que a aula sublinha *"One needs to validate and test the rule!"*?**

> [!success]- Ver Resposta
> Porque o ChatGPT gerou `condition: any of ($dll_name, $create_remote_thread_api, $open_process_api)` incluindo `$dll_name = "kernel32.dll"`. Como quase todos os executáveis legítimos do Windows importam `kernel32.dll`, a regra dispararia falsos positivos massivos sem validação e correção manual prévia.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[YARA - Tipos de Strings, Modificadores, Formato Hexadecimal, Base64 e Regex]] | `mesmo bloco` |
| **Seguinte** | [[YARA-X (Reimplementação em Rust) e Ferramenta CLI yr]] | `mesmo bloco` |
| **Índice** | [[Capítulo 3 - YARA - MOTW - Strings]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[YARA - Introdução, Estrutura de Regras, Metadados e Condições]] · `mesmo bloco`
* [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração]] · `mesmo bloco`
* [[Gestão e Manipulação de VSS (CLI, PowerShell e Permissões)]] · `Cap. 1`
