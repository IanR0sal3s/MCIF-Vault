---
title: Monitorização Avançada com Sysmon (Sysinternals)
tipo: ferramenta
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 4
bloco: 3
fonte_aula: EI_ASSI_1S2026-27_cap04_v01_LOGs_parte01_v1---ULO.pdf; 17---MCIF_ASSI_1S2026-27_ficha_sysmon+hayabusa_v1---ULO.pdf
tags:
  - assi
  - logs
  - evtx
  - sysmon
  - sysinternals
  - monitorizacao
  - ficha-17
aliases:
  - Sysmon
  - System Monitor
  - SysmonForLinux
  - Ficha 17 ASSI
atualizado: 2026-11-21
---

# Monitorização Avançada com Sysmon (Sysinternals)

O **Sysmon** (*System Monitor*, Sysinternals) é um serviço persistente que expande drasticamente a telemetria nativa do Windows, registando atividade detalhada do sistema no ficheiro:
`%SYSTEMROOT%\system32\winevt\Logs\Microsoft-Windows-Sysmon%4Operational.evtx`

Existe também uma versão open source para Linux (**`SysmonForLinux`**).

## 1. Principais Categorias de Eventos Monitorizados

O Sysmon recolhe evidências que os logs nativos do Windows frequentemente omitem ou registam com pouco detalhe:
* Criação, encerramento e adulteração de processos;
* Ligações de rede iniciadas por processos e **consultas DNS**;
* Alterações nos registos de data/hora de criação de ficheiros (*timestomping*);
* Carregamento de drivers e DLLs;
* Criação, acesso e modificação de ficheiros, diretórios e chaves do **Windows Registry**;
* Modificações na configuração de serviços, eventos **WMI** (filtros e consumidores), atividade do PowerShell e verificações do Windows Defender.

---

## 2. Configuração XML e Comandos (Ficha 17)

O comportamento e filtragem do Sysmon são definidos por um **ficheiro de configuração XML**. Embora exista uma configuração por omissão, na prática utilizam-se perfis comunitários afinados para reduzir ruído — destaque para o **`sysmonconfig-export.xml`** do repositório **`SwiftOnSecurity/sysmon-config`**.

Todos os comandos de gestão exigem **consola CMD com privilégios de administrador**:

| Operação | Comando |
| :--- | :--- |
| **Mostrar configuração atual / omissão** | `sysmon -s` |
| **Instalar como serviço com XML** | `sysmon -accepteula -i sysmonconfig-export.xml` |
| **Atualizar configuração em execução** | `sysmon -c config.xml` |
| **Desinstalar o Sysmon** | `sysmon -u` |

---

## Perguntas de revisão

1. **Onde guarda o Sysmon os eventos recolhidos e porque é frequentemente instalado com o `sysmonconfig-export.xml` (SwiftOnSecurity)?**

> [!success]- Ver Resposta
> Guarda-os em `%SYSTEMROOT%\system32\winevt\Logs\Microsoft-Windows-Sysmon%4Operational.evtx`. O ficheiro XML da SwiftOnSecurity é uma configuração documentada e operacional que filtra ruído legítimo e destaca eventos relevantes para segurança.

2. **Que comandos de administrador permitem instalar, reconfigurar e desinstalar o Sysmon?**

> [!success]- Ver Resposta
> Instalar: `sysmon -accepteula -i <config.xml>`; reconfigurar: `sysmon -c <config.xml>`; desinstalar: `sysmon -u`.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Threat Hunting em EVTX - Regras SIGMA, APT-Hunter, Chainsaw e Hayabusa]] | `mesmo bloco` |
| **Seguinte** | [[Memory Dumps (.dmp) e Windows Error Reporting (WER)]] | `muda para Bloco 04` |
| **Índice** | [[Capítulo 4 - Logs]] · [[00 ASSI]] | `Bloco 03` |

### Conceitos Relacionados

* [[Serviços Windows]] · `ASSI · Cap. 1`
* [[Salvaguarda e Monitorização do Registry]] · `ASSI · Cap. 1`
