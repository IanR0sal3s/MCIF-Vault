---
title: Artefactos Forenses de Dispositivos USB
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
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
atualizado: 2026-09-23
---

# Artefactos Forenses de Dispositivos USB

Em perícia informática, apurar a ligação de dispositivos de armazenamento amovível (pens USB, cartões SD, discos externos) é uma das diligências prioritárias de uma investigação. Permite aferir se houve **exfiltração de dados**, introdução de **malware** ou armazenamento externo de provas ilícitas.

> [!IMPORTANT] Prioridade Pericial e Apreensão
> 1. Deve determinar-se o mais rapidamente possível: **estiveram dispositivos USB ligados à máquina em análise?**
> 2. Se sim: **esses suportes físicos foram apreendidos na busca?**
> Suportes USB não apreendidos de imediato correm elevado risco de ser destruídos ou ocultados pelo suspeito (daí o recurso a cães detetores de suportes eletrónicos — *ESD dogs*).

---

## A Chave `USBSTOR` no Registry

Sempre que um dispositivo USB de armazenamento em massa é conectado pela primeira vez ao Windows, o sistema operativo cria registos persistentes sob a chave:

```text
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Enum\USBSTOR
```

(Ou `ControlSet001\Enum\USBSTOR`).

### Nomenclatura das Chaves:
* As subchaves de primeiro nível identificam a categoria e o fabricante/modelo da unidade:
  `Disk&Ven_<Fabricante>&Prod_<Produto>&Rev_<Revisao>`
  * *Exemplo*: `Disk&Ven_Kingston&Prod_DataTraveler_3.0&Rev_PMAP`
* Cada subchave contém uma subchave com a identificação do dispositivo (ex.: número de série ou identificador interno).

---

## Número de Série Real vs. *Windows Assigned Device ID*

> [!CAUTION] Armadilha Forense Essencial
> **Nem todos os dispositivos de armazenamento USB possuem número de série único gravado de fábrica pelo fabricante.**

### Regra de Distinção Pericial:
* **Número de Série Real de Hardware**: se o identificador sob a chave `USBSTOR` for composto por uma sequência alfanumérica contínua (ex.: `AA...` ou sem o símbolo `&` na segunda posição). Este número é gravado no chip e **mantém-se constante** se a mesma pen for ligada a qualquer outro computador.
* **Windows Assigned Device ID**: se o identificador contiver um **`&` na segunda posição** (ex.: `00045F057BD8BDC1D9C90033&0`).
  * O Windows atribui este valor internamente quando o hardware não fornece um número de série válido.
  * **Este número NÃO se mantém quando a pen é inserida noutro computador**. Concluir que duas pens com IDs gerados pelo Windows em máquinas diferentes são dispositivos distintos (ou iguais) é um erro pericial grave.

### Auditoria em PowerShell (Sistema Vivo):

```powershell
# Listar unidades de disco do tipo USB
gwmi win32_diskdrive | ? {$_.interfacetype -eq 'USB'}

# Exibir modelo, PNPDeviceID e SerialNumber correspondente
gwmi win32_diskdrive | ? {$_.interfacetype -eq 'USB'} | Select-Object model, pnpdeviceID, serialnumber
```

---

## O Ficheiro de Log `setupapi.dev.log`

Enquanto o Registry regista a existência do dispositivo, a data/hora da **primeira inserção** física do periférico no computador é comprovada através do ficheiro de registo de instalação de controladores:

```text
C:\Windows\INF\setupapi.dev.log
```

Quando uma pen USB é ligada, o Windows inicia o processo de associação de driver documentando o timestamp de arranque no log:

```text
>>>  [Device Install (Hardware initiated) - SWD\WPDBUSENUM\_??_USBSTOR#Disk&Ven_Lexar...#{53f56307-b6bf...}]
>>>  Section start 2024/01/21 02:06:40.028
```

* **Ficheiros Históricos**: à medida que atinge o limite de tamanho, o log é rodado e arquivado na mesma pasta com o carimbo temporal de criação (ex.: `setupapi.dev.20240315_174449.log`). O perito deve analisar todo o conjunto de ficheiros.

---

## Ferramentas de Análise e Anti-Forense

### 1. `USBDeview` (NirSoft)
Utilitário leve para inventariação de dispositivos USB conectados e históricos:
* Lista nome, descrição, número de série, letra de unidade atribuída, data de primeiro encaixe e data de desconexão.
* Suporta linha de comandos para relatórios rápidos:
  ```cmd
  usbview.exe /shtml list.html
  usbview.exe /sxml list.xml
  ```

### 2. `WLEAPP` (Alexis Brignoni)
* **Windows Logs, Events, and Properties Parser**: ferramenta open-source em Python 3 orientada para automação pericial.
* Possui módulo dedicado para analisar o `setupapi.dev.log`, extraindo tabelas consolidadas com o nome do dispositivo e a hora exata da **primeira conexão (*First Connection Time*)** em relatórios HTML e TSV.

### 3. Utilitário Anti-Forense: `USBOblivion`
Ferramenta utilizada por atores maliciosos para eliminar vestígios:
* Remove do Registry todas as referências a dispositivos USB nas chaves `USBSTOR`, `MountedDevices`, `USB`, bem como limpa os registos no `setupapi.dev.log`.
* A deteção da execução do USBOblivion ou de inconsistências entre logs NTFS e chaves residuais constitui forte indício de destruição deliberada de provas.

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Marcadores Temporais no Windows (Timestamps)]]
- [[Artefacto Forense ShellBags]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
