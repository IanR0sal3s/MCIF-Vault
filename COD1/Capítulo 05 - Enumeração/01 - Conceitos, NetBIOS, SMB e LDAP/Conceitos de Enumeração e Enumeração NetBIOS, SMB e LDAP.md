---
title: Conceitos de Enumeração e Enumeração NetBIOS, SMB e LDAP
tipo: tecnica
mestrado: Cibersegurança e Informática Forense
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
capitulo: 5
bloco: 1
fonte_aula: 2026.27_MCIF_COD1_05_Enumeracao.pdf (Slides 3–14, 26–29)
tags: [cod1, enumeracao, netbios, smb, ldap, active-directory, rpcclient, netexec]
aliases: [Enumeração NetBIOS, Enumeração SMB, Enumeração LDAP]
criado: 2026-11-15
atualizado: 2026-11-16
---

# Conceitos de Enumeração e Enumeração NetBIOS, SMB e LDAP

A enumeração estabelece ligações ativas aos serviços descobertos (`NetBIOS`, `SMB`, `LDAP`, `RPC`) para extrair contas de utilizador, grupos, partilhas de rede e políticas de domínio.

> [!TIP] Lógica de Funcionamento e Valor Operacional
> * **Porque existe (Sistema)**: Serviços de diretório e partilha corporativa (`AD`, `SMB`, `NetBIOS`) expõem metadados de rede para interoperabilidade e gestão interna.
> * **Porque importa (Pentesting / Segurança)**: Uma única sessão nula (*null session*) ou consulta LDAP anónima revela listas completas de utilizadores, partilhas e políticas de bloqueio antes de qualquer ataque de credenciais.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * O nome **NetBIOS** tem **16 carateres ASCII** (15 para o nome + 16.º byte para o tipo de registo).
>   * **`139/TCP`** = SMB sobre NetBIOS; **`445/TCP`** = SMB direto sobre TCP; **`389`** = LDAP (codificado em `BER`); **`3268`** = Global Catalog AD.

## 1. Conceito de Enumeração e Portos Críticos

A **Enumeração** consiste em estabelecer ligações ativas aos sistemas descobertos no scanning e efetuar consultas diretas (frequentemente em ambiente intranet ou perímetro exposto) para extrair:
- Recursos e **partilhas de rede**, nomes das máquinas.
- **Utilizadores e grupos** de utilizadores, políticas de passwords.
- Tabelas de encaminhamento, configurações de serviços, dados `SNMP`/`DNS`, aplicações e banners.

| Porto / Protocolo | Serviço | Alvo Principal de Enumeração |
| :--- | :--- | :--- |
| **`TCP 25`** | SMTP | Validação de contas de utilizador (`VRFY`, `EXPN`, `RCPT TO`). |
| **`TCP/UDP 53`** | DNS | Transferência de zona (`AXFR`) e registos internos. |
| **`TCP/UDP 135`** | Microsoft RPC Endpoint Mapper | Serviços RPC registados no host Windows. |
| **`UDP 137`** | NetBIOS Name Service (NBNS) | Tabela de nomes NetBIOS, domínio/workgroup e MAC. |
| **`TCP 139`** | NetBIOS Session Service (SMB-NB) | Sessões SMB sobre NetBIOS, partilhas e utilizadores. |
| **`UDP 161` / `162`** | SNMP / SNMP Trap | Utilizadores, processos, software, interfaces e rotas. |
| **`TCP/UDP 389`** | LDAP | Diretório corporativo / Active Directory (utilizadores, grupos, OUs). |
| **`TCP/UDP 445`** | SMB over TCP (Direct Host) | Partilhas, ficheiros, utilizadores, políticas via RPC/SMB. |
| **`TCP/UDP 3268`** | Global Catalog Service (AD) | Consultas globais multi-domínio em Active Directory. |

## 2. Enumeração NetBIOS

O **nome NetBIOS** é uma string única de **16 carateres ASCII** sobre TCP/IP: os primeiros 15 carateres identificam o dispositivo/serviço e o 16.º byte indica o tipo de registo. Permite obter listas de hosts de um domínio, partilhas, políticas e informações de passwords.

- **Ferramentas CLI e Nmap:**
  ```bash
  # Kali Linux: varrer sub-rede para nomes NetBIOS e MACs
  nbtscan -r 192.168.1.0/24

  # Nmap NSE script
  nmap -sV --script nbstat -v <IP>
  ```
- **Windows (`nbtstat`, `net`, `PsTools`):**
  - `nbtstat -c` (cache local de nomes NetBIOS) e `nbtstat -a <IP_remoto>` (tabela de nomes NetBIOS remota).
  - Utilitários `net`: `net view [\\computer] [/ALL]`, `net view /DOMAIN`, `net localgroup`, `net share [sharename]`, `net statistics`, `net accounts`.
  - **Suite Microsoft Sysinternals `PsTools`:** `PsGetSid` (SIDs), `PsLoggedOn` (utilizadores ligados), `PsInfo` (info de sistema), `PsExec` (execução remota), `PsList` (processos), `PsFile` (ficheiros abertos remotamente), `PsPassword` (alteração de passwords).

## 3. Enumeração LDAP e SMB

O **LDAP** (*Lightweight Directory Access Protocol*, porto `389`) acede a serviços de diretório hierárquicos (como o Active Directory) através de pedidos codificados em **BER** (*Basic Encoding Rules*), permitindo consultar usernames válidos, grupos e estrutura organizacional.

### Comandos Práticos de Enumeração SMB / RPC / LDAP
```bash
# Enumeração abrangente SMB/NetBIOS/LDAP
enum4linux -a <IP>
enum4linux-ng -A <IP>

# Scripts Nmap NSE para SMB
nmap -sS -p 445 <IP> --script smb-enum-users,smb-enum-groups,smb-enum-domains,smb-enum-shares

# NetExec (nxc) - testar null session e listar partilhas/utilizadores
nxc smb <IP> -u '' -p '' --shares --users

# RPCClient com sessão nula
rpcclient -U "" -N <IP>
# Dentro do rpcclient: querydominfo | enumdomusers | netshareenum | queryuser <user> | srvinfo

# Consultas LDAP anónimas (descobrir namingContexts / Base DN)
ldapsearch -x -H ldap://<IP> -s base
ldapsearch -x -H ldap://<IP> -b "" -s base namingContexts
```
- **Em Windows / AD:** comandos nativos `net user [/DOMAIN]`, `net user <username> [/DOMAIN]`, `net group /DOMAIN` e a suite **PowerView** (`PowerSploit/Recon`).

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Dica prática para pentests em redes Active Directory:

- **Enumeração de Política de Password antes de Password Spraying:** Antes de testar qualquer password via SMB/LDAP, extraia sempre a política de bloqueio (`enum4linux-ng`, `rpcclient -> getdompwinfo`, ou `nxc smb <IP> -u user -p pass --pass-pol`) para saber o *Account Lockout Threshold*. Testar passwords às cegas sem verificar o threshold pode bloquear dezenas de contas corporativas reais durante a auditoria.

## Perguntas de revisão

1. **Qual a diferença entre os portos `139/TCP` e `445/TCP` na enumeração SMB?**
   > [!success]- Ver Resposta
   > O porto `139/TCP` transporta SMB encapsulado sobre sessão NetBIOS (*NetBIOS Session Service*), enquanto o porto `445/TCP` executa SMB diretamente sobre TCP (*Direct Host*), sendo o padrão em sistemas Windows modernos.

2. **Que informação se obtém com `ldapsearch -x -H ldap://<IP> -b "" -s base namingContexts`?**
   > [!success]- Ver Resposta
   > Obtém-se a raiz do diretório (*Base DN* / `namingContexts`, como `DC=empresa,DC=local`), necessária como ponto de partida para consultar utilizadores, grupos e objetos dentro da árvore LDAP/Active Directory.

## Notas relacionadas
- [[Enumeração SNMP (Community Strings, MIB e OIDs)]]
- [[Enumeração SMTP, DNS, FTP, IPsec e VoIP (SIP)]]
- [[Contramedidas de Enumeração e Metodologia Pentest]]
- [[Cheat Sheet - Enumeração de Serviços e Portos]]
