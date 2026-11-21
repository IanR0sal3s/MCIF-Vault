---
title: Memory Dumps (.dmp) e Windows Error Reporting (WER)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 4
bloco: 4
fonte_aula: EI_ASSI_1S2026-27_cap04_v01_LOGs_parte02_v1.pdf; 18---MCIF_ASSI_1S2026-27_ficha_logs_ad-hoc_v2---ULO.pdf
tags:
  - assi
  - logs
  - logs-ad-hoc
  - dump
  - wer
  - storm-0558
  - appcrashview
  - bluescreenview
  - sfk
  - ficha-18
aliases:
  - Logs Ad-Hoc Windows
  - Core Dump e Memory Dump
  - Windows Error Reporting
  - Caso Storm-0558
  - Ficha 18 ASSI
atualizado: 2026-11-21
---

# Memory Dumps (`.dmp`) e Windows Error Reporting (WER)

Para além do sistema formal de Windows Event Logs, o Windows gera numerosos **logs ad-hoc** (muitos em `%SYSTEMROOT%\Logs`) e artefactos de diagnóstico em caso de falha, como *memory dumps* (`.dmp`) e relatórios **WER** (`.wer`).

## 1. Core Dumps / Memory Dumps (`.dmp`)

Quando um processo ou o sistema falha, a imagem da memória do processo pode ser gravada em disco num ficheiro `.dmp` (configurável em `SystemPropertiesAdvanced`):
* **Mini dump**: versão reduzida com informação essencial do estado da falha.
* **Full dump**: cópia completa do espaço de memória do processo (muito maior; pode conter credenciais ou segredos em claro).

**Ferramentas de criação e análise**:
* **`WinDbg`** (Microsoft Store) e **`Dumpchk.exe`**: depuração e inspeção de ficheiros `.dmp`;
* **`Process Explorer`** (Sysinternals): permite criar manualmente um *mini dump* ou *full dump* de um processo em execução (Ficha 18);
* **`BlueScreenView`** (NirSoft): verifica vestígios de *Blue Screen of Death* (BSOD);
* **`sfk` (Swiss File Knife)**: pesquisa rápida de `.dmp` e `.wer` no disco (ex.: `sfk list -dir c:\ -file .dmp > out.txt`; validável antes do uso com `sigcheck -vt`).

---

## 2. Windows Error Reporting (WER)

Sistema distribuído de depuração *post-mortem* (presente desde o Windows XP) implementado pelo serviço **`WerSvc`** (`svchost.exe -k WerSvcGroup`).

* **Formato dos ficheiros `.wer`**: texto codificado em **`UTF-16-LE`** (*Little Endian*) estruturado em pares chave-valor.
* **Localização**: `C:\ProgramData\Microsoft\Windows\WER\ReportArchive` (algumas subpastas exigem cópia prévia para uma pasta temporária como `%TEMP%` para leitura direta).
* **Envio remoto**: com consentimento do utilizador, relatórios (que podem incluir *full memory dumps*) são enviados à Microsoft. Desde o Windows 10 o canal é cifrado, mas a **1.ª mensagem é enviada em canal aberto**.
* **Exceções**: aplicações como **Chrome, Firefox e LibreOffice** implementam os seus próprios sistemas de relatório de falhas e não usam WER.
* **Correlação em EVTX**: cada relatório gera um **Event ID `1001`** no log **`Application`** (ex.: `psloglist -i 1001 -s -x application -r` ou `wevtutil qe Application /q:"*[System[(EventID=1001)]]" /f:xml`). Um evento do tipo `BEX64` indica exceção de *buffer overflow* (`/GS`) ou DEP em 64 bits.
* **Consulta visual e desativação**:
  * **Reliability Monitor** (*Monitor de Fiabilidade*): `wscui.cpl` ou Painel de Controlo;
  * **`AppCrashView`** (NirSoft): lista e exporta registos WER para CSV via CLI (Ficha 18);
  * **Desativar WER**: inibir o serviço `WerSvc` ou criar o valor DWORD `Disabled = 1` em `HKLM\Software\Microsoft\Windows\Windows Error Reporting` (também presente em `HKCU`).

---

## 3. Importância Forense e Caso Real: Storm-0558

* ***Development Tradecraft* (Schneier)**: guias de desenvolvimento de *malware* avançado proíbem explicitamente gerar *crash dumps*, *core dumps*, ecrãs azuis ou artefactos WER, pois expõem silenciosamente o binário e o seu estado de memória aos analistas.
* **Caso Storm-0558 (Chave MSA em Crash Dump)**:
  * Em abril de 2021, um crash num processo de autenticação da Microsoft gerou um *crash dump* que incluiu inadvertidamente uma **chave privada *Master Signing Authority* (MSA)** em RAM;
  * O ator **Storm-0558** comprometeu a conta de um programador da Microsoft, acedeu ao ambiente de depuração onde estava o *crash dump*, extraiu a chave e acedeu a contas de e-mail `outlook.com`.
  * **Lição de segurança**: chaves privadas críticas **nunca devem residir em RAM**, mas sim permanecer isoladas num **Hardware Security Module (HSM)** (como TPM ou Secure Enclave).

---

## Perguntas de revisão

1. **Qual a codificação dos ficheiros `.wer`, que serviço os gere e como se correlacionam com o Windows Event Log?**

> [!success]- Ver Resposta
> São ficheiros de pares chave-valor codificados em **`UTF-16-LE`**, geridos pelo serviço **`WerSvc`** (`svchost.exe -k WerSvcGroup`), e correlacionam-se com o **Event ID `1001`** no log **`Application`**.

2. **Como obteve o grupo Storm-0558 a chave privada MSA da Microsoft e que princípio de segurança foi violado?**

> [!success]- Ver Resposta
> Extraiu-a de um *crash dump* de um processo de autenticação guardado num ambiente de depuração de um programador comprometido. O princípio violado foi a presença da chave privada em RAM em vez de permanecer isolada num HSM/TPM.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Monitorização Avançada com Sysmon (Sysinternals)]] | `muda do Bloco 03` |
| **Seguinte** | [[Logs ETL e Caso de Estudo Delivery Optimization (IP Externo)]] | `mesmo bloco` |
| **Índice** | [[Capítulo 4 - Logs]] · [[00 ASSI]] | `Bloco 04` |

### Conceitos Relacionados

* [[svchost.exe]] · `ASSI · Cap. 1`
* [[Análise Forense de USB e Crashes nos Logs EVTX]] · `ASSI · Cap. 4`
* [[Extração de Strings no Windows - Sysinternals strings e Swiss File Knife (sfk)]] · `ASSI · Cap. 3`
