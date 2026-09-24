---
title: UEFI Secure Boot - Chaves e Hierarquia
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
  - uefi
  - secure-boot
  - cryptography
  - firmware
aliases:
  - UEFI Key Hierarchy
  - Secure Boot Architecture
  - UEFI Secure Boot - Chaves e Hierarquia (PK, KEK, db, dbx)
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
atualizado: 2026-09-24
---

# Hierarquia de Chaves do UEFI Secure Boot

A integridade criptográfica do [[UEFI Secure Boot]] assenta numa relação de confiança hierárquica estabelecida entre quatro bases de dados e certificados digitais. Embora frequentemente referidas de forma agregada como chaves de validação, no firmware do dispositivo residem essencialmente **certificados públicos e *hashes***; as correspondentes **chaves privadas** permanecem na posse dos respetivos emissores (fabricantes OEM e Microsoft) para autorizar atualizações e assinar binários.

```text
          ┌──────────────────────────────────┐
          │      Platform Key (PK)           │  Hardware / Firmware
          └────────────────┬─────────────────┘
                           │ Autoriza e valida modificações na KEK
          ┌────────────────▼─────────────────┐
          │    Key Exchange Key (KEK)        │  Firmware / Sistema Operativo
          └────────────────┬─────────────────┘
                 ┌─────────┴─────────┐
                 ▼                   ▼
    ┌────────────────────────┐  ┌───────────────────────────┐
    │ Signature Database (db)│  │ Forbidden Database (dbx)  │
    └────────────────────────┘  └───────────────────────────┘
```

---

## 1. Platform Key (PK)

* **Âmbito de Aplicação**: Hardware / Firmware da plataforma.
* **Função Primária**: É a chave mestra da raiz de confiança do hardware. Estabelece a ligação entre o fabricante do computador (OEM) e o firmware da placa-mãe.
* **Privilégio Crítico**: **Controla e autoriza alterações a todas as restantes chaves e bases de dados**. Quem possuir a chave privada correspondente à PK pode modificar a KEK e reconfigurar todo o comportamento do Secure Boot.
* **O Problema PKfail**: Se o fabricante incluir por negligência um certificado de teste genérico (ex.: o emitido pela American Megatrends com `Subject: DO NOT TRUST` e `Issuer: DO NOT TRUST – AMI TEST KEY`), e cuja chave privada de exemplo seja pública, qualquer atacante consegue assinar atualizações arbitrárias de chaves.

---

## 2. Key Exchange Key (KEK)

* **Âmbito de Aplicação**: Firmware / Sistema Operativo.
* **Função Primária**: Serve de intermediária entre o fabricante do hardware e os fornecedores de sistemas operativos (como a Microsoft ou distribuições Linux).
* **Privilégio**: Autoriza a inserção e atualização de certificados nas bases de dados operacionais de assinaturas (`db` e `dbx`). Tipicamente, um dispositivo contém a KEK do fabricante do PC e a KEK da Microsoft.

---

## 3. Signature Database (`db`)

* **Âmbito de Aplicação**: Componentes de arranque e controladores.
* **Função Primária**: Base de dados de **assinaturas autorizadas** (lista branca). Contém os certificados digitais e *hashes* SHA-256 de gestores de arranque (`bootmgr.efi`), carregadores de SO (`winload.efi`) e controladores de firmware EFI autorizados a executar na máquina.

---

## 4. Forbidden Signature Database (`dbx`)

* **Âmbito de Aplicação**: Binários maliciosos ou revogados.
* **Função Primária**: Base de dados de **revogação e assinaturas proibidas** (lista negra). Contém assinaturas e *hashes* de *bootloaders* vulneráveis, drivers maliciosos conhecidos ou certificados revogados por comprometimento.
* **Prevalência**: A verificação contra a `dbx` tem **prioridade absoluta sobre a `db`**. Se um binário constar simultaneamente na `db` e na `dbx`, o firmware rejeita a sua execução.

---

## Implicações Forenses e Vetor de Exploração

A posse da chave privada da Platform Key anula completamente a eficácia do Secure Boot:
1. O atacante utiliza a chave privada da PK comprometida para assinar a inserção de uma KEK sua.
2. Com a sua KEK, assina e adiciona um certificado próprio à base de assinaturas autorizadas (`db`).
3. Uma vez inserido o certificado na `db`, o atacante pode carregar um *bootkit* assinado na partição EFI de sistema (`ESP`), sendo este considerado legítimo pelo firmware durante o arranque subsequente ([[PKfail - Cadeia de Ataque e Deteção Forense]]).

## Notas relacionadas

- [[UEFI Secure Boot]]
- [[PKfail - Vulnerabilidade do UEFI Secure Boot]]
- [[PKfail - Cadeia de Ataque e Deteção Forense]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
