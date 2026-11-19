---
title: Artefacto Forense UserAssist
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 7
tipo: conceito
tags:
  - assi
  - windows
  - registry
  - userassist
  - execucao
  - rot13
  - forense
aliases:
  - UserAssist
  - UserAssist Key
  - Evidência de Execução UserAssist
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://www.aldeid.com/wiki/Windows-userassist-keys"
  - "http://www.nirsoft.net/utils/userassist_view.html"
atualizado: 2026-09-23
---

# Artefacto Forense UserAssist

Chave de telemetria de execução do Windows Explorer no hive `NTUSER.DAT` que regista contadores de execução, tempo de foco e timestamps `FILETIME64` de programas lançados via GUI (ofuscados em **ROT13**).

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Introduzida no Windows NT 4 para que a *shell* do Windows (`explorer.exe`) monitorize quais os programas e atalhos mais utilizados pelo utilizador, permitindo alimentar a lista de programas frequentes no Menu Iniciar.
> * **Porque importa (Forense)**: Reside no ficheiro `NTUSER.DAT` (`HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist`) e fornece, num bloco binário de **72 bytes**, três dados críticos por executável/atalho: **quantas vezes correu** (offset `4–7`), **quanto tempo esteve em primeiro plano** (offset `12–15`) e a **data/hora exata da última execução em UTC** (offset `60–67`, `FILETIME64`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **GUIDs Estáticos vs. PIDs**: Os GUIDs debaixo de `UserAssist` (`{CEBFF5CD...}` para `.exe` e `{F4E57C4B...}` para `.lnk`) **não mudam entre máquinas nem arranques** — são constantes estáticas codificadas no Windows Explorer.
>   * **Dupla Limitação Forense (*Pinch of Salt*)**: (1) Programas executados via linha de comandos (`cmd.exe` / PowerShell) ou serviços **não ficam registados no UserAssist** (é exclusivo da GUI); (2) A simples abertura de uma pasta no Explorer que contenha um atalho `.lnk` pode incrementar o contador `count` em 1 unidade sem que o programa tenha sido executado.

---

## Localização e Subchaves GUID Estáticas

O artefacto reside no hive pessoal do utilizador (`NTUSER.DAT`):

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist
```

Debaixo da chave `UserAssist` existem subchaves identificadas por **GUIDs** (*Globally Unique Identifiers*), dentro das quais existe a subchave **`Count`** que guarda os valores individuais de cada aplicação:

| Subchave GUID (Windows 7, 8, 10 e 11) | Função / Origem da Execução |
| :--- | :--- |
| **`{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}`** | Execução direta de ficheiro executável (**`.exe`**). |
| **`{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}`** | Execução a partir de atalho do Windows (**`.lnk`**). |

> [!NOTE] Constantes do Sistema vs. PIDs Dinâmicos
> Ao contrário de um **PID** (*Process ID*), que é dinâmico e atribuído pelo *kernel* a cada nova execução de um processo, os GUIDs do `UserAssist` são **constantes estáticas pré-definidas pela Microsoft e codificadas no `explorer.exe`**. Qualquer computador com Windows 7 a 11 utilizará exatamente o mesmo GUID para categorizar o lançamento de `.exe` ou `.lnk`.

---

## Ofuscação ROT13 e `KnownFolderIDs`

Para evitar a leitura casual dos nomes dos programas na subchave `Count`, o Windows aplica a **Cifra de César com deslocamento de 13 posições (ROT13)** aos caracteres alfabéticos (números e símbolos mantêm-se inalterados):

| Texto Descodificado (Original) | Texto Ofuscado em ROT13 (no Registry) | Explicação |
| :--- | :--- | :--- |
| `.exe` | **`.RKR`** | Deslocamento de 13 letras no alfabeto latino ($A \leftrightarrow N, E \leftrightarrow R, X \leftrightarrow K$). |
| `.lnk` | **`.YAX`** | Deslocamento de 13 letras ($L \leftrightarrow Y, N \leftrightarrow A, K \leftrightarrow X$). |
| `{0139D44E...}\Skype para Empresas.lnk` | `{0139Q44R...}\Fxlcr cnen Rzcerfnf.yax` | Os dígitos numéricos do GUID não mudam; apenas as letras A–F do GUID e o nome sofrem ROT13. |

* **Tradução de `KnownFolderIDs`**: Os GUIDs que surgem no início do caminho dos programas/atalhos representam diretórios padrão do Windows (*KnownFolderIDs*). Por exemplo, `{0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}` corresponde a `FOLDERID_CommonPrograms` (`%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs`).

---

## Mapa Binário do Valor `Count` (72 Bytes no Windows 7 a 11)

> [!TIP] Simulador Interativo Offline (`UserAssist` ROT13 + 72 Bytes)
> Para testar ao vivo a conversão **ROT13** de qualquer caminho (`C:\Tools\app.exe`) e ver os campos **Little-Endian** preenchidos nos 72 bytes, abre [assi_registry_forense.html](../../../_assets/assi_registry_forense.html).

No Windows 7, 8, 10 e 11, cada entrada dentro da subchave `Count` possui um valor do tipo `REG_BINARY` com um comprimento exato de **72 bytes**. Todos os campos numéricos encontram-se em formato [[Endianness e Ordem de Armazenamento|Little-Endian]]:

| Offset (Bytes) | Offset (Hex) | Tamanho | Campo da Estrutura | Importância Forense |
| :---: | :---: | :---: | :--- | :--- |
| **`0–3`** | `0x00–0x03` | 4 bytes | Identificador de Sessão (*Session ID*) | Sessão em que foi registado. |
| **`4–7`** | `0x04–0x07` | 4 bytes | **Contador de Execuções (*Run Counter*)** | **Crítico**: Inteiro de 32 bits LE (começa em 0) com o número de vezes que a app foi lançada. |
| **`8–11`** | `0x08–0x0B` | 4 bytes | Contador de Foco (*Focus Count*) | Número de vezes que a janela da aplicação recebeu foco. |
| **`12–15`** | `0x0C–0x0F` | 4 bytes | **Tempo Total de Foco (*Focus Time*)** | **Crítico**: Duração acumulada em que a janela esteve ativa em 1.º plano (em **milissegundos**). |
| **`16–59`** | `0x10–0x3B` | 44 bytes | Dados reservados / não documentados | Valores de ponto flutuante internos de ponderação do Menu Iniciar. |
| **`60–67`** | `0x3C–0x43` | 8 bytes | **Data/Hora da Última Execução** | **Crítico**: Carimbo [[Marcadores Temporais no Windows (Timestamps)\|Microsoft FILETIME64]] (64 bits LE, intervalos de 100 ns desde `01/01/1601 UTC`). |
| **`68–71`** | `0x44–0x47` | 4 bytes | Constante de preenchimento (*Padding*) | Sempre preenchido com `0x00000000`. |

### Exemplo Prático de Descodificação do Timestamp (Offset `60–67`)
No offset `60` (`0x3C`) de um valor de 72 bytes do `UserAssist` são lidos os seguintes 8 bytes:

`20 8A 27 EE 37 A5 D4 01`

1. **Inversão de Little-Endian para Big-Endian**: `01 D4 A5 37 EE 27 8A 20`
2. **Conversão de Hexadecimal para Decimal**: `131911948737940000`
3. **Conversão de `FILETIME64` para UTC** (ex.: via `w32tm /ntte 131911948737940000` ou DCODE): **Sábado, 5 de Janeiro de 2019 às 20:47:54 UTC**.

---

## Configuração e Técnicas Anti-Forense (`Settings`)

O comportamento do `UserAssist` pode ser alterado ou desativado através da subchave `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\Settings`:

* **Inibir totalmente o registo (Anti-Forense)**: criar o valor `REG_DWORD` **`NoLog = 1`**.
* **Desativar a ofuscação ROT13 (gravar nomes em texto claro)**: criar o valor `REG_DWORD` **`NoEncrypt = 1`**.

---

## Limitações Forenses (*With a Pinch of Salt*)

> [!CAUTION] Três Armadilhas Periciais do UserAssist em Exame e Tribunal
> 1. **Falso Positivo por Renderização de Atalhos (`.lnk`)**: Investigadores forenses demonstraram que a simples abertura no Windows Explorer de uma pasta que contenha um atalho (`.lnk`) pode provocar um incremento de 1 unidade no contador `Run Counter` (offset `4–7`) do `UserAssist` aquando da resolução do ícone pela *shell*, **mesmo que o utilizador nunca tenha clicado nem executado o programa**.
> 2. **Cegueira à Linha de Comandos (CLI)**: Programas iniciados pela consola (`cmd.exe`), scripts de PowerShell, ficheiros `.bat`, tarefas agendadas ou serviços em segundo plano **não geram entradas no UserAssist**. A ausência de registo no `UserAssist` **não prova** que um executável não correu na máquina.
> 3. **Contadores a Zero**: Podem surgir esporadicamente entradas com contador de execução a zero para certas aplicações integradas do sistema (como o Bloco de Notas).

---

## Ferramentas de Análise

* **RegistryExplorer** (Eric Zimmerman): inclui um plugin visual dedicado que descodifica automaticamente a cifra ROT13, traduz os GUIDs `KnownFolderIDs`, extrai o contador de execuções, o tempo de foco e converte o timestamp `FILETIME64` para UTC.
* **UserAssistView** (NirSoft): utilitário gráfico leve para triagem imediata em sistemas ativos.

**RegRipper** (`rip.exe`) — extração em linha de comandos sobre um hive *offline*:

```bash
./rip.exe -r NTUSER.DAT -p userassist
```

---

## Perguntas de revisão

1. **Porque é que os GUIDs `{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}` e `{F4E57C4B-2036-45F0-A9AB-443BCFE33D9F}` da chave `UserAssist` são iguais em todos os computadores com Windows 10 e 11, e o que representa cada um?**

> [!success]- Ver Resposta
> Ao contrário de identificadores dinâmicos como os PIDs, estes GUIDs são constantes estáticas definidas pela Microsoft no código do `explorer.exe`. O GUID `{CEBFF5CD-...}` agrupa execuções diretas de binários **`.exe`**, enquanto o GUID `{F4E57C4B-...}` agrupa execuções iniciadas através de atalhos **`.lnk`**.

2. **Na estrutura binária de 72 bytes de um valor da subchave `Count` do `UserAssist`, que informações periciais residem nos offsets `4–7`, `12–15` e `60–67`?**

> [!success]- Ver Resposta
> * **Offset `4–7` (4 bytes LE)**: Contador do número de execuções (*Run Counter*).
> * **Offset `12–15` (4 bytes LE)**: Tempo total de foco da janela em primeiro plano, expresso em milissegundos.
> * **Offset `60–67` (8 bytes LE)**: Data e hora da última execução em formato `Microsoft FILETIME64` (intervalos de 100 nanossegundos desde `01/01/1601 UTC`).

3. **Como aparecem as extensões `.exe` e `.lnk` nos nomes dos valores da subchave `Count` do `UserAssist` e que valor do Registry pode desativar esta ofuscação?**

> [!success]- Ver Resposta
> Como os nomes sofrem a cifra **ROT13** (deslocamento de 13 letras no alfabeto), `.exe` transforma-se em **`.RKR`** e `.lnk` transforma-se em **`.YAX`**. Esta ofuscação pode ser desativada criando o valor DWORD **`NoEncrypt = 1`** na subchave `UserAssist\Settings` (e o registo pode ser totalmente inibido com **`NoLog = 1`**).

4. **Um suspeito alega em tribunal que nunca executou um programa malicioso cujo atalho `.lnk` se encontrava numa pen USB, apesar de o `UserAssist` apresentar o contador `Run Counter = 1` para esse atalho. Esta defesa é tecnicamente plausível? E se um binário malicioso não constar de todo no `UserAssist`, isso prova que não foi executado?**

> [!success]- Ver Resposta
> Sim, a defesa para o contador a 1 num `.lnk` é tecnicamente plausível: a simples abertura da pasta da pen USB no Windows Explorer para visualizar os ficheiros pode fazer com que a *shell* processe o atalho `.lnk` e incremente o contador em 1 unidade sem execução real (devendo o perito verificar o tempo de foco no offset `12–15` e cruzar com `Prefetch`/`Amcache`). Quanto à ausência no `UserAssist`, **não prova** que o binário não correu, pois o `UserAssist` apenas regista lançamentos via GUI (`explorer.exe`), ignorando execuções via `cmd.exe`, PowerShell ou tarefas agendadas.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)]] | `mesmo bloco` |
| **Seguinte** | [[Artefacto Forense ShellBags]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 07` |

### Conceitos Relacionados

* [[Estrutura e Hives do Windows Registry]] · `Bloco 05`
* [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]] · `Comum/`
* [[Ferramentas de Análise e Extração do Registry]] · `Bloco 05`
* [[Artefactos Forenses de Execução e Persistência no Registry]] · `mesmo bloco`
* [[Organização de Estruturas de Dados em Binário]] · `AFD1 · Cap. 3`
* [[Endianness e Ordem de Armazenamento]] · `AFD1 · Cap. 3`
* [[Codificação Binário-para-Texto (Base16, Base64 e Base58)]] · `AFD1 · Cap. 3`
* [[Pesquisa de Evidências e Reconstrução de Eventos]] · `AFD1 · Cap. 1`
* [[Código de Ética na Investigação Forense Digital (ISFCE)]] · `AFD1 · Cap. 1`
