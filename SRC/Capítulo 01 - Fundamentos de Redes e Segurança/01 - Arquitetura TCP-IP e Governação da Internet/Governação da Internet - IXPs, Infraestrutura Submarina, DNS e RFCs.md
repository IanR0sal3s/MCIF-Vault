---
title: Governação da Internet - IXPs, Infraestrutura Submarina, DNS e RFCs
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 1
bloco: 1
fonte_aula: 1_fundamentals.pdf (Slides 7–11); ch1_Computer_Network_Security_Concepts.pdf (Secção 1.9)
tags:
  - src
  - redes
  - ixp
  - dns
  - rfc
  - normalizacao
aliases:
  - Governação da Internet
  - IXP
  - GigaPIX
  - RFC
atualizado: 2026-11-15
---

# Governação da Internet — IXPs, Infraestrutura Submarina, DNS e RFCs

A operacionalidade global da Internet assenta em quatro pilares de governação e infraestrutura: pontos de troca de tráfego (IXPs), cablagem submarina, gestão hierárquica de nomes/endereços (DNS, IP, AS) e especificações abertas (`RFCs`).

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Redes)**: Redes independentes (*Autonomous Systems*) precisam de pontos físicos de interligação, de um espaço de endereçamento único sem colisões e de normas públicas para interoperar.
> * **Porque importa (Segurança)**: Infraestruturas críticas (IXPs, cabos submarinos, registos DNS/AS) são pontos estratégicos para interceção, ataques de encaminhamento e resiliência; a normalização aberta garante revisão pública dos protocolos de segurança.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Em Portugal, o principal IXP referido na aula é o **`GigaPIX`**.
>   * Os `RFCs` (*Request for Comments*) e normas abertas permitem que sistemas desenvolvidos de forma independente comuniquem entre si.

---

## 1. Os Quatro Pilares da Governação da Internet

1. **Infraestrutura física de *Internet Exchange* (IX / IXP)**:
   * *Hubs* físicos onde redes independentes se ligam para trocar tráfego IP diretamente (*peering*).
   * Em Portugal, o exemplo destacado é o **`GigaPIX`**.
2. **Infraestrutura "submarina" (*Under Water Internet*)**:
   * Rede global de cabos submarinos que assegura a interligação intercontinental de dados.
3. **Gestão de Nomes e Endereços (*Internet Registry*)**:
   * Administração do espaço de nomes (**DNS**), blocos de endereços **IP** e números de **Sistemas Autónomos (AS)** através dos registos regionais e globais.
4. **Normas, Padrões e Protocolos (*Internet Standards and RFCs*)**:
   * Especificações abertas que permitem a comunicação interoperável entre sistemas desenvolvidos de forma independente.

---

## 2. Organismos de Normalização (Stallings, Secção 1.9)

Na segurança de redes e criptografia, destacam-se quatro entidades principais referidas na bibliografia oficial:

| Organismo | Âmbito Principal |
| :--- | :--- |
| **NIST** (*National Institute of Standards and Technology*) | Normas federais norte-americanas e especificações amplamente adotadas (ex.: `FIPS`, `NIST SP`, padronização criptográfica). |
| **ISOC / IETF** (*Internet Society / Internet Engineering Task Force*) | Desenvolvimento e publicação de normas da Internet através da série **`RFC`**. |
| **ITU-T** (*International Telecommunication Union*) | Recomendações de telecomunicações e segurança (ex.: **`X.800`** — Arquitetura de Segurança OSI). |
| **ISO** (*International Organization for Standardization*) | Federação mundial de organismos nacionais de normalização (mais de 140 países). |

---

## Perguntas de revisão

1. **Qual é a função de um *Internet Exchange Point* (IXP) como o `GigaPIX`?**

> [!success]- Ver Resposta
> Um IXP fornece um ponto físico de interligação onde redes independentes se ligam para trocar tráfego IP diretamente, integrando o tráfego da Internet com menor latência e menor dependência de trânsito intermédio.

2. **Porque são essenciais especificações abertas como os `RFCs` na segurança em redes?**

> [!success]- Ver Resposta
> Permitem que sistemas desenvolvidos de forma independente interoperem com base em regras públicas e escrutináveis pela comunidade técnica, alinhando-se com o princípio de desenho aberto (*open design*).

## Notas relacionadas

- [[Modelo TCP-IP, Encapsulamento e Visibilidade de Tráfego HTTPS]]
- [[Serviços e Mecanismos de Segurança (ITU-T X.800)]]
