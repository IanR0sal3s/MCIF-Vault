---
title: PKfail - Cadeia de Ataque e Deteção Forense
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 1
tipo: procedimento
tags:
  - assi
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

A exploração da vulnerabilidade [[PKfail - Vulnerabilidade do UEFI Secure Boot|PKfail]] permite a um atacante usar a chave privada pública da Platform Key (AMI) para injetar certificados próprios no firmware e executar *bootkits* antes do kernel do Windows, contornando o [[UEFI Secure Boot]].

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: O UEFI permite atualizar as variáveis autenticadas da NVRAM (`KEK`, `db`, `dbx`) a partir do sistema operativo (com privilégios de Administrador) desde que o pedido de atualização venha assinado pela chave privada da `PK` instalada.
> * **Porque importa (Forense / Segurança)**: Verificar apenas se o Secure Boot está ativo (`Confirm-SecureBootUEFI` = `True`) é insuficiente numa perícia forense; é obrigatório inspecionar o certificado da `PK` (`Get-SecureBootUEFI -Name PK`) para despistar a presença da chave `DO NOT TRUST – AMI TEST KEY`.
> * **Pontos Críticos para Exame**:
>   * Cadeia de ataque em 4 passos: **Chave Privada PK AMI** $\rightarrow$ assina **KEK do atacante** $\rightarrow$ assina **Certificado na `db`** $\rightarrow$ valida **Bootkit na partição `ESP`**.
>   * Comandos PowerShell de auditoria: `Confirm-SecureBootUEFI` (estado booleano) e `Get-SecureBootUEFI -Name PK` (extração do certificado na NVRAM).

---

## A Cadeia de Ataque (*Exploit Chain*)

O impacto central da vulnerabilidade [[PKfail - Vulnerabilidade do UEFI Secure Boot|PKfail]] reside no facto de que **o conhecimento da chave privada da Platform Key permite a um atacante substituir o software de arranque legítimo por software malicioso**. Para consolidar a persistência abaixo do sistema operativo sem despoletar erros de validação no arranque, o atacante segue uma cadeia de quatro passos:

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

### Requisitos Operacionais do Ataque

1. **Posse da chave privada da PK**: obtida a partir dos repositórios de código de exemplo da AMI.
2. **Capacidade de escrita em variáveis NVRAM autenticadas**: requer acesso com privilégios de administrador local ou interação física com o menu de configuração do firmware (*Setup Utility*).
3. **Execução Pré-Kernel**: O código malicioso inserido corre durante o arranque antes do carregamento do núcleo do Windows (`ntoskrnl.exe`), permitindo desativar controlos de segurança, injetar código no kernel ou estabelecer persistência oculta a antivírus e EDRs.

---

## Procedimento de Deteção e Auditoria Forense

Num exame pericial a um computador suspeito, a simples verificação do estado "Secure Boot: Ativado" é insuficiente para garantir a integridade da plataforma. É indispensável inspecionar a **identidade do certificado da Platform Key**.

### 1. Deteção via PowerShell (Nativo)

Numa sessão administrativa do PowerShell, pode consultar-se o estado e extrair os dados da PK:

#### Anatomia dos Comandos PowerShell

| Cmdlet / Parâmetro | Função Forense | Resultado Esperado / IoC |
| :--- | :--- | :--- |
| `Confirm-SecureBootUEFI` | Verifica se o mecanismo UEFI Secure Boot está ativo no firmware. | Devolve `True` (ativo) ou `False` (desativado). Não deteta chaves comprometidas por si só. |
| `Get-SecureBootUEFI -Name PK` | Extrai os bytes e metadados da variável NVRAM correspondente à Platform Key (`PK`). | **IoC Crítico**: Presença da string `DO NOT TRUST – AMI TEST KEY` ou `DO NOT TRUST - AMI Test PK` nos campos *Issuer* / *Subject*. |

```powershell
# Verificar se o Secure Boot está funcional
Confirm-SecureBootUEFI

# Extrair a assinatura e o certificado da Platform Key configurada no NVRAM
Get-SecureBootUEFI -Name PK
```

* **Indicador de Comprometimento (IoC)**: Se o campo *Issuer* ou *Subject* contiver a designação `DO NOT TRUST – AMI TEST KEY` ou `DO NOT TRUST - AMI Test PK`, o dispositivo está em risco crítico de execução de bootkits arbitrários.

### 2. Triagem com `IsBootSecure` e `Sigcheck`

**1. Validação do Utilitário de Teste:**

Antes de executar utilitários de terceiros na máquina periciada, valida-se a sua assinatura e reputação:

```cmd
sigcheck.exe isBootSecure.exe
sigcheck.exe /vt isBootSecure.exe
```

**2. Execução do IsBootSecure:**

O programa analisa diretamente o certificado do firmware e apresenta o diagnóstico gráfico:

* *Verde*: Secure Boot ativo com uma Platform Key fidedigna do fabricante.
* *Vermelho*: Secure Boot ativo mas assente numa chave de teste da AMI (`Platform Key should NOT be trusted`).

---

## Além da aula

A resolução definitiva da vulnerabilidade exige que os fabricantes OEM publiquem atualizações de BIOS/UEFI contendo Platform Keys privadas exclusivas e novos certificados de produção. Como medida temporária de mitigação em parques empresariais onde não existam atualizações de BIOS disponíveis, a Microsoft e o CERT/CC disponibilizaram o script `Updateamipk.ps1`, que substitui a PK de teste por uma chave segura. Contudo, repor as definições de fábrica da BIOS em muitos modelos pode restaurar novamente a PK vulnerável da AMI.

---

## Perguntas de revisão

1. **Quais são os quatro passos sequenciais da cadeia de ataque (*exploit chain*) do PKfail até à execução de um *bootkit*?**

> [!success]- Ver Resposta
> 1. O atacante usa a chave privada da PK de teste da AMI para assinar e acrescentar uma nova `KEK` controlada por si.
> 2. Com a sua `KEK`, assina e adiciona um certificado próprio à base de dados de assinaturas autorizadas (`db`).
> 3. Assina o módulo malicioso (*bootkit*) com esse certificado e copia-o para a partição EFI de sistema (`ESP`).
> 4. No reinício do sistema, o UEFI Secure Boot valida o *bootkit* com sucesso contra a `db` e executa-o antes do `ntoskrnl.exe`.

2. **Por que razão o comando PowerShell `Confirm-SecureBootUEFI` é insuficiente numa auditoria forense ao PKfail e que comando adicional deve ser executado?**

> [!success]- Ver Resposta
> Porque `Confirm-SecureBootUEFI` apenas devolve `True` se a verificação do Secure Boot estiver ligada, não validando a idoneidade criptográfica da chave raiz. É obrigatório executar `Get-SecureBootUEFI -Name PK` para inspecionar o certificado na NVRAM e confirmar se contém o indicador `DO NOT TRUST – AMI TEST KEY`.

3. **Que privilégios ou condições operacionais são necessários numa máquina vulnerável a PKfail para que o atacante consiga modificar as variáveis da NVRAM?**

> [!success]- Ver Resposta
> O atacante necessita da chave privada da PK de teste da AMI e de capacidade de escrita nas variáveis NVRAM autenticadas do UEFI, o que exige privilégios de **Administrador local** no sistema operativo ou acesso físico ao menu de configuração do firmware (*Setup Utility*).

## Notas relacionadas

- [[UEFI Secure Boot]]
- [[UEFI Secure Boot - Chaves e Hierarquia]]
- [[PKfail - Vulnerabilidade do UEFI Secure Boot]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Exercícios Práticos - Integridade de Dados e Hashes]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
