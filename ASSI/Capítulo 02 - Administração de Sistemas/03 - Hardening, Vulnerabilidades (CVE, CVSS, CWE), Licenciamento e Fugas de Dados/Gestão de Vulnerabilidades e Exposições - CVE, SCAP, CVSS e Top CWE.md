---
title: Gestão de Vulnerabilidades e Exposições - CVE, SCAP, CVSS e Top CWE
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 3
fonte_aula: System Administration - System and Data Management.pdf
tags:
  - assi
  - administracao-sistemas
  - cve
  - cvss
  - cwe
  - scap
  - mitre
  - sharepoint
  - nvd
aliases:
  - CVE
  - Common Vulnerabilities and Exposures
  - CVSS
  - Common Vulnerability Scoring System
  - CWE Top 10 2025
  - SCAP
  - Vulnerability vs Exposure
atualizado: 2026-11-11
---

# Gestão de Vulnerabilidades e Exposições — CVE, SCAP, CVSS e Top CWE

O sistema **CVE** (MITRE, 1999) identifica falhas únicas via **SCAP** (`CVE-YYYY-NNNNN`), separando **Vulnerabilidades** de **Exposições**, quantificadas por **CVSS** (`0–10`) e classificadas pelo **Top CWE**.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Equipas de administração, fabricantes e ferramentas automáticas de auditoria necessitam de uma taxonomia unificada para nomear falhas concretas (**CVE** atribuído via **SCAP** por um **CNA**), medir o seu impacto operacional (**CVSS**) e categorizar os erros de programação subjacentes (**CWE**).
> * **Porque importa (Segurança / Forense)**: Distinguir **Vulnerabilidade** (fraqueza explorável de software, como os Zero-Days do SharePoint `CVE-2025-53770` que criam *webshells* `spinstall0.aspx`) de **Exposição** (má configuração na *cloud*, como **Apollo** e **People Data Labs**) orienta tanto a remediação preventiva como a triagem em resposta a incidentes — onde relatórios FBI/CISA revelam que falhas com vários anos continuam entre as mais exploradas.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **CVE vs. CWE**: o **CVE** identifica uma ocorrência específica num produto (`CVE-YYYY-NNNNN`), enquanto a **CWE** classifica o padrão genérico de fraqueza (Top 3 de 2025: `CWE-79` XSS `60.39`, `CWE-89` SQLi `28.72`, `CWE-352` CSRF `19.65`);
>   * **Escala CVSS (`0–10`)**: memorizar os cinco intervalos exatos (`None: 0.0`, `Low: 0.1–3.9`, `Medium: 4.0–6.9`, `High: 7.0–8.9`, `Critical: 9.0–10.0`) e ler a *Vector String*;
>   * **Zero-Day SharePoint (`CVE-2025-53770`, CVSS `9.8`)**: pedido `HTTP POST` para `"/_layouts/15/ToolPane.aspx"` que escreve **`spinstall0.aspx`** via PowerShell.

---

## 1. *Common Vulnerabilities and Exposures* (CVE) e Protocolo SCAP (Slides 47–52)

### 1.1. Origem, Protocolo SCAP e Estrutura de uma Entrada CVE (Slides 48, 51–52)

* **Definição e origem**: catálogo público de vulnerabilidades e exposições de segurança da informação ([MITRE CVE](https://cve.mitre.org/)), lançado em **1999 pela MITRE** (organização sem fins lucrativos) para identificar, padronizar e categorizar falhas em software e firmware;
* **Catalogação via `SCAP` (*Security Content Automation Protocol*)**: recolhe, avalia a informação e atribui um identificador único a cada falha;
* **Estrutura de um registo CVE (*CVE Entry*)**:
  * **Identificador padrão (`CVE ID`)**: formato **`CVE-YYYY-NNNNN`** (ano de atribuição + número sequencial, ex.: `CVE-2021-36941`, `CVE-2022-21082`);
  * **Indicador de estado** (*Status indicator*);
  * **Breve descrição técnica** da falha e impacto;
  * **Referências** (avisos do fabricante, *patches*, relatórios) e identificação da entidade emissora (**`Assigning CNA`** — *CVE Numbering Authority*, ex.: `google_android`).

### 1.2. Diferença entre *Vulnerability* e *Exposure* (Slides 49–50)

| Conceito | Definição Técnica (Slide 49) | Exemplos Reais dos Diapositivos (Slides 48 e 50) |
| :--- | :--- | :--- |
| **Vulnerability** (Vulnerabilidade) | • **Fraqueza** explorável para executar ações ou obter acesso não autorizado a um sistema.<br>• Permite executar código, aceder à memória, instalar *malware* e roubar, destruir ou alterar dados sensíveis. | • **Zero-Days no Microsoft SharePoint On-Premise (2025 — Slide 48)**:<br>  - `CVE-2025-49704` (CVSS `8.8` — RCE)<br>  - `CVE-2025-49706` (CVSS `6.5` — *Server Spoofing*)<br>  - `CVE-2025-53771` (CVSS `6.5` — *Server Spoofing*)<br>  - **`CVE-2025-53770` (CVSS `9.8` — RCE Crítico)**: segundo a CrowdStrike, os ataques enviam um `HTTP POST` manipulado para `"/_layouts/15/ToolPane.aspx"` num SharePoint acessível para escrever **`spinstall0.aspx` via PowerShell**. |
| **Exposure** (Exposição) | • **Erro operacional** (ex.: má configuração) que permite acesso indevido a um sistema ou rede.<br>• Origem recorrente de fugas por **más configurações na *cloud***. | • **Caso `Apollo` (2018 — Slide 50)**: base de dados na *cloud* deixada **sem palavra-passe**, expondo **126 milhões de e-mails**, cargos, empregadores e telefones.<br>• **Caso `People Data Labs` (`PDL`, 2019 — Slide 50)**: os investigadores Bob Diachenko e Vinny Troia localizaram um servidor **Elasticsearch desprotegido** com **$4\text{ TB}$ de dados** e **$1.2\text{ mil milhões}$ de registos únicos** (incluindo $622\text{ milhões}$ de e-mails, telemóveis e perfis sociais). |

### 1.3. Catálogo de CVEs Famosas e Falhas Antigas Exploradas (Slides 51 e 55)

As falhas históricas de elevado impacto ([Help Net Security — Top Exploited](https://www.helpnetsecurity.com/2021/02/03/2020top-exploited-vulnerabilities/)) agrupam-se por superfície de infraestrutura:

| Categoria | Identificador CVE | Nome / Produto | Mecanismo e Impacto |
| :--- | :--- | :--- | :--- |
| **Windows & Active Directory** | **`CVE-2020-0796`** | **`SMBGhost`** | Execução remota de código (RCE) no protocolo SMBv3 do Windows 10/Server |
| | **`CVE-2020-1472`** | **`Zerologon`** | Falha criptográfica crítica (`AES-CFB8` com IV de zeros) no Netlogon para tomada de controlo do Domain Controller |
| | **`CVE-2020-0601`** | **`CurveBall`** | Falha de validação de certificados de curvas elípticas (ECC) no `Crypt32.dll` do Windows |
| | **`CVE-2020-16898`** | **`Bad Neighbor`** | RCE na pilha TCP/IP do Windows via pacotes ICMPv6 *Router Advertisement* |
| | **`CVE-2020-1350`** | **`SIGRed`** | RCE *wormable* no servidor **Windows DNS** |
| **Redes, VPNs & Firewalls** | **`CVE-2020-5902`** | **F5 BIG-IP** | RCE na interface de gestão TMUI |
| | **`CVE-2020-3452`** | **Cisco ASA / FTD** | Leitura arbitrária de ficheiros (*path traversal*) |
| **Servidores & SCADA/ICS** | **`CVE-2010-2772`** | **Siemens Simatic WinCC SCADA** | Palavra-passe *hardcoded* explorada pelo *worm* **Stuxnet** |
| | **`CVE-2020-14882`** | **Oracle WebLogic Server** | RCE sem autenticação na consola de administração |
| | **`CVE-2020-1938`** | **`GhostCat`** (**Apache Tomcat**) | Inclusão/leitura arbitrária de ficheiros no conector AJP |
| | **`CVE-2020-0688`** | **Microsoft Exchange Server** | Falha de validação de chave criptográfica (`viewstate`) |

* **Exploração persistente de CVEs antigas (FBI e CISA — Slide 55)**: relatórios conjuntos demonstram que muitas das falhas mais exploradas ativamente têm **vários anos de existência** — como Microsoft Office (**`CVE-2017-11882`**), Pulse Secure VPN (**`CVE-2019-11510`**), Citrix (**`CVE-2019-19781`**) e Fortinet — evidenciando atrasos crónicos na aplicação de *patches* ([Ars Technica — FBI/CISA Top 30](https://arstechnica.com/gadgets/2021/07/feds-list-the-top-30-most-exploited-vulnerabilities-many-are-years-old/)).

---

## 2. *Common Vulnerability Scoring System* (CVSS) e Bases de Dados (Slides 53–54)

### 2.1. Escala de Severidade (`0` a `10`) e *Vector String* (Slide 53)
O **CVSS** é um padrão aberto que avalia o impacto de uma vulnerabilidade e lhe atribui uma pontuação numérica de **`0` a `10`**:

| Nível de Severidade (*Severity*) | Intervalo (*Base Score*) |
| :--- | :---: |
| **`None`** (Nenhuma) | **`0.0`** |
| **`Low`** (Baixa) | **`0.1 – 3.9`** |
| **`Medium`** (Média) | **`4.0 – 6.9`** |
| **`High`** (Alta) | **`7.0 – 8.9`** |
| **`Critical`** (Crítica) | **`9.0 – 10.0`** |

Além do valor numérico (ex.: `8.1 HIGH`), o CVSS v3.x utiliza uma ***Vector String*** que codifica as métricas individuais (exemplo: `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H`):

| Métrica no Vetor | Significado no Exemplo |
| :--- | :--- |
| **`AV:N`** (*Attack Vector: Network*) | Explorável remotamente pela rede |
| **`AC:H`** (*Attack Complexity: High*) | Requer condições complexas para exploração bem-sucedida |
| **`PR:N`** (*Privileges Required: None*) | Não exige autenticação prévia |
| **`UI:N`** (*User Interaction: None*) | Não requer interação da vítima |
| **`S:U`** (*Scope: Unchanged*) | Impacto confinado ao componente vulnerável |
| **`C:H/I:H/A:H`** | Impacto **Alto** na Confidencialidade, Integridade e Disponibilidade |

### 2.2. Bases de Dados Públicas de CVE/CVSS (Slide 54)

1. **[CVE Details](https://www.cvedetails.com/)**: pesquisa filtrada por fabricante, produto, ano e distribuição de pontuações CVSS;
2. **[VulDB (*Vulnerability Database*)](https://vuldb.com/)**: base detalhada com inteligência de ameaças e contexto de exploração;
3. **[NVD (*National Vulnerability Database* — NIST)](https://nvd.nist.gov/)**: repositório oficial do governo dos EUA que enriquece os registos CVE com pontuações CVSS, vetores e mapeamentos CWE.

---

## 3. Top 10 CWE 2025 (*Common Weakness Enumeration* — Slide 56)

Enquanto um **CVE** designa uma falha específica num produto concreto, a **CWE** ([MITRE CWE Top 25 (2025)](https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html)) classifica a **categoria de fraqueza de software ou hardware** subjacente. O **Top 10 CWE de 2025** apresentado na aula é:

| Rank | Identificador CWE | Nome da Fraqueza (*Weakness*) | Pontuação |
| :---: | :---: | :--- | :---: |
| **1** | **`CWE-79`** | *Improper Neutralization of Input During Web Page Generation (**'Cross-site Scripting' — XSS**)* | `60.39` |
| **2** | **`CWE-89`** | *Improper Neutralization of Special Elements used in an SQL Command (**'SQL Injection' — SQLi**)* | `28.72` |
| **3** | **`CWE-352`** | ***Cross-Site Request Forgery (CSRF)*** | `19.65` |
| **4** | **`CWE-862`** | ***Missing Authorization*** (Falta de verificação de autorização) | `18.01` |
| **5** | **`CWE-787`** | ***Out-of-bounds Write*** (Escrita fora dos limites do *buffer*) | `15.61` |
| **6** | **`CWE-22`** | *Improper Limitation of a Pathname to a Restricted Directory (**'Path Traversal'**)* | `14.11` |
| **7** | **`CWE-416`** | ***Use After Free*** (Referência a memória dinâmica após libertação) | `11.53` |
| **8** | **`CWE-125`** | ***Out-of-bounds Read*** (Leitura fora dos limites do *buffer*) | `9.61` |
| **9** | **`CWE-78`** | *Improper Neutralization of Special Elements used in an OS Command (**'OS Command Injection'**)* | `9.53` |
| **10** | **`CWE-94`** | *Improper Control of Generation of Code (**'Code Injection'**)* | `8.29` |

---

## Além da aula

* **CVEs Estudadas Noutras Partes de `ASSI`**: A análise de exploração e vestígios forenses noutras notas da UC incide sobre casos concretos como `CVE-2016-5247` em [[PKfail - Vulnerabilidade do UEFI Secure Boot]], `CVE-2010-2568` (atalho `.LNK` no *Stuxnet*) em [[Vetores de Ataque USB (BadUSB, Rubber Ducky, LNK, USB-Killer) e Defesas (GPO, Pad Jack, ESD Dogs)]] e [[Abuso e Vetores de Ataque com Ficheiros LNK]], e `CVE-2026-45585` (*BitLocker's YellowKey*) em [[System e OS Hardening e Vulnerabilidade BitLocker YellowKey (CVE-2026-45585)]].
* **Deteção de *Webshells* (`spinstall0.aspx`) em Triagem (`ASSI` Cap. 3)**: No ataque Zero-Day ao SharePoint On-Premise (`CVE-2025-53770`), a criação da *webshell* `spinstall0.aspx` via PowerShell a partir de `/_layouts/15/ToolPane.aspx` constitui um indicador de comprometimento detetável em resposta a incidentes com os scanners [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração|LOKI]] e [[Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI|Loki-RS]] baseados em regras [[YARA - Introdução, Estrutura de Regras, Metadados e Condições|YARA]].

---

## Perguntas de revisão

1. **Em que ano e por que organização foi criado o sistema CVE, qual é o formato padrão de um identificador e que papel desempenha o protocolo SCAP?**

> [!success]- Ver Resposta
> O sistema CVE foi lançado em **1999 pela MITRE** (organização sem fins lucrativos). Cada falha recebe um identificador padrão no formato **`CVE-YYYY-NNNNN`** (ano + número sequencial). O protocolo **SCAP (*Security Content Automation Protocol*)** é utilizado para recolher, avaliar e atribuir um identificador único às vulnerabilidades catalogadas (em conjunto com o *Assigning CNA*).

2. **Distinga *Vulnerability* de *Exposure*, apresentando os exemplos do SharePoint On-Premise (2025) e dos casos *Apollo* e *People Data Labs*.**

> [!success]- Ver Resposta
> Uma **Vulnerability** é uma fraqueza no software/sistema explorável para executar ações não autorizadas — como os Zero-Days de 2025 no SharePoint On-Premise (`CVE-2025-49704` CVSS `8.8`, `CVE-2025-49706` e `CVE-2025-53771` CVSS `6.5`, e **`CVE-2025-53770` CVSS `9.8`** via `/_layouts/15/ToolPane.aspx` para gravar `spinstall0.aspx`). Uma **Exposure** é um erro de configuração que abre acesso a sistemas/dados — como a base de dados **Apollo** (2018, sem password, 126M de e-mails) e o servidor Elasticsearch aberto da **People Data Labs** (2019, 4 TB / 1.2 mil milhões de registos únicos).

3. **Quais são os cinco níveis de severidade e respetivos intervalos numéricos do CVSS e quais são as três principais bases de dados públicas para consulta?**

> [!success]- Ver Resposta
> Os intervalos CVSS (`0` a `10`) são: **None** (`0.0`), **Low** (`0.1–3.9`), **Medium** (`4.0–6.9`), **High** (`7.0–8.9`) e **Critical** (`9.0–10.0`). As três principais bases de dados são **CVE Details** (`cvedetails.com`), **VulDB** (`vuldb.com`) e **NVD** (`nvd.nist.gov`).

4. **O que distingue a CWE do CVE e quais são as cinco principais fraquezas do Top 10 CWE de 2025?**

> [!success]- Ver Resposta
> Enquanto o **CVE** identifica uma ocorrência específica de falha num produto concreto, a **CWE** categoriza o tipo de fraqueza de software/hardware subjacente. As cinco primeiras posições do Top 10 CWE de 2025 são: **1. `CWE-79`** (*Cross-site Scripting — XSS*, `60.39`), **2. `CWE-89`** (*SQL Injection*, `28.72`), **3. `CWE-352`** (*CSRF*, `19.65`), **4. `CWE-862`** (*Missing Authorization*, `18.01`) e **5. `CWE-787`** (*Out-of-bounds Write*, `15.61`).

---

## Notas relacionadas

- [[Capítulo 2 - Administração de Sistemas]]
- [[System e OS Hardening e Vulnerabilidade BitLocker YellowKey (CVE-2026-45585)]]
- [[Licenciamento de Software, Fugas em Partilha de Dados (SAS Tokens) e Falhas de Redação]]
- [[Vetores de Ataque USB (BadUSB, Rubber Ducky, LNK, USB-Killer) e Defesas (GPO, Pad Jack, ESD Dogs)]]
- [[PKfail - Vulnerabilidade do UEFI Secure Boot]]
- [[Scanner de IOCs LOKI (Versão Python) - Métodos de Deteção e Configuração]]
- [[Loki-RS (Versão Rust) - Compilação, Atualização e Parâmetros CLI]]
