---
title: Windows Event Log - Arquitetura, Retenção e Event IDs Críticos
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 4
bloco: 1
fonte_aula: EI_ASSI_1S2026-27_cap04_v01_LOGs_parte01_v1---ULO.pdf
tags:
  - assi
  - logs
  - evtx
  - event-log
  - event-id
  - retencao
  - forense
aliases:
  - Windows Event Log
  - EVTX vs EVT
  - Retenção de Logs
  - Event IDs Críticos
atualizado: 2026-11-21
---

# Windows Event Log - Arquitetura, Retenção e Event IDs Críticos

Os logs registam eventos do sistema operativo e de aplicações, servindo tanto para administração (deteção de anomalias e avarias) como para investigação forense (reconstrução de logins, instalação de serviços e acessos privilegiados).

## 1. Retenção Legal e Normativa de Logs

Diferentes setores e regulamentos impõem períodos mínimos de retenção. Apólices de seguros de cibersegurança podem igualmente exigir retenção específica e salvaguarda *off-site* de forma imutável.

| Norma / Enquadramento | Prazo de Retenção |
| :--- | :--- |
| **HIPAA** (saúde) | 6 anos |
| **GLBA** (dados financeiros de consumidores) | 6 anos |
| **ISO 27001** (gestão de segurança da informação) | 3 anos |
| **PCI DSS** (indústria de cartões de pagamento) | 1 ano |
| **Endereços IP em Portugal** | 1 ano |
| **NIS2** (diretiva europeia de cibersegurança) | 6 a 18 meses |

---

## 2. Evolução e Arquitetura do Windows Event Log

O Windows dispõe de um serviço estruturado de registo de eventos com elevada verbosidade e volume (por exemplo, `192` ficheiros `.evtx` no Windows 11 `24H2` e `410` no `25H2`).

| Característica | Windows XP / Server 2003 | Windows Vista e posteriores |
| :--- | :--- | :--- |
| **Nome do serviço** | Event Log | Windows Event Log |
| **Formato de ficheiro** | `.evt` | `.evtx` (com API para aplicações/serviços) |

* **Localização dos ficheiros**: `%SYSTEMROOT%\system32\winevt\Logs` (habitualmente `C:\Windows\System32\winevt\Logs`).
* **Visualização nativa**: Event Viewer (`eventvwr.exe` ou `eventvwr.msc`), aplicação associada por omissão a `.evtx` (`assoc .evtx` -> `evtxfile`, `ftype evtxfile` -> `eventvwr.exe /l:"%1"`). Permite gravar e exportar para `.txt`, `.csv` e `.xml`.
* **Categorias de logs (`.evtx`)**:
  * **Windows Logs**: tradicionais (`Application`, `System` e `Security` — este último **requer privilégios de administrador**) e novos (`Setup` para instalações/atualizações e `Forwarded Events` para logs recebidos de outras máquinas).
  * **Application and Services Logs**: logs dedicados por aplicação ou componente (centenas de canais distintos).

### Estrutura de uma Entrada

Cada evento inclui: `LogName`, `Source`, `Event ID`, `Task Category`, `Level` (*Information*, *Warning*, *Error*, *Critical*, *Verbose*), `Keywords` (ex.: *Audit Success* / *Audit Failure*), `User`, `OpCode`, `Logged` (data/hora), `Computer` e os detalhes completos em **`XML data`**.

### Gestão Circular e Tamanho Máximo

Por omissão, cada ficheiro `.evtx` tem um tamanho máximo reduzido (**`1 MiB` a `20 MiB`**). Ao atingir o limite, opera em **gestão circular**, sobrescrevendo os registos mais antigos.

* Para aumentar a cobertura de logging em ambientes Windows, existe o script comunitário `YamatoSecurityConfigureWinEventLogs.bat` (que eleva limites para `1 GiB` e ativa canais adicionais).

---

## 3. Event IDs Críticos e Regra de Conversão

Cada evento é identificado por um **Event ID** numérico que simplifica a filtragem forense.

| Event ID (Vista+) | Event ID (Win 2000/XP) | Log | Significado |
| :---: | :---: | :--- | :--- |
| **4624** | `528` | `Security.evtx` | *An account was successfully logged on* |
| **4625** | `529` | `Security.evtx` | *An account failed to log on* |
| **4648** | — | `Security.evtx` | *A logon was attempted using explicit credentials* |
| **4720** | `624` | `Security.evtx` | *User account created* |
| **1102** | — | `Security.evtx` | *The audit log was cleared* (técnica habitual de atacantes) |

> [!IMPORTANT] Regra de Conversão Win 2000/XP vs. Vista+
> Para converter um Event ID do `Security.evtx` (Vista ou superior) para o equivalente em Windows 2000/XP, **subtrai-se `4096`** (ex.: `4624 - 4096 = 528`; `4625 - 4096 = 529`; `4720 - 4096 = 624`).

**Referências úteis de Event IDs citadas na aula**: *Windows Event Log Cheat Sheet* (13cubed), *Event Forwarding Guidance* (NSA), *Malware Archaeology Cheat Sheets* e *Ultimate Windows Security Encyclopedia*.

---

## Perguntas de revisão

1. **Porque é que registos antigos desaparecem num ficheiro `.evtx` mesmo sem intervenção de um atacante?**

> [!success]- Ver Resposta
> Porque os ficheiros `.evtx` têm um tamanho máximo reduzido por omissão (`1 MiB` a `20 MiB`) e utilizam gestão circular: quando atingem o limite, as novas entradas sobrescrevem as mais antigas.

2. **Qual a diferença de privilégios ao consultar `Security.evtx` e que Event ID denuncia a limpeza do log de auditoria?**

> [!success]- Ver Resposta
> O acesso ao `Security.evtx` exige privilégios de administrador. A limpeza do log de auditoria fica registada com o **Event ID `1102`** (*The audit log was cleared*).

3. **Como se obtém o Event ID equivalente no Windows XP a partir do Event ID `4624` do Windows 10/11?**

> [!success]- Ver Resposta
> Subtraindo `4096`: `4624 - 4096 = 528` (*Successful logon*).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Capítulo 4 - Logs]] | Início do capítulo |
| **Seguinte** | [[Ferramentas Nativas e CLI para EVTX (WEVTUtil, psloglist e PowerShell)]] | `mesmo bloco` |
| **Índice** | [[Capítulo 4 - Logs]] · [[00 ASSI]] | `Bloco 01` |

### Conceitos Relacionados

* [[Tipos de Dados e Associação de Ficheiros no Registry]] · `ASSI · Cap. 1`
* [[Matriz de Correlação Forense e Cronologia de Ativação dos Artefactos]] · `ASSI · Cap. 1`
