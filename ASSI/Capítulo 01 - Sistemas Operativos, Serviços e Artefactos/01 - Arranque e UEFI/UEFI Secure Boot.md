---
title: UEFI Secure Boot
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
  - firmware
aliases:
  - Secure Boot
  - Arranque do Windows
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
atualizado: 2026-09-24
---

# Arranque do Windows e Secure Boot

No arranque do Windows assente em arquiteturas UEFI, todos os componentes da cadeia de boot são validados por assinaturas digitais antes da execução, impedindo o carregamento de binários ou drivers adulterados.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: O sistema operativo não se consegue proteger antes de o seu próprio núcleo (`ntoskrnl.exe`) carregar em memória. O Secure Boot delega no firmware UEFI a validação criptográfica sequencial de cada carregador de arranque antes de lhe passar o controlo do processador.
> * **Porque importa (Forense / Segurança)**: Impede a persistência pré-sistema operativo (*bootkits* e *rootkits* de firmware). Se a raiz de confiança do firmware estiver comprometida (como no caso [[PKfail - Vulnerabilidade do UEFI Secure Boot|PKfail]]), o atacante consegue assinar binários maliciosos que passam na validação como se fossem legítimos.
> * **Pontos Críticos para Exame**:
>   * Na validação assimétrica, a **chave privada** assina o binário (mantida secreta pelo OEM/Microsoft) e a **chave pública** (no certificado gravado no firmware) valida a assinatura.
>   * Ordem estrita da cadeia de arranque: **UEFI Firmware** $\rightarrow$ **UEFI Boot Manager** $\rightarrow$ **Windows Boot Manager** (`bootmgr.efi`) $\rightarrow$ **Windows Boot Loader** (`winload.efi`) $\rightarrow$ **Windows Kernel** (`ntoskrnl.exe`).

---

## Assinatura Digital e Validação de Código

A cadeia de confiança criptográfica baseia-se num sistema de chaves assimétricas:

| Componente Criptográfico | Detentor / Localização | Função Operacional no Arranque |
| :--- | :--- | :--- |
| **Par de Chaves (Privada / Pública)** | Gerado pelo fabricante (OEM / Microsoft) | Base matemática assimétrica que separa a capacidade de assinar da capacidade de verificar. |
| **Chave Privada (Assinatura)** | Mantida em segredo pelo proprietário | Utilizada exclusivamente para assinar digitalmente o executável ou o *hash* do ficheiro. |
| **Certificado Digital (Chave Pública)** | Anexado ao binário e gravado nas bases do firmware | Contém a chave pública do assinante; permite ao firmware UEFI validar a autenticidade e integridade do código. |

* **Validação Universal**: O firmware UEFI utiliza a chave pública contida no certificado (ou gravada nas suas bases de dados fidedignas) para validar a autenticidade e integridade do código. Qualquer entidade consegue validar a assinatura, mas apenas o detentor da chave privada consegue assinar novo código.
* **Risco de Comprometimento da Raiz**: Se a chave privada que o firmware reconhece como raiz de confiança (*Platform Key*) estiver comprometida ou for pública, a validação continuará com sucesso, mas validará binários fornecidos pelo atacante — este é o cerne da vulnerabilidade [[PKfail - Vulnerabilidade do UEFI Secure Boot|PKfail]].

---

## Cadeia de Confiança do Arranque

A cadeia de validação sequencial ocorre nos seguintes estágios:

```text
[1. UEFI Firmware] ──► [2. UEFI Boot Manager] ──► [3. bootmgr.efi] ──► [4. winload.efi] ──► [5. ntoskrnl.exe]
```

1. **UEFI Firmware**: Inicialização do hardware e verificação dos controladores EFI.
2. **UEFI Boot Manager**: Validação do gestor de arranque através das bases de assinaturas do firmware.
3. **Windows Boot Manager** (`bootmgr.efi`): Validação da integridade dos componentes de arranque do sistema operativo.
4. **Windows Boot Loader** (`winload.efi`): Carregamento e validação dos controladores críticos e do núcleo.
5. **Windows Kernel** (`ntoskrnl.exe`): Inicialização do núcleo do sistema operativo e subsequente arranque dos subsistemas.

Cada elo desta cadeia tem de estar obrigatoriamente assinado e validado contra a hierarquia de chaves configurada no firmware ([[UEFI Secure Boot - Chaves e Hierarquia]]).

---

## Além da aula

Em ambientes corporativos com requisitos estritos de segurança, o Secure Boot trabalha em articulação com o módulo TPM (*Trusted Platform Module*) e com o BitLocker. As medições de integridade da cadeia de arranque são gravadas nos registos PCR (*Platform Configuration Registers*) do TPM. Caso ocorra uma alteração não autorizada no firmware ou na Platform Key, o TPM recusa libertar a chave de desencriptação do volume de sistema, exigindo a chave de recuperação do BitLocker.

---

## Perguntas de revisão

1. **No contexto do UEFI Secure Boot, qual é a diferença funcional entre a chave privada e a chave pública no processo de validação de um binário de arranque?**

> [!success]- Ver Resposta
> A **chave privada** é mantida em segredo pelo fabricante (OEM ou Microsoft) e serve exclusivamente para criar a assinatura digital do binário (ou do seu *hash*). A **chave pública** está incluída no certificado digital anexado ao binário e nas bases de dados do firmware UEFI, permitindo a qualquer sistema verificar a autenticidade e integridade do código antes de o executar.

2. **Qual é a sequência exata dos cinco componentes que formam a cadeia de confiança no arranque UEFI do Windows?**

> [!success]- Ver Resposta
> 1. **UEFI Firmware** $\rightarrow$ 2. **UEFI Boot Manager** $\rightarrow$ 3. **Windows Boot Manager** (`bootmgr.efi`) $\rightarrow$ 4. **Windows Boot Loader** (`winload.efi`) $\rightarrow$ 5. **Windows Kernel** (`ntoskrnl.exe`).

3. **Por que motivo um sistema com o Secure Boot ativo continua vulnerável se a chave privada da Platform Key (PK) for divulgada publicamente?**

> [!success]- Ver Resposta
> Porque o mecanismo criptográfico do firmware continuará a verificar as assinaturas normalmente, mas qualquer atacante em posse da chave privada da PK poderá assinar novas chaves e binários maliciosos (*bootkits*) que serão reconhecidos como fidedignos e legítimos pelo UEFI.

## Notas relacionadas

- [[UEFI Secure Boot - Chaves e Hierarquia]]
- [[PKfail - Vulnerabilidade do UEFI Secure Boot]]
- [[Processo de Arranque UEFI, Secure Boot e Fluxo do Windows]]
- [[Arranque Forense e Processo de Boot (BIOS e Código Máquina)]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
