---
title: Capítulo 2 - Arranque e Aquisição Forense
tipo: indice
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 2
fonte_aula: MCIF – Digital Forensic Analysis 1 - Forensic Boot.pdf
tags:
  - moc
  - afd1
  - forense
  - forensic-boot
  - aquisicao
  - triagem
  - winfe
  - ewf
  - dcfldd
aliases:
  - Capítulo 2 AFD1
  - Forensic Boot
  - Arranque e Aquisição Forense
atualizado: 2026-10-20
---

# Capítulo 2 — Arranque e Aquisição Forense (*Forensic Boot*)

Índice temático e encadeamento pedagógico do **Capítulo 2 (*Forensic Boot*)** da unidade curricular de [[00 AFD1|Análise Forense Digital I (AFD1)]], lecionada pelos docentes **Miguel Frade** e **Baltazar Rodrigues** (LabCIF).

As notas encontram-se organizadas em **5 blocos temáticos numerados** na pasta `AFD1/Capítulo 02 - Arranque e Aquisição Forense/`, cobrindo a totalidade dos 55 diapositivos (95 páginas) da apresentação oficial.

---

## 1. Processo de Arranque e Arranque Forense (`01 - Processo de Arranque e Arranque Forense`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Arranque Forense e Processo de Boot (BIOS e Código Máquina)]] | Motivação para o arranque forense (SSDs soldados e interfaces proprietárias), impacto do arranque normal na evidência, regra de ouro da transferência de controlo para o *boot device*, as 2 fases do arranque (ROM $\rightarrow$ hardware $\rightarrow$ *boot code*), características do código máquina (`0xB400` / `MOV AH,00`) e arranque em sistemas **BIOS** (MBR $\rightarrow$ setor da partição $\rightarrow$ SO) |
| [[Processo de Arranque UEFI, Secure Boot e Fluxo do Windows]] | Arquitetura **UEFI** e partição **ESP** (`.efi`, discos $> 2\text{ TB}$, independência de CPU e GUI), validação criptográfica no **Secure Boot** (exigência de suporte no dispositivo forense) e fluxograma completo do **Windows Boot Process** (convergência BIOS/MBR e UEFI/EFI em `Bootmgr.exe` $\rightarrow$ `Boot Config. DB` $\rightarrow$ ramo normal `Winload.exe`/`NToskrnl.exe`/`HAL`/`SMSS` vs. ramo de hibernação `Winresume.exe`/`Hiberfil.sys`) |

---

## 2. Dispositivos e Ambientes de Arranque Forense (`02 - Dispositivos e Ambientes de Arranque Forense`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB]] | Criação e limpeza de disquetes de arranque MS-DOS (`O.SYS`/`IO.SYS`, `MSDOS.SYS`, `COMMAND.COM`, `format a: /U /S`, `attrib -H -R -S` e *HP USB Disk Format Tool*); Live CDs baseados em Linux (**Paladin**, **DEFT**); ambientes baseados em Windows (**WinFE** de Brett Shavers, **SAFE**, **Gargoyle Investigator** e **Ventoy**); ferramentas de criação de pens USB de arranque em Windows (**UNetBootIn**, **Rufus**) e Linux (**Gnome Multi-Writer**, **Etcher**, **`dd`**) |

---

## 3. Ferramentas de Triagem Forense (`03 - Ferramentas de Triagem Forense`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Ferramentas de Triagem Forense no Windows Registry (RegistryReport, ForensicUserInfo e WRR)]] | Análise e triagem *offline* sobre os ficheiros de *hive* `SAM`, `SOFTWARE`, `SYSTEM` e `NTUSER.DAT`: **RegistryReport** (relatórios configuráveis de SO, software e utilizador), **ForensicUserInfo** (extração de `RID`, `LM/NT Hashes`, datas e contadores de login/falhas) e **Mitec WRR** (*Windows Registry Recovery* para máquinas bloqueadas) |
| [[Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite]] | Pesquisa rápida de ficheiros com expressões booleanas e *Perl regex* no **Agent Ransack** (incluindo documentos MS Office e LibreOffice); coleção de **Portable Forensic Tools** (`DataProtectionDecryptor`, `JumpListsView`, `Windows File Analyzer`, `BinText`, `Data Converter`, `EXIF Viewer`, `eMule MET Viewer`); e capacidades multifunções do **FTK Imager Lite** em ambientes WinFE (cópia de ficheiros bloqueados, deteção de *ADS*, aquisição de disco/RAM e montagem de `.E01`) |

---

## 4. Fundamentos e Procedimentos de Aquisição Forense (`04 - Fundamentos e Procedimentos de Aquisição Forense`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Princípios de Aquisição Forense, Resposta Inicial e Camadas de Abstração]] | Enquadramento na fase de preservação e validade legal; árvore de decisão de primeira intervenção (*U.S. DOJ First Responders Flow Chart*) para computadores desligados vs. ligados e processos destrutivos (`format`, `delete`, `remove`, `wipe`); as 4 camadas de análise/aquisição (**Physical**, **Volume**, **File**, **Application**); e compromisso entre tamanho de bloco (`block size`) e tamanho de setor (`512 bytes` em HDD vs. SSD) |
| [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]] | Leitura via BIOS vs. **Direct Access**; aquisição *post-mortem* (risco de arranque rápido e *spyware* no firmware HDD) vs. *alive* (risco de *rootkits*); gestão de **bad sectors** (preenchimento com zeros `000000` para manter o alinhamento, *log* e redução automática de bloco); áreas ocultas **HPA** (`hdparm` temporário) e **DCO** (remoção permanente) e regra das 2 aquisições; **Write Blockers** de Hardware vs. Software (testes **CFTT**) |
| [[Armazenamento da Aquisição - Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes]] | Comparação técnica entre **Clonagem** (*zero out* prévio, vulnerabilidade ao *auto-mount*) e **Criação de Imagem Forense** (*read-only*, simulação de escrita com ficheiro de *cache*, *splitting*); formatos de imagem (**RAW**, **RAW + metadados externos**, **Embedded** e compromissos da compressão); aquisição **Local vs. Remota** (compressão e cifragem de rede); e assinatura digital de ficheiros de *hash* por blocos com **GnuPG** e servidor de *timestamping* |

---

## 5. Ferramentas de Aquisição Forense e Exercícios (`05 - Ferramentas de Aquisição Forense e Exercícios`)

| Nota | Descrição e Foco Técnico |
| :--- | :--- |
| [[Aquisição e Montagem em Linux - Formato EWF (ewf-tools, ewfmount e xmount)]] | Projeto **CFTT**; o formato **Expert Witness Format (EWF / `.E01`)** e a suite `ewf-tools` (`ewfacquire`, `ewfacquirestream`, `ewfmount`, `ewfexport`, `ewfinfo`, `ewfrecover`, `ewfverify`); exemplo interativo do `ewfacquire`; e montagem em 2 passos no Linux com `sudo` (`ewfmount` + `mount -o ro,loop,show_sys_files,streams_interface=windows,offset=$[63*512]`) ou sem `sudo` (`xmount --cache` + `udisksctl`) |
| [[Aquisição em Linha de Comandos no Linux - dcfldd e Derivados do dd]] | A ferramenta **`dcfldd`** (DCFL) e as 7 diferenças face ao `dd`; derivados forenses (`dc3dd`, `ddrescue`, `dd_rescue`, `rdd`); análise completa do comando de aquisição (`hashwindow=1G`, `hashconv=after`, `bs=512`, `conv=noerror,sync`, `split=10G`, `splitformat=aa`) e estrutura do ficheiro `SHA256.txt` |
| [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]] | Ferramentas GUI em Linux e Windows: **Guymager** (opção recomendada para Linux, configuração em `/etc/guymager/local.cfg`), **Paladin Toolbox** (suporte a aquisições lógicas recomendadas para SSDs), **Tableau Imager** (exclusivo para *write blockers* Tableau, leitura de HPA/DCO) e **FTK Imager** (opção recomendada para Windows, aquisição física/lógica, *File Slack*, *Recycle Bin* e relatórios de *hash*) |
| [[Exercícios Práticos e de Projeto - WinFE e Aquisição Forense com FTK Imager]] | Consolidação do **Lab 01** (construção de imagem **WinFE** e arranque em máquina virtual, Slide 23) e do **Estudo de Caso do Projeto** (extração física do HDD atribuído à equipa, ligação ao *write-blocker* e aquisição no **FTK Imager** com *split* de `4 096 MB` para `FAT32` e compressão ativa, Slide 54) |

---

## 🧭 Navegação

* [[00 AFD1|Voltar ao Índice de AFD1]]
* [[Capítulo 1 - Método de Investigação|Recuar para o Capítulo 1 — Método de Investigação]]
* [[Capítulo 3 - Organização de Dados|Avançar para o Capítulo 3 — Organização de Dados]]
* [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses|Pontes com ASSI — Capítulo 1 (UEFI Secure Boot, Hives do Registry e Triagem no Windows)]]
* [[Home|Voltar ao Hub Central do MCIF]]
