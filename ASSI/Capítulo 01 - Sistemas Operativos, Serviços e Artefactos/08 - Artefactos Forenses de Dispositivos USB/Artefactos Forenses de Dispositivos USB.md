---
title: Artefactos Forenses de Dispositivos USB
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 8
tipo: conceito
tags:
  - assi
  - windows
  - registry
  - usb
  - usbstor
  - setupapi
  - wleapp
  - forense
aliases:
  - USB Forensics
  - USBSTOR
  - setupapi.dev.log
  - USBDeview
  - WLEAPP
  - Serial Number vs Device ID
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "http://www.nirsoft.net/utils/usb_devices_view.html"
  - "https://sourceforge.net/projects/usboblivion/"
  - "https://github.com/abrignoni/WLEAPP"
  - "https://www.computerpi.com/the-truth-about-usb-device-serial-numbers-and-the-lies-your-tools-tell/"
atualizado: 2026-10-16
---

# Artefactos Forenses de Dispositivos USB

Rastreio pericial de dispositivos de armazenamento amovível no Windows através da chave `USBSTOR` (`SYSTEM`), do ficheiro de registo de controladores `setupapi.dev.log` e da validação de números de série de hardware vs. IDs gerados pelo sistema.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Quando um suporte USB de armazenamento em massa é inserido, o gestor *Plug-and-Play* (PnP) do Windows precisa de identificar o fabricante/modelo e a instância do dispositivo para carregar os controladores de disco (`USBSTOR` no hive `SYSTEM`) e registar o diagnóstico do processo de instalação do driver em `C:\Windows\INF\setupapi.dev.log`.
> * **Porque importa (Forense)**: É a diligência prioritária para provar **exfiltração de dados**, infeção por *malware* via suporte físico ou posse de ficheiros ilícitos em dispositivos externos, guiando as equipas de busca e apreensão no terreno.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Regra do `&` no 2.º Caractere (`Serial Number` vs. `Windows Assigned Device ID`)**: Se o identificador da instância debaixo de `USBSTOR` tiver um **`&` na segunda posição** (ex.: `7&19a58b0&0`), a pen **não tem número de série de fábrica** e esse ID foi gerado localmente pelo Windows (mudando se a pen for ligada noutro PC!). Além disso, mesmo sem `&` na 2.ª posição, o `pnpdeviceID` pode divergir do `serialnumber` real do chip (validar via WMI/PowerShell).
>   * **Limitação do `WLEAPP` no `setupapi.dev.log`**: O `setupapi.dev.log` prova a **1.ª conexão física** do dispositivo, mas quando enche é rodado para ficheiros datados (`setupapi.dev.YYYYMMDD_HHMMSS.log`). O módulo do `WLEAPP` processa apenas o ficheiro ativo `setupapi.dev.log`, ignorando os ficheiros históricos rodados!

---

## Prioridade Pericial em Busca e Apreensão

> [!IMPORTANT] Diligência Imediata no Local da Busca
> Em qualquer exame pericial, o investigador deve responder de imediato a duas perguntas críticas:
> 1. **Estiveram dispositivos de armazenamento USB ligados à máquina em análise?**
> 2. **Se sim, esses suportes físicos já foram localizados e apreendidos na busca?**
> Dispositivos USB têm dimensões reduzidas e correm risco extremo de ocultação ou destruição pelo suspeito — justificando o emprego de cães detetores de suportes eletrónicos (*ESD dogs*) e a inspeção de esconderijos improvisados (ex.: caso real de 2026 em Espanha, onde a polícia apreendeu pens USB com *cold wallets* de criptoativos dissimuladas dentro de um termómetro de parede).

---

## Mapa Rápido: "O que procuro sobre o USB?" $\rightarrow$ "Artefacto e Localização"

> [!TIP] Esquema Interativo de Correlação USB (4 Hives)
> Para visualizar passo a passo como cruzar `USBSTOR` $\rightarrow$ `MountedDevices` $\rightarrow$ `EMDMgmt` $\rightarrow$ `NTUSER.DAT\MountPoints2`, abre [assi_registry_forense.html](../../../_assets/assi_registry_forense.html) (separador **2. Correlação USB**).

| Pergunta do Investigador | Artefacto / Ferramenta | Caminho Físico / Comando | Limitação / Cuidado Forense |
| :--- | :--- | :--- | :--- |
| **Que marcas, modelos e números de série** de pens/discos USB foram ligados? | Chave **`USBSTOR`** (Hive `SYSTEM`) | `HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR` | Verificar se o ID da instância tem `&` no 2.º caractere (ID local gerado pelo Windows vs. Serial de fábrica). |
| **Quando ocorreu a 1.ª inserção física** do dispositivo na máquina? | Ficheiro **`setupapi.dev.log`** | `C:\Windows\INF\setupapi.dev.log` (e `setupapi.dev.*.log`) | Inspecionar também os ficheiros de log rodados (`setupapi.dev.<data>.log`); o `WLEAPP` só lê o ficheiro principal! |
| **O `pnpdeviceID` do Registry coincide com o `SerialNumber`** real do chip USB? | Consulta **WMI / PowerShell** (*Live*) | `gwmi win32_diskdrive \| ? {$_.interfacetype -eq 'USB'} \| Select-Object model, pnpdeviceID, serialnumber` | Certas pontes/controladores USB reportam valores distintos entre o `pnpdeviceID` e o `serialnumber` de hardware. |
| **Houve tentativa deliberada de apagar** os registos USB? | Deteção de **`USBOblivion`** | Cruzamento entre `USBSTOR`, `MountedDevices`, `setupapi.dev.log` e logs NTFS/`UserAssist` | O `USBOblivion` limpa `USBSTOR`, `MountedDevices` e `setupapi.dev.log`, deixando inconsistências noutros artefactos (como `ShellBags` ou `.lnk`). |

---

## 1. A Chave `USBSTOR` no Registry (`SYSTEM`)

Sempre que um dispositivo USB de armazenamento em massa (*Mass Storage*) é conectado ao Windows, o sistema cria registos persistentes no hive `SYSTEM`:

```text
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USBSTOR
```

(Em análise *offline* do ficheiro `SYSTEM`, consulta-se `ControlSet001\Enum\USBSTOR` verificando em `Select\Current` qual o `ControlSet` ativo).

### Anatomia da Nomenclatura das Subchaves de `USBSTOR`

**1. 1.º Nível (Fabricante, Produto e Revisão):**

```text
Disk&Ven_<Fabricante>&Prod_<Produto>&Rev_<Revisao>
```

* *Exemplo*: `Disk&Ven_Kingston&Prod_DataTraveler_3.0&Rev_PMAP`

**2. 2.º Nível (Identificador de Instância / Número de Série):**

* Subchave que identifica a unidade física específica, terminando habitualmente no sufixo de número de unidade lógica (`&0`).

---

## 2. Número de Série Real vs. *Windows Assigned Device ID*

> [!CAUTION] Armadilha Clássica de Exame e Perícia
> **Nem todos os dispositivos USB possuem número de série único gravado de fábrica, e nem sempre a string registada em `USBSTOR` corresponde ao verdadeiro número de série físico do hardware.**

| Tipo de Identificador em `USBSTOR` | Regra Visual de Identificação | Exemplo Prático | Comportamento entre Computadores Diferentes |
| :--- | :--- | :---: | :--- |
| **Número de Série reportado pelo Descritor USB (`iSerialNumber`)** | Sequência alfanumérica contínua **SEM o carácter `&` na 2.ª posição** (o `&0` surge apenas no fim para indicar o LUN 0). | `0707268153443174&0` | **Mantém-se constante** quando a mesma pen USB é inserida noutros computadores. |
| **Windows Assigned Device ID (ID Gerado pelo Windows)** | Possui um carácter **`&` na 2.ª posição** da string. | **`7&19a58b0&0`** | Gerado internamente pelo Windows com base na porta/topologia do barramento local porque a pen não tem `iSerialNumber`. **Muda se a pen for ligada noutro PC** (não permite correlacionar entre máquinas distintas!). |
| **Divergência `pnpdeviceID` vs. `SerialNumber` de Hardware** | Não tem `&` na 2.ª posição em `USBSTOR`, mas a ponte USB reporta um ID diferente do chip. | `pnpdeviceID`: `00045F057BD8BDC1D9C90033&0` vs. `serialnumber`: `0B0D0C415DF9` | Em sistema vivo, deve validar-se ambos os campos via **WMI/PowerShell** para evitar falhas de correspondência com o suporte apreendido. |

### Anatomia da Auditoria em PowerShell (Sistema Vivo)

```powershell
# 1. Listar todas as unidades de disco cujo barramento de interface seja USB
gwmi win32_diskdrive | ? {$_.interfacetype -eq 'USB'}

# 2. Exibir lado a lado o Modelo, o PNPDeviceID (que vai para o USBSTOR) e o SerialNumber real
gwmi win32_diskdrive | ? {$_.interfacetype -eq 'USB'} | Select-Object model, pnpdeviceID, serialnumber
```

* **`gwmi win32_diskdrive`**: (*Get-WmiObject*) interroga a classe WMI `Win32_DiskDrive` que representa os discos físicos ligados ao sistema.
* **`| ? {$_.interfacetype -eq 'USB'}`**: filtra (`Where-Object`) apenas os dispositivos cuja interface seja `USB`.
* **`| Select-Object model, pnpdeviceID, serialnumber`**: projeta os três atributos críticos, permitindo detetar imediatamente se o identificador usado em `USBSTOR` (`pnpdeviceID`) coincide ou diverge do `serialnumber` real do dispositivo.

---

## 3. O Ficheiro de Log `setupapi.dev.log` (1.ª Conexão Física)

Para apurar a **data e hora exata da primeira inserção física** do periférico USB no computador, o perito analisa o ficheiro de texto de instalação de controladores *Plug-and-Play*:

```text
C:\Windows\INF\setupapi.dev.log
```

Quando o dispositivo USB é inserido pela primeira vez, o Windows cria uma secção documentando o identificador do dispositivo e o carimbo temporal (`Section start`) na hora local do sistema:

```text
>>>  [Device Install (Hardware initiated) - SWD\WPDBUSENUM\_??_USBSTOR#Disk&Ven_Lexar...#{53f56307-b6bf...}]
>>>  Section start 2024/01/21 02:06:40.028
```

* **Atenção aos Ficheiros Históricos Rodados**: Quando o ficheiro `setupapi.dev.log` atinge o limite de tamanho, o Windows renomeia-o anexando a data/hora (ex.: **`setupapi.dev.20240315_174449.log`**) e inicia um novo `setupapi.dev.log`. O perito tem obrigatoriamente de recolher e analisar todos os ficheiros `setupapi.dev*.log` presentes em `C:\Windows\INF\`.

---

## 4. Ferramentas de Análise e Anti-Forense

### 1. `USBDeview` (NirSoft)
Utilitário gráfico e de linha de comandos para inventariação de dispositivos USB conectados e históricos (lendo o Registry):

* Lista nome, descrição, tipo de dispositivo, número de série, letra de unidade atribuída (`Drive Letter`), data de primeiro encaixe e data da última conexão/desconexão.

**Anatomia da Exportação via CLI** (binário `USBDeview.exe`, referenciado nos exemplos de aula como `usbview.exe`):

```cmd
usbview.exe /shtml list.html
usbview.exe /sxml list.xml
```

* `/shtml <ficheiro>`: exporta o inventário completo de dispositivos USB para uma tabela HTML formatada.
* `/sxml <ficheiro>`: exporta o inventário em formato estruturado XML.

### 2. `WLEAPP` (Alexis Brignoni) e a sua Limitação Pericial

* **Windows Logs, Events, and Properties Parser**: framework open-source em Python 3 orientada para triagem automatizada de artefactos Windows (**Nota**: projeto **descontinuado em 2026 e removido do GitHub**, mantendo-se como referência metodológica de aula).
* Inclui um módulo dedicado que extrai do `setupapi.dev.log` o nome do dispositivo e a hora exata da **primeira conexão (*First Connection Time*)** em relatórios HTML e TSV.
* **Limitação Pericial Crítica**: O módulo do `WLEAPP` processa exclusivamente o ficheiro principal `setupapi.dev.log`, **ignorando os ficheiros históricos rodados (`setupapi.dev.<data>.log`)**, que têm de ser inspecionados diretamente pelo perito.

### 3. Utilitário Anti-Forense: `USBOblivion`

* Ferramenta desenhada especificamente para apagar vestígios de conexões USB num sistema Windows.
* **O que apaga**: elimina do Registry todas as entradas nas chaves `USBSTOR`, `USB`, `MountedDevices` e limpa entradas do `setupapi.dev.log`.
* **Como detetar**: a presença do próprio executável no `UserAssist`/`MuiCache`/`Prefetch` ou a descoberta de caminhos e atalhos para letras de unidades amovíveis em [[Artefacto Forense ShellBags|ShellBags]], `RecentDocs` e ficheiros `.lnk` sem a correspondente entrada em `USBSTOR` constitui forte evidência de eliminação intencional de provas.

---

## Perguntas de revisão

1. **Ao inspecionar a chave `HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR`, o perito encontra duas pens USB: a primeira tem a subchave de instância `0707268153443174&0` e a segunda tem a subchave `7&19a58b0&0`. Qual a diferença fundamental entre estes dois identificadores e que impacto tem na comparação com uma pen apreendida noutro computador?**

> [!success]- Ver Resposta
> A regra reside na presença do carácter **`&` na segunda posição**. O identificador `0707268153443174&0` não tem `&` na 2.ª posição (apenas o sufixo final `&0` da unidade lógica), tratando-se de um **número de série reportado pelo hardware** que se mantém constante em qualquer computador onde a pen seja ligada. Já `7&19a58b0&0` possui um **`&` na 2.ª posição**, o que significa que a pen não forneceu número de série de fábrica e o Windows gerou um **Windows Assigned Device ID** local baseado na topologia do barramento; se essa mesma pen for ligada noutro PC, receberá um ID diferente.

2. **Mesmo quando o identificador em `USBSTOR` não apresenta um `&` na segunda posição, que precaução adicional deve o perito tomar num sistema vivo usando PowerShell e porquê?**

> [!success]- Ver Resposta
> O perito deve executar o comando `gwmi win32_diskdrive | ? {$_.interfacetype -eq 'USB'} | Select-Object model, pnpdeviceID, serialnumber` porque certos controladores e pontes USB reportam no `pnpdeviceID` (que alimenta a chave `USBSTOR`) um identificador diferente do verdadeiro `serialnumber` gravado no chip de memória do suporte.

3. **Em que ficheiro do sistema operativo fica registada a data e hora exata da primeira conexão física de um dispositivo USB e qual é a limitação crítica da ferramenta `WLEAPP` ao analisar este artefacto?**

> [!success]- Ver Resposta
> A primeira conexão física fica registada no ficheiro `C:\Windows\INF\setupapi.dev.log` (na linha `Section start YYYY/MM/DD HH:MM:SS.mmm`). A limitação crítica do `WLEAPP` (além de ter sido descontinuado em 2026) é que o seu parser analisa apenas o ficheiro ativo `setupapi.dev.log`, **não processando os ficheiros históricos rodados** (`setupapi.dev.<data_hora>.log`) que se encontram na mesma pasta.

4. **O que faz a ferramenta anti-forense `USBOblivion` e como pode um perito descobrir que uma pen USB esteve ligada à máquina mesmo após a execução dessa ferramenta?**

> [!success]- Ver Resposta
> O `USBOblivion` apaga os registos de dispositivos USB nas chaves `USBSTOR`, `USB` e `MountedDevices` do hive `SYSTEM` e limpa o ficheiro `setupapi.dev.log`. O perito pode detetar a manobra anti-forense encontrando rasto da execução do próprio `USBOblivion` (em `UserAssist`, `MuiCache` ou `Prefetch`) e detetando inconsistências como pastas e ficheiros acedidos em unidades externas que permanecem gravados nos hives do utilizador (**ShellBags** em `USRCLASS.DAT`, `RecentDocs`, `ComDlg32` e atalhos `.lnk`).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Artefacto Forense ShellBags]] | `Bloco 07` |
| **Seguinte** | [[LastActivityView e Reconstituição Temporal Live]] | `muda para Bloco 09` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 08` |

### Conceitos Relacionados

* [[Salvaguarda e Monitorização do Registry]] · `Bloco 06`
* [[Estrutura e Hives do Windows Registry]] · `Bloco 05`
* [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]] · `Comum/`
* [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]] · `AFD1 · Cap. 1`
* [[Exercício de Projeto - Catalogação e Etiquetagem de Dispositivos e Serviços]] · `AFD1 · Cap. 1`
* [[Fases da Investigação Forense Digital]] · `AFD1 · Cap. 1`
