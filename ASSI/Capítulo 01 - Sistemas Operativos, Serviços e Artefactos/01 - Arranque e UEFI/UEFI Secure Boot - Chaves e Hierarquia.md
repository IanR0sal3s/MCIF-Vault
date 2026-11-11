---
title: UEFI Secure Boot - Chaves e Hierarquia
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 1
tipo: conceito
tags:
  - assi
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

A integridade do [[UEFI Secure Boot]] baseia-se numa relação de confiança hierárquica entre quatro bases de dados e certificados gravados na NVRAM do firmware: a Platform Key (`PK`), a Key Exchange Key (`KEK`), a base autorizada (`db`) e a base de revogação (`dbx`).

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Separar a raiz de propriedade do hardware (`PK`, gerida pelo OEM) da gestão operacional do sistema operativo (`KEK`, gerida pela Microsoft/SO) permite atualizar listas de binários permitidos (`db`) e revogados (`dbx`) via Windows Update sem exigir a chave mestra do fabricante da placa-mãe.
> * **Porque importa (Forense / Segurança)**: A posse da chave privada correspondente à `PK` compromete toda a árvore descendente, permitindo ao atacante inscrever uma `KEK` própria, adicionar o seu certificado à `db` e executar *bootkits* assinados na partição EFI (`ESP`).
> * **Pontos Críticos para Exame**:
>   * No firmware residem apenas **certificados públicos e *hashes***; as **chaves privadas** permanecem na posse dos emissores (OEM e Microsoft).
>   * A lista negra **`dbx` tem prioridade absoluta sobre a `db`**: se um binário constar em ambas, a sua execução é bloqueada.

---

## Arquitetura e Comparação das 4 Chaves / Bases de Dados

Embora frequentemente referidas de forma agregada como chaves de validação, no firmware do dispositivo residem essencialmente **certificados públicos e *hashes***; as correspondentes **chaves privadas** permanecem na posse dos respetivos emissores (fabricantes OEM e Microsoft) para autorizar atualizações e assinar binários.

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

| Base / Chave | Âmbito de Aplicação | Entidade Gestora Típica | Função Primária e Regra de Prevalência |
| :--- | :--- | :--- | :--- |
| **1. `PK`** (*Platform Key*) | Hardware / Firmware da plataforma | Fabricante do computador (OEM) | Chave mestra da raiz de confiança; controla e autoriza alterações à `KEK` e a todas as restantes bases de dados. |
| **2. `KEK`** (*Key Exchange Key*) | Firmware / Sistema Operativo | OEM e Fornecedores de SO (Microsoft, Linux) | Chave intermediária que autoriza a inserção e atualização de certificados nas bases operacionais (`db` e `dbx`). |
| **3. `db`** (*Signature Database*) | Componentes de arranque e drivers EFI | Atualizada via `KEK` (OEM / Microsoft) | **Lista branca**: contém certificados e *hashes* SHA-256 de `bootmgr.efi`, `winload.efi` e drivers EFI autorizados. |
| **4. `dbx`** (*Forbidden Signature Database*) | Binários maliciosos ou vulneráveis | Atualizada via `KEK` (Microsoft / UEFI Revocation) | **Lista negra**: contém *hashes* e certificados revogados. **Prevalece sempre sobre a `db`** em caso de conflito. |

---

## Detalhe Individual dos Componentes

### 1. Platform Key (PK)

* **Âmbito de Aplicação**: Hardware / Firmware da plataforma.
* **Função Primária**: É a chave mestra da raiz de confiança do hardware. Estabelece a ligação entre o fabricante do computador (OEM) e o firmware da placa-mãe.
* **Privilégio Crítico**: **Controla e autoriza alterações a todas as restantes chaves e bases de dados**. Quem possuir a chave privada correspondente à PK pode modificar a KEK e reconfigurar todo o comportamento do Secure Boot.
* **O Problema PKfail**: Se o fabricante incluir por negligência um certificado de teste genérico (ex.: o emitido pela American Megatrends com `Subject: DO NOT TRUST` e `Issuer: DO NOT TRUST – AMI TEST KEY`), e cuja chave privada de exemplo seja pública, qualquer atacante consegue assinar atualizações arbitrárias de chaves.

### 2. Key Exchange Key (KEK)

* **Âmbito de Aplicação**: Firmware / Sistema Operativo.
* **Função Primária**: Serve de intermediária entre o fabricante do hardware e os fornecedores de sistemas operativos (como a Microsoft ou distribuições Linux).
* **Privilégio**: Autoriza a inserção e atualização de certificados nas bases de dados operacionais de assinaturas (`db` e `dbx`). Tipicamente, um dispositivo contém a KEK do fabricante do PC e a KEK da Microsoft.

### 3. Signature Database (`db`)

* **Âmbito de Aplicação**: Componentes de arranque e controladores.
* **Função Primária**: Base de dados de **assinaturas autorizadas** (lista branca). Contém os certificados digitais e *hashes* SHA-256 de gestores de arranque (`bootmgr.efi`), carregadores de SO (`winload.efi`) e controladores de firmware EFI autorizados a executar na máquina.

### 4. Forbidden Signature Database (`dbx`)

* **Âmbito de Aplicação**: Binários maliciosos ou revogados.
* **Função Primária**: Base de dados de **revogação e assinaturas proibidas** (lista negra). Contém assinaturas e *hashes* de *bootloaders* vulneráveis, drivers maliciosos conhecidos ou certificados revogados por comprometimento.
* **Prevalência**: A verificação contra a `dbx` tem **prioridade absoluta sobre a `db`**. Se um binário constar simultaneamente na `db` e na `dbx`, o firmware rejeita a sua execução.

---

## Implicações Forenses e Vetor de Exploração

A posse da chave privada da Platform Key anula completamente a eficácia do Secure Boot:

1. O atacante utiliza a chave privada da PK comprometida para assinar a inserção de uma KEK sua.
2. Com a sua KEK, assina e adiciona um certificado próprio à base de assinaturas autorizadas (`db`).
3. Uma vez inserido o certificado na `db`, o atacante pode carregar um *bootkit* assinado na partição EFI de sistema (`ESP`), sendo este considerado legítimo pelo firmware durante o arranque subsequente ([[PKfail - Cadeia de Ataque e Deteção Forense]]).

---

## Perguntas de revisão

1. **Qual é a função específica da Key Exchange Key (`KEK`) na hierarquia do UEFI Secure Boot e que chaves lhe são subordinadas?**

> [!success]- Ver Resposta
> A `KEK` atua como intermediária de confiança entre o fabricante do hardware (OEM) e os fornecedores do sistema operativo (como a Microsoft). A sua função é autorizar e validar a inserção ou atualização de certificados e *hashes* nas bases de dados operacionais subordinadas: a `db` (assinaturas autorizadas) e a `dbx` (assinaturas proibidas/revogadas).

2. **Se um gestor de arranque (`bootmgr.efi`) estiver assinado por um certificado válido presente na `db`, mas o seu *hash* SHA-256 tiver sido adicionado à `dbx`, o firmware UEFI permite a sua execução?**

> [!success]- Ver Resposta
> Não. A verificação contra a base de dados de assinaturas proibidas (`dbx`) tem **prioridade absoluta sobre a `db`**. Sempre que um binário ou certificado conste simultaneamente na `db` e na `dbx`, o firmware rejeita a sua execução.

3. **Como é que um atacante em posse da chave privada da Platform Key (`PK`) consegue fazer com que o firmware execute um *bootkit* na partição `ESP` sem desativar o Secure Boot?**

> [!success]- Ver Resposta
> Com a chave privada da `PK`, o atacante assina a adição de uma `KEK` própria no firmware; de seguida, usa a sua `KEK` para assinar e inserir um certificado seu na base `db`. Por fim, assina o *bootkit* com esse certificado e coloca-o na partição `ESP`, passando na verificação do Secure Boot como software legítimo.

## Notas relacionadas

- [[UEFI Secure Boot]]
- [[PKfail - Vulnerabilidade do UEFI Secure Boot]]
- [[PKfail - Cadeia de Ataque e Deteção Forense]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
