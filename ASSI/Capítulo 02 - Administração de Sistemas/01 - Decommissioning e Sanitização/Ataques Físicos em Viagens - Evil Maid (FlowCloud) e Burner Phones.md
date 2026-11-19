---
title: Ataques Físicos em Viagens - Evil Maid (FlowCloud) e Burner Phones
tipo: analise
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 1
fonte_aula: System Administration - System and Data Management.pdf
tags:
  - assi
  - administracao-sistemas
  - evil-maid
  - flowcloud
  - burner-phones
  - seguranca-fisica
  - stingray
  - darkhotel
aliases:
  - Evil Maid Attack
  - FlowCloud
  - Burner Phones
  - Viagens ao Estrangeiro
  - DarkHotel
atualizado: 2026-11-11
---

# Ataques Físicos em Viagens - Evil Maid (FlowCloud) e Burner Phones

Os ataques **Evil Maid** exploram acesso físico breve a dispositivos desligados em viagens — como na injeção USB da *backdoor* `FlowCloud` (2026) — exigindo *burner phones* e controlo rígido do arranque.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Por omissão, portáteis permitem o arranque a partir de suportes externos (USB) e os dispositivos móveis mantêm interfaces sem fios ativas (Bluetooth, Wi-Fi e banda base celular) suscetíveis a interação em proximidade física. Quando o equipamento sai da custódia direta do utilizador (quarto de hotel ou inspeção aduaneira), o perímetro lógico da rede corporativa deixa de proteger o hardware.
> * **Porque importa (Segurança / Forense)**: Um atacante com minutos de acesso físico a um portátil desligado consegue arrancar um ambiente externo via USB e implantar *malware* persistente diretamente no armazenamento (caso `FlowCloud`). Em análise forense pós-viagem, estas intrusões exigem correlacionar alterações no disco/arranque e eventuais instalações de *spyware* efetuadas offline sem registo em *firewalls* corporativos.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * No caso `FlowCloud` (*CrowdStrike 2026 Threat Hunting Report*), os portáteis estavam desligados no quarto de hotel e foram **arrancados via pen USB**;
>   * Os dispositivos de empréstimo (*loaner devices* / *burner phones*) têm de ser apagados **antes da partida e imediatamente após o regresso**;
>   * Os **5 vetores de risco em viagens** combinam ataques rádio (Bluetooth), inspeção secundária aduaneira (*secondary screening*), torres celulares falsas (`StingRay` / *IMSI-catchers*), atualizações Wi-Fi falsas e campanhas `DarkHotel` / *Evil Maid*.

---

## 1. *Evil Maid Attack* e o Caso `FlowCloud` (CrowdStrike 2026 — Slide 10)

### 1.1. Mecanismo do Ataque *Evil Maid*
O *Evil Maid Attack* ocorre quando um portátil ou dispositivo eletrónico é deixado desligado num quarto de hotel (ou outro espaço temporário) e um agente disfarçado — como um empregado de limpeza, segurança ou intruso — obtém **acesso físico breve** ao equipamento na ausência do proprietário para adulterar o firmware, o carregador de arranque ou o sistema em disco ([Artigo Evil Maid / FlowCloud](https://tinyurl.com/4zzkb5tb)).

### 1.2. Caso Real — *CrowdStrike 2026 Threat Hunting Report*

* **Contexto operacional**: um grupo de *hacking* chinês entrou em quartos de hotel enquanto executivos jantavam fora;
* **Vetor de execução**: os atacantes **arrancaram os portáteis desligados a partir de uma pen USB** (*booted from a USB stick*);
* **Implantação da ameaça**: injetaram a *backdoor* **`FlowCloud`** diretamente no armazenamento de cada portátil, reiniciaram as máquinas e abandonaram o quarto sem deixar sinais aparentes ao utilizador.

---

## 2. Protocolo de *Burner Phones* e Dispositivos de Empréstimo (Slide 11)

Para deslocações a países estrangeiros de risco elevado, aplicam-se as recomendações operacionais ilustradas pelo protocolo de Kenneth G. Lieberthal (especialista da *Brookings Institution* em viagens à China — [NYT — Protocolo de Viagem](https://nyti.ms/2Nkll8W)):

1. **Usar equipamentos temporários (*Burner Phones* / *Loaner Devices*)**: deixar os dispositivos habituais em casa e levar apenas equipamentos de empréstimo, **apagados antes de partir e imediatamente após regressar**;
2. **Desativar Bluetooth e Wi-Fi**: manter as interfaces rádio desativadas sempre que não forem estritamente necessárias;
3. **Não ligar a redes desconhecidas**: evitar redes Wi-Fi públicas ou de hotéis sem isolamento adequado;
4. **Nunca deixar o telemóvel fora de vista**: durante reuniões sensíveis, desligar o telemóvel e remover a bateria, caso o modelo o permita;
5. **Evitar digitar palavras-passe no teclado**: para contornar eventuais *keyloggers* de hardware ou software, copiar e colar credenciais a partir de uma pen USB limpa dedicada.

---

## 3. Os Cinco Vetores de Risco em Viagens ao Estrangeiro (Slide 12)

| # | Vetor de Risco | Mecanismo de Comprometimento |
| :---: | :--- | :--- |
| **1** | **Ataques por Radiofrequência (*RF Hacking*)** | Exploração remota de proximidade através de Bluetooth ou outras interfaces rádio ativas. |
| **2** | **Instalação física por agentes alfandegários** | Durante inspeções secundárias (*secondary screening*) na fronteira ou aeroporto, o telemóvel é retirado da vista do viajante, permitindo a instalação física direta de *spyware*. |
| **3** | **Torres celulares falsas (*Fake Cell Towers*)** | Interceção de comunicações e metadados móveis com equipamentos **`StingRay`** (*IMSI-catchers*). |
| **4** | **Infeção via Wi-Fi** | Injeção de **atualizações de software falsas (*bogus software updates*)** através da rede do hotel. |
| **5** | **Campanhas `DarkHotel` e ataques *Evil Maid*** | Comprometimento direcionado de executivos em redes hoteleiras e acesso físico furtivo aos quartos. |

---

## Além da aula

* **Bloqueio do Arranque USB e Mitigação de `FlowCloud` (`AFD1` Cap. 2 e `ASSI` Cap. 1 e Cap. 2)**: O arranque de um portátil desligado a partir de uma pen USB explora o mecanismo de ordem de arranque estudado em [[Arranque Forense e Processo de Boot (BIOS e Código Máquina)]] e [[Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB]]. Para neutralizar este vetor físico, é obrigatório conjugar [[UEFI Secure Boot]] (sem chaves comprometidas como no [[PKfail - Vulnerabilidade do UEFI Secure Boot]]) com password na BIOS/UEFI, desativação do arranque USB externo e cifragem completa com `TPM+PIN` (evitando também o bypass [[System e OS Hardening e Vulnerabilidade BitLocker YellowKey (CVE-2026-45585)|BitLocker YellowKey CVE-2026-45585]]).
* **Interceção Celular com `StingRay` (`ASSI` Cap. 2 Bloco 06)**: O funcionamento dos *IMSI-catchers* e torres falsas que forçam o *downgrade* celular articula-se diretamente com as vulnerabilidades de comunicações móveis analisadas em [[Falhas de Autenticação por SMS - Protocolo SS7, SIM-Jacking, Vishing e StingRay]].

---

## Perguntas de revisão

1. **Em que consiste um *Evil Maid Attack* e que técnica física permitiu injetar a *backdoor* `FlowCloud` no caso reportado pela CrowdStrike em 2026?**

> [!success]- Ver Resposta
> Um *Evil Maid Attack* consiste na obtenção de acesso físico não autorizado a um portátil ou dispositivo deixado sem supervisão (por exemplo, num quarto de hotel) para o comprometer. No caso da CrowdStrike (2026), os atacantes entraram nos quartos enquanto os executivos jantavam, **arrancaram os portáteis desligados através de uma pen USB** e gravaram a *backdoor* `FlowCloud` diretamente no disco antes de reiniciar e sair.

2. **Indique as cinco boas práticas operacionais do protocolo de *burner phones* e *loaner devices* para viagens ao estrangeiro.**

> [!success]- Ver Resposta
> (1) Deixar os equipamentos habituais em casa e usar dispositivos de empréstimo apagados antes da viagem e imediatamente após o regresso; (2) desativar Bluetooth e Wi-Fi; (3) não ligar a redes desconhecidas; (4) nunca perder o telemóvel de vista (desligando-o e removendo a bateria em reuniões, se possível); e (5) evitar digitar palavras-passe no teclado, copiando-as de uma pen USB limpa contra *keyloggers*.

3. **Quais são os cinco vetores de risco identificados em viagens ao estrangeiro envolvendo telemóveis e portáteis?**

> [!success]- Ver Resposta
> (1) *Radio frequency hacking* (via Bluetooth ou outras interfaces rádio); (2) instalação física de *spyware* por agentes aduaneiros durante *secondary screening*; (3) torres celulares falsas (`StingRay` / *IMSI-catchers*); (4) infeção via Wi-Fi por injeção de atualizações de software falsas (*bogus software updates*); e (5) campanhas `DarkHotel` e ataques físicos *Evil Maid*.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Decommissioning de Equipamentos, Destruição de Papel (P-1 a P-7) e Enquadramento Legal UE]] | `mesmo bloco` |
| **Seguinte** | [[Sanitização e Destruição de Discos Magnéticos (HDDs) - Wiping, Degaussing e Destruição Física]] | `mesmo bloco` |
| **Índice** | [[Capítulo 2 - Administração de Sistemas]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[System e OS Hardening e Vulnerabilidade BitLocker YellowKey (CVE-2026-45585)]] · `Bloco 03`
* [[Falhas de Autenticação por SMS - Protocolo SS7, SIM-Jacking, Vishing e StingRay]] · `Bloco 06`
* [[Arranque Forense e Processo de Boot (BIOS e Código Máquina)]] · `AFD1 · Cap. 2`
* [[Dispositivos de Arranque Forense - Disquetes DOS, Live CDs Linux, WinFE e USB]] · `AFD1 · Cap. 2`
* [[UEFI Secure Boot]] · `Cap. 1`
* [[PKfail - Vulnerabilidade do UEFI Secure Boot]] · `Cap. 1`
