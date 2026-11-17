---
title: Vetores de Ataque USB (BadUSB, Rubber Ducky, LNK, USB-Killer) e Defesas (GPO, Pad Jack, ESD Dogs)
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 2
fonte_aula: System Administration - System and Data Management.pdf
tags:
  - assi
  - administracao-sistemas
  - usb
  - badusb
  - rubber-ducky
  - usb-killer
  - raspberry-robin
  - gpedit
  - pad-jack
  - esd-dogs
aliases:
  - Tipos de Ataques USB
  - BadUSB
  - USB Rubber Ducky
  - USB-Killer
  - Raspberry Robin
  - USB Pad Jack
  - ESD Dogs
atualizado: 2026-11-11
---

# Vetores de Ataque USB (BadUSB, Rubber Ducky, LNK, USB-Killer) e Defesas (GPO, Pad Jack, ESD Dogs)

Os ataques USB abrangem **Rubber Ducky**, **BadUSB**, abuso de protocolos (`.LNK` no **Stuxnet** e **Raspberry Robin**), **USB-Killer** e *drop attacks*, defendidos com **GPO**, **Pad Jack** e **ESD dogs**.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: O protocolo USB confia nos descritores de classe (`HID`, `Mass Storage`, interface de rede) declarados pelo próprio dispositivo durante a enumeração, enquanto o sistema operativo processa automaticamente ficheiros de atalho e metadados ao abrir uma unidade montada.
> * **Porque importa (Segurança / Forense)**: Esta confiança permite contornar defesas de perímetro e isolamento de rede — desde injeção de comandos PowerShell via teclado emulado (**FIN7 / BadUSB**) até propagação via lojas de fotocópias (**`Raspberry Robin`**). Forensicamente, ataques `HID` deixam rastos em `RunMRU`, `Prefetch` e registos de teclado (`VID/PID`) em vez de chaves clássicas `USBSTOR` de armazenamento.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Categoria A (`USB Rubber Ducky`) vs. B (`BadUSB`)**: A reprograma o **microcontrolador interno** para emular teclado HID; B reprograma o **firmware do controlador USB** (incluindo criação de **partição oculta**);
>   * **Limitação `gpedit.msc`**: o Editor de Política de Grupo Local **não existe nativamente nas edições `Home`** do Windows 10 e Windows 11;
>   * **`USB Pad Jack`**: bloqueio físico *tamper-evident* (deixa marca visível e tem número de série) disponível em **`Multi-lock`** (cabo de aço cortável) e **`Single-lock`** (obriga a partir o bloqueador);
>   * **`ESD dogs`**: cães treinados para detetar o composto químico **TPPO (*triphenylphosphine oxide*)** em chips de memória flash escondidos.

---

## 1. Taxonomia dos Ataques Baseados em USB (Nissim et al., 2017 — Slide 31)

Com base na classificação de **Nissim, N., Yahalom, R., & Elovici, Y. (2017)** (*"USB-based attacks"*, *Computers & Security*, 70, 675–688, `doi:10.1016/j.cose.2017.08.002`), distinguem-se **quatro categorias técnicas principais** e um vetor comportamental adicional:

| Categoria | Mecanismo Técnico                                                     | Exemplos e Impacto Operacional                                                                                                                                                                                                                                           |
| :-------: | :-------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  **A)**   | **Reprogramação do microcontrolador interno**                         | • O dispositivo aparenta ser um periférico comum (ex.: pen USB ou carregador), mas opera como outro dispositivo — tipicamente um **teclado HID (*Human Interface Device*) que injeta sequências rápidas de teclas**.<br>• Exemplo clássico: **`USB Rubber Ducky`**.      |
|  **B)**   | **Reprogramação do firmware do dispositivo (`BadUSB`)**               | • Altera o firmware do controlador USB para:<br>  1. Executar ações maliciosas autónomas (descarregamento de *malware*, exfiltração ou alteração de DNS/rede);<br>  2. **Criar uma partição oculta (*hidden partition*)** para exfiltrar dados de forma invisível.       |
|  **C)**   | **Exploração de falhas na interação do SO com protocolos/normas USB** | • **Execução de código arbitrário via atalho `.LNK` manipulado (`CVE-2010-2568`, usado pelo *worm* `Stuxnet`)**;<br>• Exploits de execução automática (**`AutoRun` / `AutoPlay`**);<br>• Ataques a smartphones através de carregadores USB maliciosos (*Juice Jacking*). |
|  **D)**   | **Ataques elétricos baseados em USB**                                 | • **`USB-Killer`**: acumula energia da porta USB em condensadores internos e descarrega picos de alta tensão pelas linhas de dados/alimentação, destruindo fisicamente a *motherboard*.                                                                                  |
| **BÓNUS** | ***USB Drop Attacks* (*"Road Apples"*)**                              | • Abandono intencional de uma pen USB infetada (ex.: parque de estacionamento ou receção) explorando a curiosidade humana para que seja ligada a um PC interno.                                                                                                          |

---

## 2. Casos Reais: Campanha Postal *FIN7* (`BadUSB`) e `Raspberry Robin` (Slides 32–33)

### 2.1. Engenharia Social Postal + `BadUSB` — Grupo *FIN7* (Slide 32)

* **Vetor combinado** ([Alerta FBI / Campanha FIN7](https://bit.ly/2wC9mwq)): o grupo cibercriminoso **FIN7** enviou encomendas pelo correio postal (USPS) a empresas de retalho, restauração e hotelaria contendo ursos de peluche, vales de oferta falsos da Best Buy e uma pen **`BadUSB`**;
* **Execução**: quando o destinatário ligava a pen ao PC, esta emulava um teclado HID, abria a janela *Executar* (`Win+R`) e injetava comandos **PowerShell** para descarregar e executar em memória a *backdoor* JScript **`GRIFFON`** e o *malware* **`Bateleur`**.

### 2.2. *Malware* `Raspberry Robin` e Lojas de Impressão/Fotocópias (Slide 33)

* **Infeção inicial**: nos incidentes do *worm/trojan* **`Raspberry Robin`**, o utilizador clica num ficheiro de **atalho malicioso (`.LNK`)** existente na pen USB após ligá-la ao computador, desencadeando execuções encadeadas (`msiexec.exe` / `odbcconf.exe` / `cmd.exe`) para contacto com infraestrutura de comando e controlo;
* **Origem da propagação (*Deutsche Telekom CERT*)**: a análise do CERT da Deutsche Telekom identificou um ponto comum surpreendente — **todos os utilizadores afetados tinham utilizado previamente a pen USB em lojas de impressão/fotocópias** ([BushidoToken — Raspberry Robin](https://blog.bushidotoken.net/2023/05/raspberry-robin-global-usb-malware.html); [Reddit — Relato Técnico](https://www.reddit.com/r/techsupport/comments/zam23c/raspberry_robin_trojan_on_usb/));
* **Agravante**: várias impressoras e quiosques dessas lojas encontravam-se **diretamente acessíveis a partir da Internet**, atuando como vetores persistentes de infeção para todas as pens USB de clientes.

---

## 3. Defesas Lógicas (`gpedit.msc`), Físicas (`Pad Jack`) e Deteção K9 (`ESD Dogs`) (Slides 35–37)

### 3.1. Proteção Lógica via Group Policy no Windows 10/11 (Slide 35)

* **Consola**: **`gpedit.msc`** (*Local Group Policy Editor*);
* **Caminho**: `Computer Configuration` (ou `User Configuration`) $\to$ `Administrative Templates` $\to$ `System` $\to$ **`Removable Storage Access`**;
* **Políticas principais**: `Removable Disks: Deny execute access`, `Removable Disks: Deny read access`, `Removable Disks: Deny write access` e **`All Removable Storage classes: Deny all access`** (*Enabled*).
* **Armadilha de exame**: o **`gpedit.msc` NÃO está disponível por omissão nas edições `Home`** do Windows 10 e Windows 11 (apenas nas edições *Pro*, *Enterprise* e *Education*).

### 3.2. Proteção Física de Portas USB — `USB Pad Jack` (Slide 36)

* O **`Pad Jack`** é um bloqueador físico inserido diretamente na porta USB para impedir a ligação de periféricos ([NovaVision — Pad Jack](https://www.novavisioninc.com/pages/prd_padjack_computer_seals.html));
* **Evidência de violação (*Tamper-evident*)**: possui número de série único gravado e **não pode ser removido sem deixar vestígio físico visível**;
* **Variantes**:
  1. **`Multi-lock`**: bloqueia múltiplas portas adjacentes através de um cabo de aço (*wire lock*) que **tem de ser cortado** para libertar as portas;
  2. **`Single-lock`**: sela uma porta individual e **exige partir fisicamente o dispositivo** para o remover.

### 3.3. Procura Forense de Armazenamento Oculto — `ESD Dogs` (Slide 37)

* **Caso real — *Mt. Diablo School District* (Califórnia)**: um estudante detido por invadir os sistemas do distrito escolar para alterar notas (14 acusações criminais) ocultou uma pen USB numa **caixa de lenços de papel**. Durante a busca domiciliária, a unidade K9 (**`@CoCoSheriff`**) farejou e localizou o dispositivo ([Artigo — Caso Mt. Diablo](https://tek.io/2KoASPc));
* **Base técnica**: os **`ESD dogs` (*Electronic Storage Detection dogs*)** são cães treinados para detetar o composto químico **TPPO (*triphenylphosphine oxide*)**, utilizado no revestimento térmico de circuitos eletrónicos e chips de memória flash (pens USB, cartões MicroSD, SSDs e telemóveis).

---

## Além da aula

* **Abuso de Ficheiros `.LNK` no `Stuxnet` e no `Raspberry Robin` (`ASSI` Cap. 1 Bloco 12)**: O vetor de Categoria C articula-se diretamente com a estrutura binária `[MS-SHLLINK]` estudada em [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário]] e com as técnicas de abuso de argumentos e *LOLBins* detalhadas em [[Abuso e Vetores de Ataque com Ficheiros LNK]].
* **Investigação Forense de Dispositivos USB e `BadUSB` (`ASSI` Cap. 1 Bloco 08)**: Enquanto unidades de massa deixam rasto em `HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR` ([[Artefactos Forenses de Dispositivos USB]]), ataques `USB Rubber Ducky` ou `BadUSB` em modo teclado registam-se como dispositivos `HID` e deixam vestígios de comandos em `RunMRU` ([[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)]]) e artefactos de execução ([[Serviço Prefetch e SysMain - Arquitetura e Funcionamento]], [[Application Compatibility e ShimCache (AppCompatCache)]] e [[AmCache - Arquitetura, Hives e Evolução para SQLite]]).

---

## Perguntas de revisão

1. **Quais são as quatro categorias principais de ataques USB segundo Nissim et al. (2017) e o que distingue a Categoria A (`USB Rubber Ducky`) da Categoria B (`BadUSB`)?**

> [!success]- Ver Resposta
> As categorias são: **A)** reprogramação do microcontrolador interno (`USB Rubber Ducky`, emulando teclado HID para injetar teclas); **B)** reprogramação do firmware do dispositivo (`BadUSB`, executando ações maliciosas e podendo criar **partições ocultas**); **C)** exploração de falhas na interação do SO com protocolos USB (atalhos `.LNK` `CVE-2010-2568`, `AutoRun`/`AutoPlay`, *Juice Jacking*); e **D)** ataques elétricos (`USB-Killer`). Além destas, existe o vetor bónus de *USB Drop attacks*.

2. **Como atuaram os ataques reais do grupo *FIN7* via correio postal e do *malware* `Raspberry Robin`?**

> [!success]- Ver Resposta
> O grupo **FIN7** enviou pacotes postais com ursos de peluche, cartões-presente falsos e pens `BadUSB` que, ao serem ligadas, emulavam um teclado, abriam `Win+R` e injetavam PowerShell para descarregar a *backdoor* `GRIFFON` e o *malware* `Bateleur`. Já o **`Raspberry Robin`** infeta o utilizador quando este clica num atalho `.LNK` malicioso na pen USB; o *Deutsche Telekom CERT* verificou que as pens tinham sido contaminadas em lojas de impressão/fotocópias cujas impressoras estavam expostas à Internet.

3. **Como se bloqueia o acesso USB via `gpedit.msc` no Windows 10/11, qual é a limitação das edições *Home* e como funcionam os bloqueadores `USB Pad Jack`?**

> [!success]- Ver Resposta
> No `gpedit.msc`, navega-se até `Computer Configuration` (ou `User Configuration`) $\to$ `Administrative Templates` $\to$ `System` $\to$ `Removable Storage Access` (ex.: `All Removable Storage classes: Deny all access`), mas a consola **`gpedit.msc` não existe nas edições *Home***. Fisicamente, o `USB Pad Jack` sela a porta USB com evidência de violação (*tamper-evident*, com número de série), existindo em versão **`Multi-lock`** (cabo de aço que tem de ser cortado) e **`Single-lock`** (exige partir o dispositivo para remoção).

4. **O que são `ESD dogs`, que composto químico detetam e que caso real ilustra a sua utilização?**

> [!success]- Ver Resposta
> Os **`ESD dogs` (*Electronic Storage Detection dogs*)** são cães polícia treinados para detetar o composto químico **TPPO (*triphenylphosphine oxide*)** presente no revestimento de chips de memória flash e placas eletrónicas. No caso do *Mt. Diablo School District*, a unidade K9 `@CoCoSheriff` encontrou uma pen USB escondida dentro de uma caixa de lenços de papel durante uma busca domiciliária.

---

## Notas relacionadas

- [[Capítulo 2 - Administração de Sistemas]]
- [[Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)]]
- [[Pen Drives USB Falsas e Verificação com ValiDrive (Ficha 11)]]
- [[Educação de Utilizadores, Phishing, Spear-Phishing e Reforço Positivo]]
- [[Artefactos Forenses de Dispositivos USB]]
- [[Abuso e Vetores de Ataque com Ficheiros LNK]]
- [[Ficheiros LNK (Shell Links) - Metadados e Formato Binário]]
- [[Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB]]
