---
title: PKfail - Vulnerabilidade do UEFI Secure Boot
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: vulnerabilidade
tags:
  - cve/cve-2016-5247
  - uefi
  - secure-boot
  - bootkit
aliases:
  - PKfail
  - CVE-2016-5247
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://www.binarly.io/blog/pkfail-untrusted-platform-keys-undermine-secure-boot-on-uefi-ecosystem"
atualizado: 2026-09-24
---

# PKfail — Vulnerabilidade do UEFI Secure Boot

O mecanismo de [[UEFI Secure Boot]] assenta na validação digital de todos os módulos de arranque. No entanto, dezenas de fabricantes de dispositivos e integradores de hardware recorreram a uma chave privada de teste e código de exemplo fornecido pela American Megatrends (AMI) como a chave mestra em produção — a [[UEFI Secure Boot - Chaves e Hierarquia|Platform Key (PK)]].

Esta vulnerabilidade de cadeia de fornecimento de firmware foi designada por **PKfail** e afeta cerca de **850 modelos de computadores** de múltiplos fabricantes que utilizam firmware UEFI baseado na base da AMI.

---

## Mecanismo de Falha e Impacto

O Secure Boot depende da premissa de que a chave privada correspondente ao certificado da Platform Key reside exclusivamente sob custódia segura do fabricante (OEM).

* **Origem da Falha**: A chave privada utilizada para assinar o certificado da Platform Key fazia parte do repositório de código de teste da AMI, tornando-se pública e acessível.
* **Certificado Inválido em Produção**: O certificado da PK emitido pela AMI declara expressamente nos seus campos identificadores que se trata de uma chave não fidedigna:
  * `Issuer: DO NOT TRUST – AMI TEST KEY`
  * `Subject: DO NOT TRUST`
* **Consequência Prática**: Qualquer atacante que obtenha a chave privada pública da AMI pode gerar assinaturas válidas reconhecidas pelo firmware, permitindo **substituir o software de arranque por software malicioso (bootkits)** mantendo a aparência de que o Secure Boot se encontra ativo e funcional.

---

## Identificador e Referência

* **Identificador de Vulnerabilidade**: **CVE-2016-5247** (identificação original associada ao uso de chaves de teste AMI em dispositivos de fabricantes como a Lenovo).
* **Investigação de Referência**: Estudo da Binarly intitulado *PKfail: Untrusted Platform Keys Undermine Secure Boot on UEFI Ecosystem*, que documentou o impacto abrangente do problema no ecossistema UEFI.

---

## Procedimento de Validação em Sistema Ativo

A deteção de vulnerabilidade a PKfail exige auditar a assinatura e o certificado da Platform Key em execução:

1. **Inspeção do Certificado da PK via IsBootSecure**:
   * O utilitário **IsBootSecure** (Gibson Research Corporation) interroga o firmware e analisa o certificado digital da master key / Platform Key.
   * A ferramenta deteta se o Secure Boot está ativo e assinala a vermelho se a Platform Key em vigor pertence à chave de teste não fidedigna da AMI (*"Platform Key should NOT be trusted"*).
2. **Validação Prévia do Binário via Sigcheck**:
   * Como boa prática de administração segura antes de executar qualquer ferramenta de diagnóstico, valida-se o binário com o `sigcheck` (Sysinternals):
     ```cmd
     REM Validar a assinatura Authenticode do executável
     sigcheck.exe isBootSecure.exe

     REM Consultar a pontuação de reputação no VirusTotal (/vt)
     sigcheck.exe /vt isBootSecure.exe
     ```

Para a cadeia completa de exploração e deteção via PowerShell, consulta: [[PKfail - Cadeia de Ataque e Deteção Forense]].

---

## Além da aula

Em julho de 2024, a empresa de segurança Binarly reabriu a investigação do PKfail ao descobrir que centenas de modelos modernos de fabricantes como Acer, ASUS, Dell, HP e Gigabyte continuavam a ser comercializados com a mesma chave de teste da AMI de 2016. Esta reavaliação em larga escala foi catalogada pelo CERT/CC sob a nota de vulnerabilidade VU#455367 e recebeu o identificador **CVE-2024-8105**.

## Notas relacionadas

- [[UEFI Secure Boot]]
- [[UEFI Secure Boot - Chaves e Hierarquia]]
- [[PKfail - Cadeia de Ataque e Deteção Forense]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
