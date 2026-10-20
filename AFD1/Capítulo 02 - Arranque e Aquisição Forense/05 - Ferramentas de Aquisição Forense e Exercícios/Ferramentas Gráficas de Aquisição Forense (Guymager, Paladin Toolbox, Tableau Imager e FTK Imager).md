---
title: Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 2
bloco: 5
fonte_aula: MCIF – Digital Forensic Analysis 1 - Forensic Boot.pdf
tags:
  - afd1
  - forense
  - aquisicao
  - guymager
  - paladin
  - tableau-imager
  - ftk-imager
  - ssd
  - file-slack
aliases:
  - Guymager
  - Paladin Toolbox
  - Tableau Imager
  - FTK Imager
  - Aquisição Lógica em SSDs
atualizado: 2026-10-20
---

# Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)

Para além das ferramentas de linha de comandos, a aquisição forense dispõe de aplicações com interface gráfica (GUI) de alto desempenho: em **Linux**, o **Guymager** é a opção recomendada para aquisições físicas ultrarrápidas (`RAW`, `EWF`, `AFF`), enquanto a **Paladin Toolbox** se destaca por suportar aquisições lógicas (recomendadas para unidades **SSD**); em **Windows**, o **Tableau Imager** opera em conjunto com bloqueadores de escrita Tableau (lendo HPA e DCO), e o **FTK Imager** constitui a opção recomendada para Windows pela sua versatilidade na aquisição física/lógica, pré-visualização de *File Slack* e recuperação da Reciclagem.

---

## Quadro Comparativo das Ferramentas Gráficas de Aquisição

| Ferramenta | Sistema Operativo | Licença / Origem | Suporte a Aquisição Lógica (Recomendada para SSDs) | Destaque Principal na Aula |
| :--- | :---: | :--- | :---: | :--- |
| **Guymager** | Linux (GUI) | Gratuito / *Open Source* | **Não** (apenas física / clone) | **Opção recomendada para Linux**; mais rápido do que *imagers* comerciais em Windows; suporta `RAW`, `EWF` e `AFF`. |
| **Paladin Toolbox** | Linux (GUI) | Gratuito (não *open source*, requer registo) | **Sim** | Incluído na distribuição forense Live Linux **Paladin** da *Sumuri*; suporta aquisições lógicas para SSDs. |
| **Tableau Imager** | Windows (GUI) | Gratuito (não *open source*, requer registo) | **Não** | Funciona **exclusivamente com bloqueadores de escrita Tableau**; identifica e lê áreas ocultas **HPA e DCO**. |
| **FTK Imager** | Windows (GUI) | Gratuito (proprietário *Exterro / AccessData*) | **Sim** (pastas e ficheiros individuais) | **Opção recomendada para Windows**; cria imagens, pré-visualiza conteúdos e *File Slack*, monta imagens *read-only* e tem versão portátil (*Lite*). |

---

## 1. Linux GUI — *Guymager* (Opção Recomendada para Linux)

* **Perfil e Desempenho**:
  * Interface gráfica extremamente intuitiva (*very user friendly*).
  * Suporta os formatos de ficheiro de imagem **`RAW`**, **`EWF`** (`.E01`) e **`AFF`** (*Advanced Forensic Format*).
  * **Mais rápido do que os *imagers* comerciais conhecidos a correr sobre Windows** (*faster than known commercial imagers running under Windows* — devido à arquitetura multithread em C++ sobre Linux).
  * **Limitação em SSDs**: **Não suporta aquisições lógicas (*logical acquisitions*), que são a opção recomendada para unidades SSD**.
* **Ficheiros de Configuração no Linux**:
  * `/etc/guymager/guymager.cfg` $\rightarrow$ ficheiro de configuração por omissão — **NÃO alterar!** (*default configuration file, do not change!*).
  * `/etc/guymager/local.cfg` $\rightarrow$ **realizar todas as configurações personalizadas neste ficheiro**, por exemplo:
    ```ini
    EwfCompression=BEST
    ```
* **Informação Visível na Interface**: Lista o número de série (`Serial nr.`), dispositivo Linux (`/dev/sda`, `/dev/sdb`), modelo, estado, tamanho, presença de áreas ocultas (`Hidden areas`, ex.: `HPA:No / DCO:Unknown`), contagem de `Bad sectors`, velocidade média em `MB/s` e tempo restante, oferecendo no menu de contexto as ações **`Acquire image`** e **`Clone device`**.

---

## 2. Linux GUI — *Paladin Toolbox*

* **Origem e Licenciamento**:
  * Incluída na distribuição forense Live Linux **Paladin** da **Sumuri**.
  * É gratuita (*free*), mas **não é de código aberto (*not open source*)** e exige registo prévio para descarregar.
* **Vantagem Técnica**:
  * **Suporta aquisições lógicas (*supports logical acquisitions*), que constituem a opção recomendada para unidades SSD** (disponibilizando na barra lateral módulos dedicados: *Imager*, *Image Converter*, *Find*, *Unallocated*, *Disk Manager* e *Network Share*).

---

## 3. Windows GUI — *Tableau Imager*

* **Requisitos e Licenciamento**:
  * **Funciona exclusivamente com bloqueadores de escrita da marca Tableau** (*works only with Tableau write blockers*).
  * É gratuito, mas **não é de código aberto** e requer registo para descarga.
* **Capacidades e Limitações**:
  * Conforme visto na secção de áreas ocultas ([[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]]), é capaz de **identificar e ler tanto áreas HPA como DCO**.
  * **Não suporta aquisições lógicas** (recomendadas para SSDs).

---

## 4. Windows GUI — *FTK Imager* (Opção Recomendada para Windows)

O **FTK Imager** é destacado na aula como a **opção recomendada para ambientes Windows** (*Recommended option for Windows*), reunindo um conjunto abrangente de funcionalidades de aquisição e inspeção:

1. **Criação de imagens forenses Físicas e Lógicas**:
   * Cria imagens forenses de discos rígidos locais, CDs e DVDs, pens USB (*thumb drives*) ou outros dispositivos USB, bem como de **pastas inteiras (*entire folders*) ou ficheiros individuais (*individual files*)** a partir de vários locais do suporte (aquisição lógica).
2. **Pré-visualização imediata (*Preview*)**:
   * Pré-visualiza ficheiros e pastas diretamente no disco ou dentro de imagens forenses já criadas.
   * Na interface (*Evidence Tree* + *File List* + *Hex Value Interpreter*), permite inspecionar em hexadecimal tanto ficheiros regulares como o espaço de sobra de cluster (**`File Slack`**), o espaço não alocado (**`[unallocated space]`**) e o espaço não particionado (**`Unpartitioned Space`**).
3. **Montagem e Exportação**:
   * **Monta uma imagem** para visualização em modo estritamente só de leitura (*read-only view*).
   * **Exporta ficheiros e pastas** a partir de imagens forenses.
4. **Recuperação de Ficheiros Eliminados**:
   * Permite visualizar e **recuperar ficheiros que foram eliminados da Reciclagem (*Recycle Bin*)**.
5. **Integridade Criptográfica**:
   * Cria *hashes* de ficheiros para verificar a integridade dos dados e **gera relatórios de *hash* (*hash reports*)** tanto para ficheiros regulares como para imagens de disco completas.
6. **Portabilidade**:
   * A versão **Lite** corre como aplicação portátil (*portable application* — ver [[Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite]]).

---

## Implicações Forenses

* **Porquê os Slides Sublinham que a Aquisição Lógica é Recomendada para SSDs?**: Nas unidades de estado sólido (**SSD**), os mecanismos internos do controlador — como o comando **TRIM** e o *Garbage Collection* em segundo plano — limpam ativamente os blocos marcados como eliminados (convertendo o espaço não alocado em zeros) e remapeiam continuamente os endereços físicos através do *Wear Leveling* (FTL). Além disso, em muitos portáteis modernos (ex.: com cifragem de hardware ou controladores NVMe em que o arranque externo vê apenas o volume lógico desencriptado ou em que se pretende preservar rapidamente os ficheiros ativos antes que o *Garbage Collection* atue), o suporte a aquisições lógicas (presente na **Paladin Toolbox** e no **FTK Imager**, mas ausente no **Guymager** e no **Tableau Imager**) torna-se uma valência operacional importante.
* **Regra de Ouro na Configuração do Guymager**: Em exames práticos ou em distribuições forenses baseadas em Debian/Ubuntu (como CAINE, Kali ou DEFT), nunca se deve editar `/etc/guymager/guymager.cfg` (que é sobrescrito em atualizações de pacotes e contém os valores base), mas sim `/etc/guymager/local.cfg`.

---

## Além da aula

* **Inspeção de *Magic Bytes* e Estruturas em Hexadecimal no FTK Imager**:
  * Na captura de ecrã do FTK Imager (Slide 53), observa-se no painel inferior o *Hex Dump* de um ficheiro `.docx` começando pelos bytes `50 4B 03 04` (`PK..` — assinatura ZIP/OOXML) e, logo abaixo do *Regular File*, o item **`File Slack`** correspondente aos bytes residuais até ao final do cluster. Esta visualização materializa diretamente os conceitos de [[Sistemas de Numeração e Conversão entre Bases]], [[Codificação de Caracteres - ASCII, Latin-1 e Unicode]] e [[Organização de Estruturas de Dados em Binário]] estudados no Capítulo 3 de AFD1.

---

## Perguntas de revisão

- Qual é a ferramenta gráfica de aquisição recomendada para Linux e em que ficheiro devem ser guardadas as alterações de configuração (como `EwfCompression=BEST`)?
- Que limitação partilham o *Guymager* e o *Tableau Imager* no que respeita à aquisição de unidades SSD e que ferramentas gráficas apresentadas na aula superam essa limitação?
- Que requisito de hardware específico exige o *Tableau Imager* para funcionar e que vantagem oferece na deteção de áreas ocultas?
- Enumere as principais funcionalidades do *FTK Imager* que justificam a sua recomendação como ferramenta padrão em ambientes Windows.

## Notas relacionadas

- [[Aquisição e Montagem em Linux - Formato EWF (ewf-tools, ewfmount e xmount)]]
- [[Aquisição em Linha de Comandos no Linux - dcfldd e Derivados do dd]]
- [[Exercícios Práticos e de Projeto - WinFE e Aquisição Forense com FTK Imager]]
- [[Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB]]
- [[Ferramentas Portáteis de Triagem, Pesquisa e FTK Imager Lite]]
- [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]]
- [[Organização de Estruturas de Dados em Binário]]
- [[Capítulo 2 - Arranque e Aquisição Forense]]
