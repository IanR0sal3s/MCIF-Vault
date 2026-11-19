---
title: Pen Drives USB Falsas e Verificação com ValiDrive (Ficha 11)
tipo: ferramenta
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
  - validrive
  - fake-usb
  - integridade-armazenamento
  - ficha-11
aliases:
  - Pen Drives USB Falsas
  - Fake USB Flash Drives
  - ValiDrive
  - Ficha 11 ValiDrive
atualizado: 2026-11-11
---

# Pen Drives USB Falsas e Verificação com ValiDrive (Ficha 11)

As **pen drives USB falsas** adulteram o firmware para reportar `1 TB` ou `2 TB` sobre apenas `50–64 GB` reais; o utilitário **ValiDrive** testa **576 regiões** sem destruir dados para expor a fraude.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: O sistema operativo confia no número total de setores reportado pelo controlador USB (`reported capacity`) durante a enumeração para criar partições e tabelas de ficheiros ao longo de todo o espaço lógico anunciado.
> * **Porque importa (Segurança / Forense)**: Unidades fraudulentas vendidas a baixo custo combinam um chip físico reduzido (*Real Part*) com endereçamento fictício (*Fake Part*). Quando o utilizador ou um técnico grava cópias de segurança ou aquisições forenses além do limite físico real, o controlador descarta dados em silêncio ou sobrescreve ciclicamente o início da tabela de ficheiros, corrompendo irremediavelmente a evidência ou o backup.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Falsa sensação de normalidade**: a formatação rápida e a cópia inicial de ficheiros decorrem sem mensagens de erro do SO; o problema só surge na leitura posterior;
>   * **Anatomia**: distinguir `reported capacity` (ex.: `1–2 TB`), **Parte Real** (`50–64 GB`) e **Parte Falsa** (`950 GB+`);
>   * **Funcionamento do `ValiDrive` (Ficha 11)**: realiza um *spot-check* aleatório **não destrutivo** em **576 regiões** distribuídas por toda a capacidade declarada, apresentando células **verdes** (*Validated Storage*) vs. **vermelhas** (*Missing Storage*).

---

## 1. Anatomia das Pen Drives USB Falsas (*Fake USB Flash Drives* — Slides 38–40)

Unidades USB fraudulentas — frequentemente comercializadas online a preços irrealisticamente baixos (ex.: **`$19.99 USD` por `1 TB` ou `2 TB`**) — possuem o firmware do controlador manipulado para enganar o sistema operativo ([Vídeo Demonstrativo](https://www.youtube.com/watch?v=xMgEHy1A9QA)):

**Capacidade Declarada ao SO (*reported capacity*):** `1 TB – 2 TB`

| Região Lógica do Dispositivo | Parte Real (*Real Part*) | Parte Falsa (*Fake Part* — ex.: `950 GB+`) |
| :--- | :--- | :--- |
| **Hardware físico** | `50 GB – 64 GB` físicos reais | Sem chips de memória flash físicos |
| **Comportamento na escrita** | Armazenamento funcional até ao limite físico real | Escritas descartadas silenciosamente ou em **sobreposição cíclica** sobre o início do disco / tabela FAT |

1. **Capacidade anunciada vs. real**: o controlador declara ao sistema operativo (`reported capacity`) o valor fraudado (ex.: `2 TB`), mas a placa contém apenas um chip pequeno correspondente à **Parte Real (*Real Part*, ex.: `50 GB` ou `64 GB`)** e uma extensa **Parte Falsa (*Fake Part*, ex.: `950 GB`)** sem memória física;
2. **Corrupção silenciosa dos dados**: a unidade aceita escritas aparentemente normais muito além do seu limite físico; na prática, os dados enviados para a *Fake Part* são descartados ou **sobrescrevem ciclicamente os blocos iniciais**, destruindo a própria tabela de alocação de ficheiros e corrompendo ficheiros gravados anteriormente — falha que apenas se descobre ao tentar ler os ficheiros mais tarde.

---

## 2. Verificação Não Destrutiva com `ValiDrive` — Ficha 11 (Slides 39–41)

Para validar a integridade e a capacidade física genuína de unidades USB antes de armazenar cópias de segurança ou dados críticos, utiliza-se o utilitário gratuito **`ValiDrive`**, desenvolvido por Steve Gibson / Gibson Research Corporation ([GRC — ValiDrive](https://www.grc.com/validrive.htm)):

* **Amostragem em 576 regiões (`Ficha 11 – Validrive`, Slide 41)**: o `ValiDrive` executa verificações rápidas aleatórias (*spot-check*) de leitura e escrita **não destrutivas** (restaurando o conteúdo original após cada teste) em **576 regiões** uniformemente distribuídas por toda a capacidade reportada pelo dispositivo;
* **Mapa visual de integridade**:
  * **Células verdes (*Validated Storage*)**: regiões com memória flash física funcional que retêm corretamente os padrões escritos;
  * **Células vermelhas (*Missing Storage*)**: regiões sem armazenamento físico real, com descarte de escrita ou sobreposição cíclica;
* **Diagnóstico final**: a ferramenta apresenta com exatidão a capacidade real verificada face à capacidade falsamente declarada (ex.: declara `2.00 TB`, mas apenas os primeiros `62 GB` correspondem a armazenamento real validado).

---

## Além da aula

* **Integridade de Suportes de Destino na Aquisição Forense (`AFD1` Cap. 2 e `AFD1` Cap. 1)**: Nunca se deve utilizar um suporte externo de origem desconhecida ou não validada para receber imagens forenses ou ficheiros de triagem (`E01`/`dd`), uma vez que a sobreposição cíclica de uma pen falsa destruiria irremediavelmente os ficheiros de imagem e invalidaria os *hashes* descritos em [[Armazenamento da Aquisição - Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes]].
* **Articulação com Políticas e Sanitização USB (`ASSI` Cap. 2 Blocos 01 e 02)**: A verificação com `ValiDrive` complementa a governação segura de dispositivos amovíveis de [[Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)]] e os procedimentos específicos para memórias NAND Flash em [[Arquitetura SSD e Memória NAND (Wear Leveling e Garbage Collection)]].

---

## Perguntas de revisão

1. **Como é que uma pen USB falsa engana o sistema operativo e porque é que o utilizador só descobre a perda de dados mais tarde?**

> [!success]- Ver Resposta
> O firmware adulterado declara uma `reported capacity` muito superior (ex.: `1 TB` ou `2 TB`) à memória física existente (**Parte Real**, ex.: `50–64 GB`). O sistema operativo aceita escrever na **Parte Falsa** sem erros aparentes, mas o controlador descarta silenciosamente esses dados ou sobrescreve ciclicamente os blocos iniciais do disco (destruindo a tabela de ficheiros e os primeiros dados gravados), erro que só fica visível quando o utilizador tenta ler os ficheiros posteriormente.

2. **Como funciona a verificação realizada pelo utilitário `ValiDrive` (Ficha 11) e qual é o significado das cores no mapa visual?**

> [!success]- Ver Resposta
> O `ValiDrive` realiza testes aleatórios (*spot-check*) de escrita e leitura **não destrutivos** em **576 regiões** distribuídas por toda a capacidade declarada pelo dispositivo. As células **verdes** indicam armazenamento físico verdadeiro verificado (*Validated Storage*), enquanto as células **vermelhas** assinalam armazenamento inexistente (*Missing Storage*), determinando a capacidade física real exata face à declarada.

3. **Que risco crítico existe se um técnico armazenar cópias de segurança ou aquisições forenses numa pen USB não verificada com capacidade fraudulenta?**

> [!success]- Ver Resposta
> Assim que o volume de dados gravados exceder a pequena *Real Part* física, a sobreposição cíclica corromperá não apenas os novos ficheiros gravados na *Fake Part*, como também os blocos iniciais onde residem a tabela de ficheiros e os primeiros ficheiros/segmentos gravados, provocando perda irreversível dos backups ou da evidência.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Vetores de Ataque USB (BadUSB, Rubber Ducky, LNK, USB-Killer) e Defesas (GPO, Pad Jack, ESD Dogs)]] | `mesmo bloco` |
| **Seguinte** | [[System e OS Hardening e Vulnerabilidade BitLocker YellowKey (CVE-2026-45585)]] | `muda para Bloco 03` |
| **Índice** | [[Capítulo 2 - Administração de Sistemas]] · [[00 ASSI]] | `Bloco 02` |

### Conceitos Relacionados

* [[Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)]] · `mesmo bloco`
* [[Arquitetura SSD e Memória NAND (Wear Leveling e Garbage Collection)]] · `Comum/`
* [[Armazenamento da Aquisição - Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes]] · `AFD1 · Cap. 2`
