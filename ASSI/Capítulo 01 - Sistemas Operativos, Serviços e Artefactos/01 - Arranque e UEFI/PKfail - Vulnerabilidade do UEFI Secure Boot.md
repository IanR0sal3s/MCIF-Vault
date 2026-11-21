---
title: PKfail - Vulnerabilidade do UEFI Secure Boot
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 1
tipo: conceito
tags:
  - assi
  - cve/cve-2016-5247
  - uefi
  - secure-boot
  - bootkit
  - sigcheck
aliases:
  - PKfail
  - CVE-2016-5247
  - PKfail - Cadeia de Ataque e Deteção Forense
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
fontes:
  - "https://www.binarly.io/blog/pkfail-untrusted-platform-keys-undermine-secure-boot-on-uefi-ecosystem"
  - "https://www.grc.com/isbootsecure.htm"
atualizado: 2026-11-21
---

# PKfail — Vulnerabilidade do UEFI Secure Boot

A vulnerabilidade **PKfail** (**`CVE-2016-5247`**) resulta de vários fabricantes terem utilizado em produção, como [[UEFI Secure Boot|Platform Key (PK)]], uma chave privada de teste incluída no código exemplo da **American Megatrends (AMI)** — afetando cerca de **850 modelos** de computadores com UEFI.

## 1. Causa Raiz e Impacto

* **Chave de teste em produção**: o próprio certificado da PK da AMI declarava explicitamente não dever ser usado em produção:
  * `Issuer`: **`DO NOT TRUST – AMI TEST KEY`**
  * `Subject`: **`DO NOT TRUST`**
* **Consequência**: como a chave privada de exemplo se tornou pública, um atacante pode assinar atualizações das chaves UEFI e **substituir o software de arranque por software malicioso (*bootkits*)**, mantendo o Secure Boot aparentemente ativo.

---

## 2. Verificação Prática (`sigcheck` e `IsBootSecure`)

### 1) Validar o executável com `sigcheck.exe` (Sysinternals)
Antes de correr utilitários descarregados da Internet, valida-se a assinatura digital e a reputação no VirusTotal:

```cmd
:: Validar a assinatura digital Authenticode do executável
sigcheck isBootSecure.exe

:: Consultar a pontuação do ficheiro no VirusTotal (/vt)
sigcheck /vt isBootSecure.exe
```

### 2) Auditar a Platform Key com `IsBootSecure` (GRC)
O utilitário **IsBootSecure** analisa o certificado da *master key* / Platform Key instalada no firmware, indicando se o Secure Boot está ativo e se a `PK` pertence a uma chave de teste não fidedigna.

---

## Além da aula

* **Deteção via PowerShell**: em consola administrativa, `Confirm-SecureBootUEFI` verifica apenas se o Secure Boot está ligado (`True`/`False`); para inspecionar o certificado da `PK` na NVRAM usa-se `Get-SecureBootUEFI -Name PK`.
* **Reavaliação em 2024**: a investigação da Binarly revelou que modelos recentes continuavam afetados pela mesma chave de teste AMI, originando o identificador **`CVE-2024-8105`** (e o script temporário `Updateamipk.ps1` enquanto não existem atualizações de BIOS/UEFI dos fabricantes).

---

## Perguntas de revisão

1. **Qual é a origem da vulnerabilidade PKfail (`CVE-2016-5247`) e que texto identifica o certificado vulnerável?**

> [!success]- Ver Resposta
> Vários fabricantes deixaram em equipamentos de produção a chave privada de teste do código exemplo da AMI (~850 modelos afetados). O certificado vulnerável exibe `Issuer: DO NOT TRUST – AMI TEST KEY` e `Subject: DO NOT TRUST`.

2. **Que comandos `sigcheck` permitem validar o `isBootSecure.exe` antes de o executar?**

> [!success]- Ver Resposta
> `sigcheck isBootSecure.exe` (valida a assinatura digital do binário) e `sigcheck /vt isBootSecure.exe` (consulta a deteção/reputação no VirusTotal).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[UEFI Secure Boot]] | `mesmo bloco` |
| **Seguinte** | [[Processos e linha de comandos no Windows]] | `muda para Bloco 02` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[Preservação do Sistema e Integridade de Dados]] · `AFD1 · Cap. 1`
* [[Exercícios Práticos - Integridade de Dados e Hashes]] · `AFD1 · Cap. 1`
