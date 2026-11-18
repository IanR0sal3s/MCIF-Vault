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
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon"
  - "https://github.com/SwiftOnSecurity/sysmon-config/blob/master/sysmonconfig-export.xml"
atualizado: 2026-09-23
---

# Salvaguarda e Monitorização do Registry

Mecanismos nativos de cópia de segurança periódica (`RegBack` e `RegIdleBackup`), auditoria de tarefas agendadas (`schtasks.exe`) e monitorização de alterações ao Registry em tempo real (`Procmon` vs. `Sysmon`).

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: O sistema operativo precisa de mecanismos de recuperação contra corrupção de hives (`RegBack`), de um motor de automação administrativa (`schtasks.exe`) e de interfaces de instrumentação de *kernel* para diagnóstico e auditoria de segurança (`Procmon` e `Sysmon`).
> * **Porque importa (Forense)**: O Registry e as Tarefas Agendadas são alvos primários de persistência maliciosa. A pasta `RegBack` (quando ativa) permite comparar o estado do Registry antes e depois de uma infeção; o `Procmon` permite observar em laboratório que chaves um *malware* tenta ler/escrever; e o `Sysmon` regista permanentemente no Event Log quem criou, alterou ou renomeou chaves críticas (Event IDs **12, 13 e 14**).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Mudança no Windows 10 v1803 (`RegBack` a 0 KB)**: A partir do Windows 10 versão 1803, a Microsoft desativou por defeito a tarefa `RegIdleBackup`. A pasta `C:\Windows\System32\config\RegBack\` continua a existir, mas está vazia ou contém ficheiros com **0 KB**, a menos que seja reativada via chave `EnablePeriodicBackup = 1`.
>   * **Diferença Arquitetural `Procmon` vs. `Sysmon`**: O `Procmon` é uma ferramenta **interativa/volátil** para análise pontual (não persiste como serviço de auditoria contínua); o `Sysmon` instala-se como **serviço do sistema e driver de kernel**, gravando eventos persistentes no Windows Event Log.

---

## Salvaguarda Automática do Registry (`RegBack`)

Historicamente, o Windows mantinha cópias de segurança automáticas dos hives de sistema em `C:\Windows\System32\config\RegBack\` (`DEFAULT`, `SAM`, `SECURITY`, `SOFTWARE`, `SYSTEM`), geridas pela tarefa agendada `RegIdleBackup`.

### Evolução Comportamental: Antes vs. Depois do Windows 10 v1803

| Característica | Windows 7 / Windows 10 (até v1709) | Windows 10 (v1803+) e Windows 11 |
| :--- | :--- | :--- |
| **Estado por Defeito** | **Ativo** (executado pela tarefa `RegIdleBackup` a cada 10 dias em inatividade) | **Desativado por defeito** pela Microsoft (para reduzir a pegada de disco) |
| **Conteúdo de `\System32\config\RegBack\`** | Cópias completas e funcionais dos 5 hives de sistema (`SYSTEM`, `SOFTWARE`, `SAM`, `SECURITY`, `DEFAULT`) | Pasta vazia ou com ficheiros de hive com tamanho de **0 KB** |
| **Como Reativar?** | Já ativo nativamente | Criar valor `REG_DWORD` **`EnablePeriodicBackup = 1`** em `HKLM\System\CurrentControlSet\Control\Session Manager\Configuration Manager` |
| **Valor Forense** | Fornece uma "fotografia limpa" anterior ao incidente para comparação diferencial de chaves e recuperação de contas | Só tem valor pericial se o administrador tiver forçado previamente a chave `EnablePeriodicBackup = 1` |

### Anatomia do Comando de Auditoria do `RegIdleBackup`

```cmd
schtasks.exe /query /v /FO CSV | findstr /i "regIdleBackup"
```

* **`schtasks.exe /query`**: interroga o Agendador de Tarefas (*Task Scheduler*) listando as tarefas configuradas.
* **`/v`**: (*verbose*) exibe informações detalhadas da tarefa (última execução, código de retorno, autor, comando a executar).
* **`/FO CSV`**: (*Format Output*) formata a saída em texto separado por vírgulas (CSV) para facilitar o processamento linha a linha.
* **`| findstr /i "regIdleBackup"`**: filtra apenas a linha correspondente à tarefa de salvaguarda do Registry (ignorando maiúsculas/minúsculas com `/i`).

---

## Auditoria de Tarefas Agendadas (`schtasks.exe`)

O agendador de tarefas é amplamente abusado por agentes maliciosos para garantir persistência (disparando scripts ou binários no arranque, no logon ou em horários fixos). A triagem em linha de comandos realiza-se com o `schtasks`:

```cmd
REM 1. Listar todas as tarefas do sistema em formato CSV
schtasks /query /FO csv

REM 2. Filtrar apenas tarefas ativas e prontas a executar ("Ready")
schtasks /query /FO csv | findstr /i "ready"

REM 3. Filtrar tarefas desativadas, em execução ou em estado distinto de "Ready"
schtasks /query /FO csv | findstr /v /i "ready"
```

* **Detalhe Crítico da Flag `/v` no `findstr`**: Enquanto no `schtasks` o parâmetro `/v` significa *verbose*, no comando `findstr` o parâmetro **`/v`** inverte o filtro (imprime apenas as linhas que **não** contêm a palavra `"ready"`).

---

## Monitorização da Atividade no Registry: `Procmon` vs. `Sysmon`

| Critério | Process Monitor (`procmon.exe`) | System Monitor (`sysmon.exe`) |
| :--- | :--- | :--- |
| **Natureza e Operação** | Aplicação gráfica interativa para **análise dinâmica pontual** e *troubleshooting* em tempo real | **Serviço do Windows + Driver de Kernel** para **auditoria contínua** e persistente em segundo plano |
| **Onde guarda os dados?** | Em buffer de memória RAM (ou ficheiro `.PML` exportado manualmente pelo analista) | Grava continuamente no **Windows Event Log**: `Applications and Services Logs\Microsoft\Windows\Sysmon\Operational` |
| **Granularidade no Registry** | Captura todas as chamadas de API: `RegOpenKey`, `RegQueryKey`, `RegSetValue`, `RegDeleteKey` (dezenas de milhares de eventos por segundo) | Focado em alterações de segurança filtradas por ficheiro XML (**Event IDs 12, 13 e 14**) |
| **Cenário Ideal** | Engenharia reversa dinâmica de *malware* numa *sandbox* ou resolução de falhas (`NAME NOT FOUND`, `ACCESS DENIED`) | Monitorização permanente de servidores/postos de trabalho e envio de telemetria para um SIEM / EDR |

### Eventos do Registry Monitorizados pelo Sysmon

* **Event ID 12** (*RegistryEvent - Object create and delete*): Criação ou eliminação de chaves ou valores do Registry.
* **Event ID 13** (*RegistryEvent - Value Set*): Modificação do conteúdo de um valor de chave (ex.: adicionar um *payload* à chave `Run`).
* **Event ID 14** (*RegistryEvent - Key and Value Rename*): Mudança de nome de uma chave ou valor (técnica de evasão).

### Anatomia dos Comandos de Gestão do `sysmon.exe`

O Sysmon requer um ficheiro de regras XML (sendo a configuração comunitária de referência a de **SwiftOnSecurity**: `https://github.com/SwiftOnSecurity/sysmon-config`) para filtrar o ruído do sistema e focar em chaves de persistência e ataque:

```cmd
REM 1. Consultar e imprimir a configuração atual em vigor no sistema
sysmon.exe -c

REM 2. Instalar o Sysmon aceitando a licença e aplicando o ficheiro de regras XML
sysmon.exe -accepteula -i sysmonconfig-export.xml

REM 3. Desinstalar completamente o serviço e o driver do Sysmon
sysmon.exe -u
```

* **`-accepteula`**: aceita automaticamente os termos de utilização da Sysinternals sem abrir janela de diálogo (indispensável em scripts de implantação remota).
* **`-i <ficheiro.xml>`**: instala o serviço e o controlador de kernel carregando as regras de filtragem definidas no XML.
* **`-c`**: exibe as regras atualmente aplicadas (ou atualiza a configuração se seguido de um novo ficheiro XML).
* **`-u`**: remove o serviço e descarrega o driver do Sysmon.

---

## Perguntas de revisão

1. **Ao analisar uma imagem forense de um posto de trabalho Windows 11, o perito acede à pasta `C:\Windows\System32\config\RegBack\` para recuperar uma cópia anterior do hive `SOFTWARE`, mas verifica que os ficheiros têm 0 KB. Qual a causa técnica e como poderia o administrador ter prevenido esta situação?**

> [!success]- Ver Resposta
> A partir do Windows 10 versão 1803, a Microsoft desativou por defeito a cópia de segurança automática gerida pela tarefa `RegIdleBackup` para poupar espaço em disco. Para reativar este mecanismo em ambientes empresariais, o administrador deve criar o valor `REG_DWORD` **`EnablePeriodicBackup = 1`** na chave `HKLM\System\CurrentControlSet\Control\Session Manager\Configuration Manager`.

2. **Qual a diferença entre o papel do `Process Monitor (procmon.exe)` e do `System Monitor (sysmon.exe)` na monitorização do Windows Registry?**

> [!success]- Ver Resposta
> O `Procmon` é uma ferramenta interativa de captura em tempo real usada em sessões pontuais de análise dinâmica (registando milhares de leituras e escritas como `RegOpenKey`, `RegQueryKey`, `RegSetValue` e `RegDeleteKey`). Já o `Sysmon` instala-se permanentemente como um serviço e driver de *kernel*, filtrando eventos através de uma configuração XML e gravando registos de auditoria persistentes no Windows Event Log (`Microsoft-Windows-Sysmon/Operational`).

3. **Quais são os três Event IDs gerados pelo `Sysmon` especificamente dedicados a alterações no Windows Registry?**

> [!success]- Ver Resposta
> * **Event ID 12**: Criação ou eliminação de chaves ou valores (*Object create and delete*).
> * **Event ID 13**: Modificação de um valor no Registry (*Value Set*).
> * **Event ID 14**: Renomeação de uma chave ou valor (*Key and Value Rename*).

4. **No comando `schtasks /query /FO csv | findstr /v /i "ready"`, qual é a função exata dos parâmetros `/FO csv` e `/v`?**

> [!success]- Ver Resposta
> O parâmetro `/FO csv` instrui o `schtasks` a formatar a listagem de tarefas como valores separados por vírgulas (CSV). Já o parâmetro `/v` passado ao `findstr` inverte a correspondência textual, exibindo apenas as linhas que **não** contêm a palavra `"ready"` (permitindo identificar tarefas desativadas, em execução ou com falhas).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]] | `Comum/` · `mesmo bloco` |
| **Seguinte** | [[Artefactos Forenses de Execução e Persistência no Registry]] | `muda para Bloco 07` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 06` |

### Conceitos Relacionados

* [[Artefactos Forenses de Dispositivos USB]] · `Bloco 08`
* [[Estrutura e Hives do Windows Registry]] · `Bloco 05`
* [[Ferramentas de Análise e Extração do Registry]] · `Bloco 05`
* [[Diretrizes de Manuseamento - Identificação, Preservação, Isolamento e Correlação]] · `AFD1 · Cap. 1`
