---
title: Artefacto Forense UserAssist
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
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

O **UserAssist** é uma chave do Registry introduzida no Windows NT 4 que armazena telemetria detalhada sobre as aplicações e ficheiros executáveis que um utilizador inicia através da interface gráfica (**GUI**) do Windows Explorer (Menu Iniciar, ambiente de trabalho, atalhos).

Reside no hive pessoal do utilizador (`NTUSER.DAT`):

```text
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist
```

---

## Estrutura das Subchaves e Ofuscação ROT13

Debaixo da chave `UserAssist` existem subchaves identificadas por **GUIDs** (*Globally Unique Identifiers*). Cada GUID corresponde a uma categoria de execução:

| Subchave GUID | Função / Origem da Execução |
| :--- | :--- |
| `{CEBFF5CD-ACE2-4F4F-9178-9926F41749EA}` | Execução direta de ficheiro executável (`.exe`). |
| `{F4E57C4B-45F0-49AB-443B-CFE233D9F}` | Execução a partir de atalho do Windows (`.lnk`). |

Dentro destas subchaves existe uma subchave denominada **`Count`**, onde residem os valores individuais de cada aplicação.

### Codificação ROT13

Para ocultar os nomes à inspeção casual, os nomes dos valores estão cifrados com a **Cifra de César com deslocamento 13 (ROT13)**:
* Cada letra é substituída pela letra 13 posições à frente no alfabeto latino.
* `.exe` torna-se `.RKR`
* `.lnk` torna-se `.YAX`
* *Exemplo*:
  * Cifrado: `{0139Q44R...}\Fxlcr cnen Rzcerfnf.yax`
  * Descodificado: `{0139D44E...}\Skype para Empresas.lnk`

Os GUIDs que surgem no caminho dos atalhos correspondem a **KnownFolderIDs** do Windows. Por exemplo, `{0139D44E-6AFE-49F2-8690-3DAFCAE6FFB8}` traduz-se para `FOLDERID_CommonPrograms` (`%ALLUSERSPROFILE%\Microsoft\Windows\Start Menu\Programs`).

---

## Estrutura Binária do Valor `Count` (72 Bytes)

No Windows 7, Windows 10 e Windows 11, cada valor na subchave `Count` é do tipo `REG_BINARY` com um comprimento fixo de **72 bytes**. A sua estrutura interna decompõe-se nos seguintes campos:

| Offset (Bytes) | Tamanho | Descrição do Campo |
| :---: | :---: | :--- |
| `0–3` | 4 bytes | Identificador de Sessão (*Session ID*). |
| `4–7` | 4 bytes | **Contador de Execuções (*Run Counter*)** — inteiro Little-Endian (começa em 0). |
| `8–11` | 4 bytes | Contador de Foco (*Focus Count*). |
| `12–15` | 4 bytes | **Tempo Total de Foco** — duração em que a janela esteve em primeiro plano (em milissegundos). |
| `16–59` | 44 bytes | Dados reservados / não documentados pela Microsoft. |
| `60–67` | 8 bytes | **Data/Hora da Última Execução** — formato [[Marcadores Temporais no Windows (Timestamps)|Microsoft FILETIME64]] (Little-Endian). |
| `68–71` | 4 bytes | Constante de preenchimento (sempre `0x00000000`). |

### Exemplo Prático de Descodificação de Timestamp

No offset `60` são lidos 8 bytes:
`20 8A 27 EE 37 A5 D4 01` (Little-Endian)
1. Inversão para Big-Endian: `01 D4 A5 37 EE 27 8A 20`
2. Conversão hexadecimal para decimal: `131911948737940000`
3. Conversão de FILETIME: **Sábado, 5 de Janeiro de 2019 às 20:47:54 UTC**.

---

## Configuração e Técnicas Anti-Forense

O UserAssist pode ser manipulado ou inibido através da subchave `Settings`:
* **Desativar registo**: criar valor DWORD `NoLog = 1` sob `...\UserAssist\Settings`.
* **Desativar cifra ROT13**: criar valor DWORD `NoEncrypt = 1` sob `...\UserAssist\Settings`.

---

## Limitações Forenses (*With a Pinch of Salt*)

> [!CAUTION] Falsos Positivos de Execução
> 1. **Renderização de Atalhos**: Investigadores periciais demonstraram que a simples abertura no Explorador de uma pasta que contenha um atalho (`.lnk`) pode provocar um incremento de uma unidade no contador `count` do UserAssist, **mesmo sem que o utilizador tenha clicado ou executado a aplicação**.
> 2. **Exclusividade da GUI**: Programas iniciados pela consola de comandos (`cmd.exe`), scripts de PowerShell, tarefas agendadas ou serviços em segundo plano **não geram entradas no UserAssist**. A ausência de registo no UserAssist não prova que um executável não correu.
> 3. Entradas anormais com contador a zero podem ocorrer esporadicamente para certas aplicações integradas (ex.: Bloco de Notas).

---

## Ferramentas de Análise

* **RegistryExplorer** (Eric Zimmerman): apresenta o separador dedicado *UserAssist*, descodificando automaticamente a cifra ROT13, ordenando por contagem de execuções e traduzindo os timestamps em UTC.
* **UserAssistView** (NirSoft): aplicação gráfica dedicada para triagem rápida em sistemas ativos.
* **RegRipper**: plugin `userassist` (`./rip.exe -r NTUSER.DAT -p userassist`).

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Marcadores Temporais no Windows (Timestamps)]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Artefactos Forenses de Execução e Persistência no Registry]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
