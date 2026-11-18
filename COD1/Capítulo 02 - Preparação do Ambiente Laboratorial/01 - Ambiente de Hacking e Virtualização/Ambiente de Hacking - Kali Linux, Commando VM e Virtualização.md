---
title: Ambiente de Hacking - Kali Linux, Commando VM e Virtualização
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
capitulo: 2
bloco: 1
fonte_aula: 2026.27_MCIF_COD1_02_Preparação_Ambiente.pdf (Slides 2–9)
tags: [cod1, kali-linux, virtualizacao, commando-vm, ferramentas]
aliases: [Kali Linux COD1, Commando-VM, Ambiente de Hacking]
criado: 2026-11-15
atualizado: 2026-11-16
---

# Ambiente de Hacking - Kali Linux, Commando VM e Virtualização

Um laboratório de *pentesting* isolado recorre a máquinas virtuais (`VMware`, `VirtualBox`, `Hyper-V`), contentores (`Docker`) e distribuições ofensivas dedicadas como `Kali Linux` ou `Commando-VM`.

> [!TIP] Lógica de Funcionamento e Valor Operacional
> * **Porque existe (Sistema)**: Isola ferramentas ofensivas potencialmente destrutivas ou ruidosas do sistema anfitrião e permite reverter estados limpos através de *snapshots*.
> * **Porque importa (Pentesting / Segurança)**: Permite testar exploits, simular redes inteiras (atacante + alvos) e manter separação entre auditorias de clientes diferentes.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Credenciais padrão da VM oficial de Kali Linux: **`kali` / `kali`** (alterar após o primeiro arranque).
>   * Em `Hyper-V`, problemas de resolução/clipboard resolvem-se verificando o **Enhanced Session Mode** e daemons de integração.
>   * `Commando-VM` complementa o `Kali` quando o alvo depende de ferramentas nativas Windows / `PowerShell` / Active Directory.

## 1. Requisitos, Virtualização e Contentores

Para montar um laboratório funcional de testes de penetração, o ambiente baseia-se em:

- **Hardware e Virtualização:** Um anfitrião com recursos suficientes (CPU com suporte de virtualização VT-x/AMD-V, RAM adequada para correr múltiplas VMs em simultâneo e armazenamento SSD). Hipervisores comuns incluem `VirtualBox`, `VMware` e `Hyper-V`.
- **Contentores (`Docker`):** Úteis para levantar rapidamente serviços vulneráveis ou ferramentas isoladas sem o peso de uma VM completa.
- **Scripting:** Domínio de linguagens de automação é indispensável para adaptar exploits, automatizar enumeração e processar outputs:
  - `Python` (scripts multiplataforma, sockets, parsing, automação).
  - `Bash` (automação rápida em Linux e encadeamento de ferramentas CLI).
  - `PowerShell` (essencial em ambientes Windows e pós-exploração em Active Directory).

## 2. Distribuições Especializadas para Pentesting

| Plataforma | Sistema / Foco | Descrição Operacional |
| :--- | :--- | :--- |
| **Kali Linux** | Linux (Debian) — Geral | Distribuição padrão da indústria (Offensive Security); inclui centenas de ferramentas pré-configuradas. Credenciais padrão da VM: `kali` / `kali`. |
| **Parrot OS** | Linux (Debian) — Segurança e Privacidade | Alternativa leve ao Kali (Security Edition), com foco adicional em privacidade e desenvolvimento. |
| **BackBox** | Linux (Ubuntu) — Avaliação de Segurança | Focada em análise de vulnerabilidades e testes de penetração com ambiente desktop leve. |
| **SamuraiWTF** | Linux — Aplicações Web | Ambiente pré-configurado especificamente para Web Testing Framework. |
| **Wifislax** | Linux (Slackware) — Wireless | Especializada em auditoria e cracking de redes Wi-Fi. |
| **ArchStrike** | Linux (Arch) — Avançado | Repositório e ambiente rolling-release para utilizadores avançados de Arch Linux. |
| **Network Security Toolkit (NST)** | Linux (Fedora) — Rede | Focada em análise de tráfego, monitorização e diagnóstico de rede. |
| **Attify OS** | Linux — IoT | Especializada em auditoria de segurança de dispositivos Internet of Things (firmware, rádio, hardware). |
| **Commando-VM** | Windows — Pentest / Red Team | Conjunto de scripts de instalação para transformar uma VM Windows numa estação ofensiva (útil para testar alvos Windows/AD). |
| **Pentestbox** | Windows — Portátil | Ambiente portátil baseado em Windows sem necessidade de VM Linux dedicada. |

## 3. Configuração e Troubleshooting Comum (Kali Linux e Hyper-V)

- Ao importar uma imagem oficial de VM do Kali Linux, as credenciais iniciais padrão são utilizador `kali` e palavra-passe `kali` (devendo ser alteradas imediatamente após o primeiro boot num ambiente partilhado).
- **Hyper-V (Windows):** Caso ocorram problemas de resolução de ecrã, partilha de área de transferência (*clipboard*) ou integração de rato, deve verificar-se a configuração do **Enhanced Session Mode** e os serviços de integração (`hyperv-daemons` / `xrdp`) na VM convidada.

## 4. Categorias de Ferramentas Essenciais do Laboratório

- **Reconhecimento e OSINT:** `Spiderfoot` (automação de recolha OSINT).
- **Análise de Rede e Tráfego:** `Wireshark` (captura e inspeção profunda de pacotes).
- **Cracking de Credenciais:** `John the Ripper` e `hashcat` (ataques a hashes offline por dicionário, regras ou força bruta em GPU/CPU).
- **Testes Web:** `Burp Suite` (proxy de interceção HTTP/HTTPS, manipulação de pedidos e scanning web).
- **Engenharia Reversa:** `Ghidra` (descompilador e disassembler desenvolvido pela NSA para análise de binários e malware).

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> As práticas abaixo complementam a preparação laboratorial para cenários reais de pentesting organizacional.

- **Gestão de Snapshots antes de cada Engagement:** Criar sempre um *snapshot* limpo (`Clean-Base`) após atualizar a VM (`sudo apt update && sudo apt full-upgrade`), e um *snapshot* por cliente/projeto, evitando contaminação de logs, cookies, chaves SSH ou artefactos entre auditorias.
- **Redes Isoladas de Laboratório:** Para testar ferramentas destrutivas ou serviços vulneráveis (ex.: Metasploitable, DVWA, Active Directory labs), configurar uma rede virtual **Host-Only** ou **Internal Network** (NAT Network isolada) sem rota para a rede corporativa real.
- **Organização de Diretórios por Alvo:** Estruturar `/home/kali/engagements/<cliente>/` com subpastas fixas (`recon/`, `scans/`, `enum/`, `exploits/`, `loot/`, `evidence/`, `report/`) para manter evidências rastreáveis durante todo o pentest.

## Perguntas de revisão

1. **Qual a principal vantagem de manter `Commando-VM` em paralelo com `Kali Linux` num laboratório?**
   > [!success]- Ver Resposta
   > Enquanto o `Kali Linux` concentra a maioria das ferramentas clássicas de rede, web e exploração em Linux, a `Commando-VM` fornece um ambiente nativo Windows pré-equipado, facilitando testes que dependem de ferramentas Windows, `PowerShell`, binários `.NET` e interação nativa com ambientes Active Directory.

2. **Quais são as credenciais iniciais padrão de uma VM oficial de Kali Linux e que ferramenta do laboratório se usa para engenharia reversa de binários?**
   > [!success]- Ver Resposta
   > As credenciais padrão são `kali` / `kali`. Para engenharia reversa de binários, a ferramenta referida no capítulo é o `Ghidra`.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Capítulo 2 - Preparação do Ambiente Laboratorial]] | Início do capítulo |
| **Seguinte** | [[Anonimização - MAC, Proxy, VPN, kali-anonsurf e Whonix]] | `muda para Bloco 02` |
| **Índice** | [[Capítulo 2 - Preparação do Ambiente Laboratorial]] · [[00 COD1]] | `Bloco 01` |

### Conceitos Relacionados

* [[Testes de Penetração - Metodologia, Pentest Request e Relatórios]] · `Cap. 1`
* [[Cheat Sheet - Playbook de Pentesting e Footprinting Organizacional]]
