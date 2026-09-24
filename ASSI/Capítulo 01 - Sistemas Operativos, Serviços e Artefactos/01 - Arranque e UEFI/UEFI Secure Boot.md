---
title: UEFI Secure Boot
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
  - uefi
  - secure-boot
  - firmware
aliases:
  - Secure Boot
  - Arranque do Windows
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
atualizado: 2026-09-24
---

# Arranque do Windows e Secure Boot

No processo de arranque do Windows assente em arquiteturas UEFI, **todos os componentes da cadeia de boot são validados através de assinaturas digitais** antes da sua execução pelo processador. O mecanismo de **Secure Boot** garante que nenhum binário ou controlador adulterado é executado durante o arranque.

## Assinatura Digital e Validação de Código

A cadeia de confiança criptográfica baseia-se num sistema de chaves assimétricas:
* **Par de Chaves (Privada / Pública)**: O desenvolvedor ou fabricante (OEM / Microsoft) gera um par de chaves criptográficas.
* **Assinatura do Binário**: A chave privada é mantida em segredo pelo proprietário e é utilizada para assinar digitalmente o executável (ou o *hash* do ficheiro).
* **Certificado Digital**: O binário assinado inclui o certificado digital do assinante, contendo a respetiva chave pública.
* **Validação Universal**: O firmware UEFI utiliza a chave pública contida no certificado (ou gravada nas suas bases de dados fidedignas) para validar a autenticidade e integridade do código. Qualquer entidade consegue validar a assinatura, mas apenas o detentor da chave privada consegue assinar novo código.

Se a chave privada que o firmware reconhece como raiz de confiança (*Platform Key*) estiver comprometida ou for pública, a validação continuará com sucesso, mas validará binários fornecidos pelo atacante — este é o cerne da vulnerabilidade [[PKfail - Vulnerabilidade do UEFI Secure Boot|PKfail]].

## Cadeia de Confiança do Arranque

A cadeia de validação sequencial ocorre nos seguintes estágios:
1. **UEFI Firmware**: Inicialização do hardware e verificação dos controladores EFI.
2. **UEFI Boot Manager**: Validação do gestor de arranque através das bases de assinaturas do firmware.
3. **Windows Boot Manager** (`bootmgr.efi`): Validação da integridade dos componentes de arranque do sistema operativo.
4. **Windows Boot Loader** (`winload.efi`): Carregamento e validação dos controladores críticos e do núcleo.
5. **Windows Kernel** (`ntoskrnl.exe`): Inicialização do núcleo do sistema operativo e subsequente arranque dos subsistemas.

Cada elo desta cadeia tem de estar obrigatoriamente assinado e validado contra a hierarquia de chaves configurada no firmware ([[UEFI Secure Boot - Chaves e Hierarquia]]).

## Além da aula

Em ambientes corporativos com requisitos estritos de segurança, o Secure Boot trabalha em articulação com o módulo TPM (*Trusted Platform Module*) e com o BitLocker. As medições de integridade da cadeia de arranque são gravadas nos registos PCR (*Platform Configuration Registers*) do TPM. Caso ocorra uma alteração não autorizada no firmware ou na Platform Key, o TPM recusa libertar a chave de desencriptação do volume de sistema, exigindo a chave de recuperação do BitLocker.

## Notas relacionadas

- [[UEFI Secure Boot - Chaves e Hierarquia]]
- [[PKfail - Vulnerabilidade do UEFI Secure Boot]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
