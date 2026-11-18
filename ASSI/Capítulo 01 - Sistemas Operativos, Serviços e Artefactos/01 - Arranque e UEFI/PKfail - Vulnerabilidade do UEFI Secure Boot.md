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
aliases:
  - PKfail
  - CVE-2016-5247
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://www.binarly.io/blog/pkfail-untrusted-platform-keys-undermine-secure-boot-on-uefi-ecosystem"
atualizado: 2026-09-24
---

# PKfail — Vulnerabilidade do UEFI Secure Boot

A vulnerabilidade **PKfail** (**CVE-2016-5247**) resulta da utilização, em produção por dezenas de fabricantes, de uma chave privada de teste da American Megatrends (AMI) como [[UEFI Secure Boot - Chaves e Hierarquia|Platform Key (PK)]] mestra do [[UEFI Secure Boot]].

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Durante o desenvolvimento de firmware UEFI, a AMI forneceu aos fabricantes OEM código de referência com uma Platform Key de teste pré-gerada (`DO NOT TRUST – AMI TEST KEY`) que deveria ser substituída antes da comercialização, mas cerca de 850 modelos foram distribuídos com essa chave intacta.
> * **Porque importa (Forense / Segurança)**: Como a chave privada da AMI se tornou pública, qualquer atacante pode assinar atualizações de chaves UEFI e substituir o software de arranque por *bootkits* mantendo o indicador do Secure Boot como "Ativo".
> * **Pontos Críticos para Exame**:
>   * Identificadores no certificado vulnerável: `Issuer: DO NOT TRUST – AMI TEST KEY` e `Subject: DO NOT TRUST` (associado ao **CVE-2016-5247** e reavaliado em **CVE-2024-8105**).
>   * Antes de executar o utilitário de diagnóstico **IsBootSecure**, deve validar-se a sua assinatura Authenticode e reputação no VirusTotal usando o **`sigcheck.exe`** (Sysinternals).

---

## Mecanismo de Falha e Impacto

O Secure Boot depende da premissa de que a chave privada correspondente ao certificado da Platform Key reside exclusivamente sob custódia segura do fabricante (OEM). Esta vulnerabilidade de cadeia de fornecimento de firmware afeta cerca de **850 modelos de computadores** de múltiplos fabricantes que utilizam firmware UEFI baseado na base da AMI.

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

### 1. Validação Prévia do Binário via `sigcheck` (Sysinternals)
Como boa prática de administração segura antes de executar qualquer ferramenta de diagnóstico em linha de comandos, valida-se o binário com o `sigcheck`:

#### Anatomia do Comando (`sigcheck.exe`)

```cmd
sigcheck.exe [/vt] <caminho_do_executavel>
```

* Sem parâmetros adicionais: verifica a assinatura digital **Authenticode**, a cadeia de certificação, a versão e a data do binário.
* **`/vt`**: submete o *hash* do ficheiro à API do **VirusTotal** para consultar o rácio de deteções de motores antivírus.

```cmd
REM Validar a assinatura Authenticode do executável
sigcheck.exe isBootSecure.exe

REM Consultar a pontuação de reputação no VirusTotal (/vt)
sigcheck.exe /vt isBootSecure.exe
```

### 2. Inspeção do Certificado da PK via `IsBootSecure`

* O utilitário **IsBootSecure** (Gibson Research Corporation) interroga o firmware e analisa o certificado digital da master key / Platform Key.
* A ferramenta deteta se o Secure Boot está ativo e assinala a vermelho se a Platform Key em vigor pertence à chave de teste não fidedigna da AMI (*"Platform Key should NOT be trusted"*).

Para a cadeia completa de exploração e deteção via PowerShell, consulta: [[PKfail - Cadeia de Ataque e Deteção Forense]].

---

## Além da aula

Em julho de 2024, a empresa de segurança Binarly reabriu a investigação do PKfail ao descobrir que centenas de modelos modernos de fabricantes como Acer, ASUS, Dell, HP e Gigabyte continuavam a ser comercializados com a mesma chave de teste da AMI de 2016. Esta reavaliação em larga escala foi catalogada pelo CERT/CC sob a nota de vulnerabilidade VU#455367 e recebeu o identificador **CVE-2024-8105**.

---

## Perguntas de revisão

1. **Qual é a causa raiz da vulnerabilidade PKfail (CVE-2016-5247) e que valores surgem nos campos `Issuer` e `Subject` do certificado vulnerável?**

> [!success]- Ver Resposta
> A falha decorre de fabricantes OEM terem deixado em equipamentos de produção a chave mestra de teste da American Megatrends (AMI), cuja chave privada é pública. O certificado vulnerável apresenta `Issuer: DO NOT TRUST – AMI TEST KEY` e `Subject: DO NOT TRUST`.

2. **Que comandos devem ser executados para verificar a autenticidade e reputação do utilitário `isBootSecure.exe` antes de o correr num sistema auditado?**

> [!success]- Ver Resposta
> Utiliza-se a ferramenta `sigcheck.exe` da suite Sysinternals:
> 1. `sigcheck.exe isBootSecure.exe` (para validar a assinatura digital Authenticode do binário).
> 2. `sigcheck.exe /vt isBootSecure.exe` (para consultar a reputação do ficheiro no VirusTotal).

3. **Qual é o impacto prático do PKfail num equipamento cujo diagnóstico do sistema operativo indica que o UEFI Secure Boot está "Ativo"?**

> [!success]- Ver Resposta
> Apesar de o Secure Boot estar formalmente ativo, a proteção é ilusória: qualquer atacante que possua a chave privada pública de teste da AMI pode assinar *bootkits* ou modificar as bases de dados de arranque (`KEK`, `db`), executando código malicioso no arranque sem gerar alertas de violação criptográfica.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[UEFI Secure Boot - Chaves e Hierarquia]] | `mesmo bloco` |
| **Seguinte** | [[PKfail - Cadeia de Ataque e Deteção Forense]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[UEFI Secure Boot]] · `mesmo bloco`
* [[Preservação do Sistema e Integridade de Dados]] · `AFD1 · Cap. 1`
