---
title: Modelo TCP-IP, Encapsulamento e Visibilidade de Tráfego HTTPS
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 1
bloco: 1
fonte_aula: 1_fundamentals.pdf (Slides 2–6, 12–13)
tags:
  - src
  - redes
  - tcp-ip
  - https
  - encapsulamento
aliases:
  - Modelo TCP/IP
  - Encapsulamento TCP/IP
  - Visibilidade de Tráfego HTTPS
atualizado: 2026-11-15
---

# Modelo TCP/IP, Encapsulamento e Visibilidade de Tráfego HTTPS

A Internet interliga redes autónomas através da família de protocolos IP, organizando a comunicação em camadas onde cada protocolo adiciona informação de controlo (encapsulamento) à medida que os dados descem na pilha.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Redes)**: A separação em camadas (Aplicação, Transporte, Rede, Física/Ligação) permite que aplicações web, email ou acesso remoto operem de forma independente do meio físico e do encaminhamento IP.
> * **Porque importa (Segurança)**: Compreender o que é encapsulado e cifrado permite distinguir o que a cifragem HTTPS protege (conteúdo HTTP, URL path, cookies, passwords) do que permanece visível a um observador de rede (IPs, portas, tamanho/temporização de pacotes e, potencialmente, nomes de domínio).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * A cifragem **protege o conteúdo**, mas a **análise de tráfego** (*traffic patterns*: tamanho, ritmo e direção dos pacotes) continua a revelar informação mesmo sem chaves de sessão.
>   * Domínios podem continuar expostos via **DNS** não cifrado ou durante o **handshake TLS** (dependendo da proteção aplicada).

---

## 1. Fluxo de Comunicação na Internet (`https://ead.ulo.pt/`)

Quando um navegador acede a um serviço web (ex.: Moodle em `https://ead.ulo.pt/`):

1. O dispositivo liga-se através de uma rede local e de um fornecedor de Internet (ISP) até à rede que aloja o serviço.
2. O **DNS** resolve o nome do serviço para um endereço **IP**.
3. O protocolo **IP** transporta os pacotes através das redes interligadas.
4. O **HTTPS** protege a comunicação entre o navegador (cliente) e o servidor, que processa os pedidos e devolve respostas no paradigma **cliente-servidor**.
5. A Web é apenas um dos serviços da Internet, a par de email, transferência de ficheiros e acesso remoto.

---

## 2. Pilha TCP/IP e Encapsulamento

No modelo TCP/IP apresentado nos slides, a pilha organiza-se em quatro níveis principais (com a fronteira entre Aplicação e Sistema Operativo — Windows, Linux, etc.):

| Camada | Papel Principal | Localização Típica |
| :--- | :--- | :--- |
| **Aplicação** | Protocolos e dados das aplicações (HTTP/HTTPS, DNS, email, acesso remoto) | Espaço de utilizador / aplicação |
| **Transporte** | Comunicação fim-a-fim, controlo de fluxo e erros, portas e *sockets* (`TCP`, `UDP`) | Sistema Operativo |
| **Rede (Internet)** | Endereçamento lógico (`IPv4`/`IPv6`), encaminhamento (*routing*) e fragmentação/remontagem | Sistema Operativo |
| **Física / Ligação** | Cablagem, tecnologia `Ethernet`, endereçamento `MAC` e transmissão de *frames* | Sistema Operativo / Hardware (NIC) |

* **Encapsulamento**: À medida que os dados descem na pilha, cada camada adiciona cabeçalhos (e, na ligação de dados, delimitadores de *frame*) com informação de controlo até o dado se transformar numa *frame* transmitida no meio físico.

---

## 3. O que Consegue Ver um Observador de Rede em HTTPS?

Num cenário em que uma ligação **HTTPS** é capturada na rede do cliente **sem acesso às chaves de sessão**:

| Normalmente Visível ao Observador | Protegido pela Cifragem (HTTPS/TLS) |
| :--- | :--- |
| Endereços IP de origem e destino | Conteúdo dos pedidos e respostas HTTP |
| Portas `TCP` ou `UDP` | Caminho do URL (*URL path*) e parâmetros de *query* |
| Tamanho dos pacotes, temporização e direção | Palavras-passe, *cookies* e dados submetidos em formulários |
| Nomes de domínio *(podem ficar expostos consoante a proteção de DNS e handshake)* | — |

---

## 4. Tópicos Base de Redes Revisitados na UC

Os slides 12–13 listam os conceitos de redes pré-requisito para a disciplina:
* Funcionamento global da Internet, encapsulamento TCP/IP e paradigma cliente-servidor;
* Significado de **serviço** vs. **protocolo**, controlo de fluxo e controlo de erro;
* Cablagem, `Ethernet`, endereçamento `MAC`, `IPv4`/`IPv6` e sub-endereçamento (*subnetting*);
* Encaminhamento IP (*routing*) vs. comutação (*switching*), fragmentação e remontagem IP;
* Protocolos de transporte `TCP` e `UDP`, noção de **porta** e ***socket***;
* `NAT`/`PAT`, `VLAN` e *inter-VLAN routing*.

---

## Perguntas de revisão

1. **Numa captura de tráfego HTTPS sem acesso às chaves de sessão, que informação continua visível a um observador na rede do cliente?**

> [!success]- Ver Resposta
> Continuam visíveis os endereços IP de origem e destino, as portas TCP/UDP, o tamanho, temporização e direção dos pacotes, e eventualmente os nomes de domínio (consoante a proteção do DNS e do *handshake*). O conteúdo HTTP, o *URL path*, os parâmetros de *query*, *cookies*, passwords e formulários permanecem protegidos pela cifragem.

2. **Qual a diferença entre os dados protegidos por cifragem e a exposição por padrões de tráfego?**

> [!success]- Ver Resposta
> A cifragem protege a confidencialidade do *payload* aplicacional, mas não oculta metadados de rede nem padrões temporais e volumétricos (análise de tráfego), que podem ainda inferir comportamentos ou serviços acedidos.

## Notas relacionadas

- [[Governação da Internet - IXPs, Infraestrutura Submarina, DNS e RFCs]]
- [[Conceitos Fundamentais de Segurança (CIA, Ameaça, Vulnerabilidade e Ataque)]]
