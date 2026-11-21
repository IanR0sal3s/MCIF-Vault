---
title: Salvaguarda e Monitorização do Registry
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 6
tipo: procedimento
tags:
  - assi
  - windows
  - registry
  - backup
  - schtasks
  - procmon
  - sysmon
  - forense
aliases:
  - RegBack
  - schtasks
  - Sysmon
  - Procmon
  - Monitorização do Registry
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
fontes:
  - "https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon"
  - "https://github.com/SwiftOnSecurity/sysmon-config/blob/master/sysmonconfig-export.xml"
atualizado: 2026-11-21
---

# Salvaguarda e Monitorização do Registry

A auditoria contínua e histórica do Registry envolve a salvaguarda automática (`RegBack`), a consulta de tarefas agendadas (`schtasks`) e a monitorização de acessos em tempo real (`Procmon` e `Sysmon`).

## 1. Salvaguarda Automática (`RegBack` e `RegIdleBackup`)

* **Funcionamento histórico (Windows 7 / W10 até v1709)**: a tarefa agendada **`RegIdleBackup`** efetuava cópia automática dos hives de sistema de 10 em 10 dias para `C:\Windows\System32\config\RegBack\` (valioso em forense para comparar o estado anterior a um incidente).
* **Alteração crítica**: **desativado por omissão a partir do Windows 10 v1803** (os ficheiros em `RegBack` ficam vazios / `0 KB`).

---

## 2. Agendamento de Tarefas (`schtasks`)

O **`schtasks`** é o equivalente CLI do Agendador de Tarefas gráfico (`taskschd.msc`), permitindo criar (`/create`), eliminar (`/delete`), consultar (`/query`) e alterar (`/change`) tarefas agendadas — frequentemente abusado por *malware* para persistência.

```cmd
schtasks /query /FO csv                            :: Listar tarefas em formato CSV
schtasks /query /FO csv /v                         :: Modo verboso (/v no schtasks = verbose)
schtasks /query /FO csv | findstr /i "ready"       :: Apenas tarefas em estado Ready
schtasks /query /FO csv | findstr /v /i "ready"    :: Excluir Ready (/v no findstr = inverter filtro)
```

---

## 3. Monitorização do Registry: `Procmon` vs. `Sysmon`

| Critério | `Procmon` (Process Monitor) | `Sysmon` (System Monitor) |
| :--- | :--- | :--- |
| **Tipo** | Ferramenta gráfica interativa (análise pontual em tempo real) | Serviço persistente do Windows (auditoria contínua) |
| **Escopo** | Monitoriza interação de processos com Registry, ficheiros e rede | Regista eventos de segurança filtrados por ficheiro XML |
| **Onde grava** | Buffer em RAM / exportação manual | Windows Event Log (`Applications and Services\Microsoft\Windows\Sysmon`) |

```cmd
sysmon.exe -c                                        :: Mostrar configuração atual / omissão
sysmon.exe -accepteula -i sysmonconfig-export.xml    :: Instalar com XML (ex.: SwiftOnSecurity)
sysmon.exe -u                                        :: Desinstalar o serviço Sysmon
```
*(Para detalhe completo do Sysmon e integração com regras SIGMA, ver [[Monitorização Avançada com Sysmon (Sysinternals)]].)*

---

## Além da aula

* **Reativar `RegBack` no W10 v1803+/W11**: criar o valor `REG_DWORD` `EnablePeriodicBackup = 1` em `HKLM\System\CurrentControlSet\Control\Session Manager\Configuration Manager`.
* **Event IDs do Sysmon para o Registry**: `12` (criação/eliminação de chave ou valor), `13` (modificação de valor) e `14` (renomeação de chave ou valor).

---

## Perguntas de revisão

1. **Qual a função do comando `schtasks` e qual a diferença do parâmetro `/v` no `schtasks` face ao `findstr`?**

> [!success]- Ver Resposta
> O `schtasks` permite criar, eliminar, consultar e alterar tarefas agendadas via CLI. No `schtasks`, `/v` ativa o modo *verbose*; no `findstr`, `/v` inverte o filtro (mostra as linhas que **não** contêm o padrão).

2. **Porque é que a pasta `C:\Windows\System32\config\RegBack\` costuma estar vazia ou com ficheiros de 0 KB no Windows 10/11 recente?**

> [!success]- Ver Resposta
> Porque a Microsoft desativou por omissão a tarefa automática `RegIdleBackup` a partir do **Windows 10 versão 1803**.

3. **Qual a diferença prática entre usar `Procmon` e `Sysmon` para monitorizar atividade no Registry?**

> [!success]- Ver Resposta
> O `Procmon` serve para análise interativa pontual em tempo real; o `Sysmon` corre como serviço persistente configurado via XML (ex.: SwiftOnSecurity) e grava continuamente no Windows Event Log.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]] | `Comum/` · `mesmo bloco` |
| **Seguinte** | [[Artefactos Forenses de Execução e Persistência no Registry]] | `muda para Bloco 07` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 06` |

### Conceitos Relacionados

* [[Monitorização Avançada com Sysmon (Sysinternals)]] · `ASSI · Cap. 4`
* [[Artefactos Forenses de Dispositivos USB]] · `Bloco 08`
* [[Estrutura e Hives do Windows Registry]] · `Bloco 05`
* [[Ferramentas de Análise e Extração do Registry]] · `Bloco 05`
* [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]] · `AFD1 · Cap. 1`
