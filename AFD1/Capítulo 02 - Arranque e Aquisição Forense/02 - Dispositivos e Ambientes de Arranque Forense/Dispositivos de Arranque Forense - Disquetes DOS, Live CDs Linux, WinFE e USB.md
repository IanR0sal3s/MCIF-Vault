---
title: Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 2
bloco: 2
fonte_aula: MCIF – Digital Forensic Analysis 1 - Forensic Boot.pdf
tags:
  - afd1
  - forense
  - forensic-boot
  - msdos
  - paladin
  - deft
  - winfe
  - ventoy
  - rufus
  - dd
aliases:
  - Forensic Boot Tools
  - Bootable Diskette
  - WinFE
  - Windows Forensic Environment
  - Paladin Linux
  - DEFT Linux
  - Ventoy
  - Bootable USB Devices
atualizado: 2026-10-20
---

# Dispositivos de Arranque Forense — Disquetes DOS, Live CDs Linux, WinFE e USB

Os **dispositivos de arranque forense (*Forensic Boot Tools*)** evoluíram desde as disquetes de arranque em MS-DOS (hoje obsoletas, mas ocasionalmente necessárias em sistemas legados) para os CD-ROMs/DVDs *Live* baseados em Linux (**Paladin**, **DEFT**) ou em Windows (**WinFE**, **SAFE**, **Gargoyle Investigator**) e, atualmente, para unidades USB de arranque criadas com utilitários como **Ventoy**, **Rufus**, **UNetBootIn**, **Etcher**, **Gnome Multi-Writer** ou o comando **`dd`**.

---

## 1. Disquete de Arranque Forense em MS-DOS (*Bootable Diskette*)

Embora obsoleto, um disco de arranque MS-DOS ainda é ocasionalmente necessário na perícia de máquinas industriais ou sistemas antigos:
* **3 Ficheiros Obrigatórios** para arrancar um computador em MS-DOS:
  * `IO.SYS` (referido nos diapositivos como `O.SYS`)
  * `MSDOS.SYS`
  * `COMMAND.COM`
* **Ficheiros Opcionais Processados no Arranque** (se estiverem presentes na disquete, são também utilizados durante o *boot*, devendo ser controlados ou removidos):
  * `DRVSPACE.BIN` ou `DBLSPACE.BIN` (drivers de compressão de disco)
  * `CONFIG.SYS` e `AUTOEXEC.BAT` (ficheiros de configuração e execução automática)

### Procedimento de Criação num Sistema Windows 98
1. Na linha de comandos do Windows 98, formatar a disquete transferindo os ficheiros de sistema:
   ```bat
   format a: /U /S
   ```
   * `/U` (*unconditional format*): formatação incondicional (apaga todos os dados existentes).
   * `/S`: copia os ficheiros de sistema necessários para a disquete de modo a torná-la um disco de arranque (*boot disk*).
2. **Tornar a disquete "Forense" (Limpeza)**:
   * Remover todos os ficheiros da disquete **exceto os três ficheiros obrigatórios** (`O.SYS` / `IO.SYS`, `MSDOS.SYS` e `COMMAND.COM`).
   * Para conseguir apagar ficheiros protegidos (como `DRVSPACE.BIN`), remover previamente os atributos especiais de Oculto (`H`), Só de Leitura (`R`) e Sistema (`S`):
     ```bat
     attrib -H -R -S filename
     ```
3. **Personalização Posterior**:
   * Adicionar ficheiros `CONFIG.SYS` e `AUTOEXEC.BAT` próprios e controlados pelo perito.
   * Adicionar utilitários de bloqueio de escrita (*write-blocking utilities*) e outras ferramentas forenses para DOS.

### Alternativa sem Windows 98 Instalado
* Utilizar o utilitário gratuito **HP USB Disk Format Tool**, que inclui a opção *"Create a DOS Startup Disk"*:
  * Utilitário: `http://www.19systems.net/HP-USB-Tool-v2.1.8.exe`
  * Ficheiros de arranque do Windows 98/DOS: `http://www.19systems.net/Win98-Boot-Files.zip`
* Uma vez criada a disquete de arranque, aplicam-se exatamente os mesmos passos descritos acima para a tornar "forense" (remover todos os ficheiros exceto `O.SYS`/`IO.SYS`, `MSDOS.SYS` e `COMMAND.COM` e personalizar com `CONFIG.SYS`, `AUTOEXEC.BAT`, *write-blockers* e ferramentas periciais).

---

## 2. CD-ROMs de Arranque Baseados em Linux (*Linux Based Bootable CD-ROMs*)

Existem várias distribuições Linux em formato *Live CD* pré-configuradas para análise forense (que não montam automaticamente os discos internos ou os montam estritamente em modo *read-only*):

| Distribuição Forense | Características Principais |
| :--- | :--- |
| **Paladin** (`www.sumuri.com`) | Distribuição Linux forense equipada com inúmeras ferramentas de interface gráfica (GUI), incluindo o **Autopsy** e a *Paladin Toolbox*. |
| **DEFT** (*Digital Evidence & Forensic Toolkit* — `https://launchpad.net/deft`) | Distribuição personalizada baseada no *Ubuntu Live Linux CD* vocacionada para recolha de evidência digital e resposta a incidentes. |

* **Como criar o CD-ROM de arranque**:
  1. Procurar e descarregar o ficheiro de imagem `.iso` (ex.: `Paladin-6.1.iso`).
  2. Utilizar um programa de gravação de discos óticos (*CD-burning program*) para gravar a imagem `ISO` no CD.
* **Desvantagem dos Live CDs baseados em Linux**:
  * **Nem todos os agentes de primeira intervenção (*first responders*) se sentem confortáveis a utilizar Linux**.

---

## 3. CD-ROMs e Ambientes de Arranque Baseados em Windows (*Windows Based*)

Para colmatar a barreira de utilização do Linux e permitir correr ferramentas nativas de Windows sem iniciar o sistema operativo instalado no disco suspeito, existem ambientes de arranque baseados em Windows (*Windows Preinstallation Environment* modificado para não montar/escrever em discos locais):

| Ferramenta / Ambiente | Licença / Modelo | Descrição |
| :--- | :---: | :--- |
| **WinFE (*Windows Forensic Environment*)** | Gratuito (*Free*) | Criado por **Brett Shavers**; ambiente Windows forense de referência (requer uma licença válida do Windows para construção). |
| **SAFE (*System Acquisition Forensic Environment*) Boot Disk** | Comercial | Desenvolvido pela *Forensic Soft*. |
| **Gargoyle Investigator** | Comercial | Desenvolvido pela *Wetstone*. |
| **Ventoy** | *Open Source* | Ferramenta de código aberto para criar uma pen USB de arranque multi-imagem capaz de iniciar diretamente ficheiros `ISO`, `WIM`, `IMG`, `VHD(x)` e `EFI`. |

### Análise do WinFE (*Windows Forensic Environment*)
* **Vantagens**:
  * É gratuito (embora exija que o utilizador possua uma licença de Windows).
  * Executa **software nativo de Windows**, como o **FTK Imager**, **RegRipper**, entre outros.
  * Pode ser amplamente personalizado (*customized*).
* **Desvantagens**:
  * Exige configuração prévia por parte do utilizador antes da utilização.
  * Tem de ser **construído (*built*) previamente** para incluir o conjunto específico de ferramentas do perito.

---

## 4. Dispositivos USB de Arranque (*Bootable USB Devices*)

Como a grande maioria dos computadores atuais já não possui unidades leitoras de CD/DVD, as imagens forenses (`ISO`) são instaladas em dispositivos USB de arranque através das seguintes ferramentas:

### Em Sistemas Windows
* **UNetBootIn** (`https://unetbootin.github.io/`)
* **Rufus** (`http://rufus.akeo.ie/`)

### Em Sistemas Linux
* **Gnome Multi-Writer**
* **Etcher** (*USB and SD Card Writer*)
* **UNetBootIn for Linux**
* **Ferramenta de linha de comandos `dd`**:
  ```bash
  sudo dd bs=4M if=input.iso of=/dev/sdx conv=fdatasync
  ```
  *(Nota: substituir `sdx` pela letra identificadora do dispositivo de bloco correspondente à pen USB; `bs=4M` define blocos de escrita de 4 MB e `conv=fdatasync` garante a sincronização física dos buffers antes de o comando terminar).*

---

## Implicações Forenses

* **Validação Prévia do Suporte de Arranque**: Um Ubuntu ou Windows PE comum **não é um ambiente de arranque forense** por omissão (pode ativar partições de *swap* existentes ou montar volumes NTFS em leitura/escrita para reproduzir o *journal* `$LogFile`). O perito deve usar exclusivamente distribuições forenses dedicadas (**Paladin**, **DEFT**, **WinFE**) onde o *automount* está desativado ao nível do kernel/registo.
* **Versatilidade do Ventoy em Campo**: O uso do **Ventoy** numa pen USB pericial permite transportar na mesma unidade tanto imagens Linux (`Paladin.iso`) como imagens Windows (`WinFE.iso` / `.wim`) e arrancar em modo BIOS legado ou UEFI com suporte a *Secure Boot*.

---

## Além da aula

* **Ligação aos Ficheiros Legados de Inicialização e Ferramentas de Registry em [[00 ASSI|ASSI]]**:
  * Os ficheiros `CONFIG.SYS` e `AUTOEXEC.BAT` estudados no arranque por disquete MS-DOS são exatamente os ficheiros de configuração legados cuja substituição no Windows 95 deu origem ao [[Estrutura e Hives do Windows Registry|Windows Registry]], conforme estudado no Bloco 05 de ASSI.
  * A grande vantagem apontada para o **WinFE** — poder executar ferramentas Windows como o **RegRipper** e o **FTK Imager** — articula-se diretamente com as notas [[Ferramentas de Análise e Extração do Registry]] e [[Extração da AmCache e Comparação Forense com a ShimCache]] de ASSI, permitindo ao perito correr plugins de extração sobre os hives do disco suspeito a partir de um ambiente *live* seguro sem iniciar o Windows comprometido.

---

## Perguntas de revisão

- Quais são os três ficheiros obrigatórios para arrancar um computador em MS-DOS e porque se devem apagar ficheiros como `DRVSPACE.BIN`, `CONFIG.SYS` e `AUTOEXEC.BAT` ao preparar uma disquete forense?
- Que significado têm os parâmetros `/U` e `/S` no comando `format a: /U /S` e os parâmetros `-H -R -S` no comando `attrib`?
- Compare as vantagens e desvantagens de utilizar um Live CD baseado em Linux (como o Paladin ou o DEFT) face ao ambiente WinFE baseado em Windows.
- Que comando de terminal permite gravar uma imagem `.iso` numa pen USB em Linux garantindo a escrita física integral antes do fecho do comando?

## Notas relacionadas

- [[Arranque Forense e Processo de Boot (BIOS e Código Máquina)]]
- [[Processo de Arranque UEFI, Secure Boot e Fluxo do Windows]]
- [[Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite]]
- [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]]
- [[Exercícios Práticos e de Projeto - WinFE e Aquisição Forense com FTK Imager]]
- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Extração da AmCache e Comparação Forense com a ShimCache]]
- [[Capítulo 2 - Arranque e Aquisição Forense]]
