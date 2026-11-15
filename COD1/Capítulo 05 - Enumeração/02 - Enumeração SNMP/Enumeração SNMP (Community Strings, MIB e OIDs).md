---
title: "Enumeração SNMP (Community Strings, MIB e OIDs)"
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
tipo: nota
capitulo: 5
topico: enumeracao-snmp
tags: [cod1, enumeracao, snmp, mib, oid, snmpwalk, onesixtyone]
---
# Enumeração SNMP (Community Strings, MIB e OIDs)

**Capítulo:** [[Capítulo 5 - Enumeração]]

> [!TIP] Lógica de Funcionamento e Valor Operacional
> O `SNMP` (`UDP 161`) é frequentemente esquecido pelos administradores com versões antigas (`v1`/`v2c`) e *community strings* padrão (`public` / `private`). Quando exposto, funciona como um raio-X completo do sistema: devolve utilizadores locais, processos em execução, software instalado, portos abertos e tabelas de encaminhamento sem precisar de credenciais de sistema operativo.

## 1. Arquitetura SNMP e *Community Strings*

O protocolo **SNMP** (*Simple Network Management Protocol*) baseia-se em dois componentes:
- **Agente SNMP:** Corre no dispositivo gerido (router, switch, servidor Windows/Linux, impressora).
- **Gestor SNMP:** Aplicação central que consulta ou altera configurações no agente.

Nas versões `SNMPv1` e `SNMPv2c`, a autenticação resume-se a palavras-passe enviadas em texto claro chamadas **community strings**:
- **`read community string` (omissão: `public`):** Permite consultar configurações e métricas do host.
- **`read/write community string` (omissão: `private`):** Permite **modificar remotamente** configurações do dispositivo.

**Informação obtida via enumeração SNMP:** contas de utilizadores, hosts, routers, dispositivos, partilhas, tabelas ARP, tabelas de encaminhamento e estatísticas de tráfego.

## 2. MIB (*Management Information Base*) e OIDs Relevantes

A **MIB** é uma base de dados virtual hierárquica que contém descrições formais de todos os objetos geridos pelo SNMP, traduzindo identificadores numéricos (**OID** — *Object Identifier*) para formato legível por humanos. Cada objeto define tipo (contador, string, endereço), permissões (inacessível, leitura, leitura/escrita), restrições de tamanho e intervalo.

| OID | Informação Devolvida |
| :--- | :--- |
| `1.3.6.1.2.1.25.1.6.0` | Processos do sistema |
| `1.3.6.1.2.1.25.4.2.1.2` | Programas em execução |
| `1.3.6.1.2.1.25.4.2.1.4` | Caminho (*Path*) dos processos |
| `1.3.6.1.2.1.25.2.3.1.4` | Unidades de armazenamento |
| `1.3.6.1.2.1.25.6.2.1.2` | Nome do software instalado |
| `1.3.6.1.4.1.77.1.2.25` | Utilizadores Windows |
| `1.3.6.1.2.1.6.13.1.3` | Portos locais TCP à escuta |

*(Referência de OIDs: `oidref.com/1` e browsers MIB como `mibble` / `dnsstuff.com/mib-browsers`.)*

## 3. Ferramentas e Comandos de Enumeração SNMP

```bash
# Descobrir community strings válidas por dicionário (muito rápido)
onesixtyone -c /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt <IP>
onesixtyone <IP> public

# Enumeração estruturada legível (utilizadores, processos, rede, software)
snmp-check -c public -v 1 <IP>

# Walk completo ou dirigido a um OID específico (ex.: utilizadores Windows)
snmpwalk -c public -v1 -t 10 <IP>
snmpwalk -c public -v2c <IP> 1.3.6.1.4.1.77.1.2.25

# Scripts Nmap NSE para SNMP
nmap --script-help "snmp-*"
sudo nmap -sU -p 161 <IP> --script="snmp*"
```

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Impacto prático em pentests corporativos:

- **Descoberta de credenciais em parâmetros de processos:** Como o OID `1.3.6.1.2.1.25.4.2.1.5` (argumentos de linha de comando dos processos, complementar ao `.4` do path) e o `1.3.6.1.2.1.25.4.2.1.2` expõem processos em execução, é comum encontrar scripts ou comandos lançados com passwords na linha de comando via SNMP.
- **SNMP `private` (Read-Write):** Se `onesixtyone` encontrar uma string de escrita (`private`), o auditor deve reportá-la com severidade **Alta/Crítica**, pois em routers/switches Cisco ou servidores pode permitir extrair configurações completas ou alterar rotas/ACLs.

## Perguntas de revisão

1. **Qual a função da `MIB` no protocolo SNMP?**
   > [!success]- Ver Resposta
   > A `MIB` (*Management Information Base*) é a base de dados hierárquica que define formalmente cada objeto gerido (tipo, permissões, intervalo) e traduz os identificadores numéricos (`OID`) para nomes legíveis.

2. **Qual a diferença prática entre as *community strings* padrão `public` e `private`?**
   > [!success]- Ver Resposta
   > `public` é a community string padrão de apenas leitura (*read-only*, consulta de estado/dados), enquanto `private` é a padrão de leitura e escrita (*read/write*, permitindo alterar configurações remotamente).

## Notas relacionadas
- [[Conceitos de Enumeração e Enumeração NetBIOS, SMB e LDAP]]
- [[Contramedidas de Enumeração e Metodologia Pentest]]
- [[Cheat Sheet - Enumeração de Serviços e Portos]]
