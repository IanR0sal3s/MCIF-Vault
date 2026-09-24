---
title: PKfail - Cadeia de Ataque e Deteção Forense
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: procedimento
tags:
  - bootkit
  - forense
  - uefi
  - powershell
aliases:
  - PKfail Exploit Chain
  - Deteção PKfail
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://www.grc.com/isbootsecure.htm"
  - "https://learn.microsoft.com/en-us/sysinternals/downloads/sigcheck"
atualizado: 2026-09-24
---

# PKfail: Cadeia de Ataque e Deteção Forense

O impacto central da vulnerabilidade [[PKfail - Vulnerabilidade do UEFI Secure Boot|PKfail]] reside no facto de que **o conhecimento da chave privada da Platform Key permite a um atacante substituir o software de arranque legítimo por software malicioso**. Ao deter a chave de topo da hierarquia, o atacante adquire a capacidade de contornar todas as restrições impostas pelo [[UEFI Secure Boot]].

---

## A Cadeia de Ataque (*Exploit Chain*)

Para consolidar a persistência abaixo do sistema operativo sem despoletar erros de validação no arranque, o atacante segue uma cadeia de quatro passos:

```text
[Chave Privada da PK de Teste AMI]
                │
                ▼ (1) Assina e acrescenta nova KEK
       [KEK do Atacante]
                │
                ▼ (2) Assina e adiciona certificado à Signature Database (db)
 [Certificado do Atacante na 'db']
                │
                ▼ (3) Assina módulo malicioso (bootkit) e copia para a partição ESP
         [Bootkit na ESP]
                │
                ▼ (4) Reinício do sistema alvo
   [UEFI Secure Boot valida bootkit com sucesso contra a 'db' -> Execução]
```

### Requisitos Operacionais do Ataque:
1. **Posse da chave privada da PK**: obtida a partir dos repositórios de código de exemplo da AMI.
2. **Capacidade de escrita em variáveis NVRAM autenticadas**: requer acesso com privilégios de administrador local ou interação física com o menu de configuração do firmware (*Setup Utility*).
3. **Execução Pré-Kernel**: O código malicioso inserido corre durante o arranque antes do carregamento do núcleo do Windows (`ntoskrnl.exe`), permitindo desativar controlos de segurança, injetar código no kernel ou estabelecer persistência oculta a antivírus e EDRs.

---

## Procedimento de Deteção e Auditoria Forense

Num exame pericial a um computador suspeito, a simples verificação do estado "Secure Boot: Ativado" é insuficiente para garantir a integridade da plataforma. É indispensável inspecionar a **identidade do certificado da Platform Key**.

### 1. Deteção via PowerShell (Nativo)

Numa sessão administrativa do PowerShell, pode consultar-se o estado e extrair os dados da PK:

```powershell
# Verificar se o Secure Boot está funcional
Confirm-SecureBootUEFI

# Extrair a assinatura e o certificado da Platform Key configurada no NVRAM
Get-SecureBootUEFI -Name PK
```

* **Indicador de Comprometimento (IoC)**: Se o campo *Issuer* ou *Subject* contiver a designação `DO NOT TRUST – AMI TEST KEY` ou `DO NOT TRUST - AMI Test PK`, o dispositivo está em risco crítico de execução de bootkits arbitrários.

### 2. Triagem com IsBootSecure e Sigcheck

1. **Validação do Utilitário de Teste**:
   Antes de executar utilitários de terceiros na máquina periciada, valida-se a sua assinatura e reputação:
   ```cmd
   sigcheck.exe isBootSecure.exe
   sigcheck.exe /vt isBootSecure.exe
   ```
2. **Execução do IsBootSecure**:
   O programa analisa diretamente o certificado do firmware e apresenta o diagnóstico gráfico:
   * *Verde*: Secure Boot ativo com uma Platform Key fidedigna do fabricante.
   * *Vermelho*: Secure Boot ativo mas assente numa chave de teste da AMI (`Platform Key should NOT be trusted`).

---

## Além da aula

A resolução definitiva da vulnerabilidade exige que os fabricantes OEM publiquem atualizações de BIOS/UEFI contendo Platform Keys privadas exclusivas e novos certificados de produção. Como medida temporária de mitigação em parques empresariais onde não existam atualizações de BIOS disponíveis, a Microsoft e o CERT/CC disponibilizaram o script `Updateamipk.ps1`, que substitui a PK de teste por uma chave segura. Contudo, repor as definições de fábrica da BIOS em muitos modelos pode restaurar novamente a PK vulnerável da AMI.

## Notas relacionadas

- [[UEFI Secure Boot]]
- [[UEFI Secure Boot - Chaves e Hierarquia]]
- [[PKfail - Vulnerabilidade do UEFI Secure Boot]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
