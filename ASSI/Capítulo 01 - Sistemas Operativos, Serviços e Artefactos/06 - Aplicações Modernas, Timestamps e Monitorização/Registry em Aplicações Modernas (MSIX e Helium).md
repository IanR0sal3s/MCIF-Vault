---
title: Registry em Aplicações Modernas (MSIX e Helium)
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 6
tipo: conceito
tags:
  - assi
  - windows
  - msix
  - helium
  - registry
  - uwp
  - forense
aliases:
  - MSIX Registry
  - Pasta Helium
  - Virtualized Registry
  - Helium User.dat
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://tinyurl.com/MSIXregistryHelium"
atualizado: 2026-09-23
---

# Registry em Aplicações Modernas (MSIX e Helium)

Modelo de isolamento por contentores e virtualização de hives do Windows Registry na subpasta `Helium` (`User.dat` e `Registry.dat`) em aplicações empacotadas em formato **MSIX**.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: As aplicações Win32 clássicas poluem `NTUSER.DAT` e `HKLM\SOFTWARE` com chaves órfãs que permanecem após a desinstalação (*registry rot*). Com os modelos [[Aplicações UWP (Universal Windows Platform) - Visão Geral|UWP]] e **MSIX**, o Windows executa a aplicação num contentor leve e **redireciona as suas operações de escrita no Registry** para ficheiros de hive privados na pasta `Helium` do pacote, garantindo isolamento e desinstalações limpas.
> * **Porque importa (Forense)**: Aplicações nativas modernas do Windows 11 (como o **novo Bloco de Notas / Notepad**, Windows Terminal, Paint, Microsoft Teams e Dropbox) **já não gravam o seu histórico operacional (`ComDlg32\OpenSavePIDMru`, ficheiros recentes) no `NTUSER.DAT` do utilizador**, mas sim no ficheiro privado `User.dat` dentro de `%LocalAppData%\Packages\<APPID>\SystemAppData\Helium\`.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Risco de Falso Negativo em Perícia Tradicional**: Analisar apenas `NTUSER.DAT` no Windows 11 leva o perito a concluir erroneamente que o utilizador não abriu nem guardou ficheiros no Notepad moderno.
>   * **Recolha de Logs Transacionais**: Na extração da pasta `Helium`, é obrigatório recolher `User.dat`, `Registry.dat`, `UsrClasses.dat` e os respetivos ficheiros `*.dat.LOG1` e `*.dat.LOG2` para consolidar transações pendentes no `RegistryExplorer`.

---

## Comparação: Aplicações Win32 Clássicas vs. Pacotes Modernos MSIX

| Característica | Aplicação Win32 Clássica (ex.: `notepad.exe` no Windows 7 / 10 inicial) | Aplicação Empacotada **MSIX** (ex.: Notepad no Windows 11) |
| :--- | :--- | :--- |
| **Acesso ao Sistema** | Direto aos recursos do SO e ao Registry global do utilizador/máquina | Isolado num contentor leve; permissões declaradas em `AppManifest.xml` |
| **Assinatura Digital** | Opcional (embora recomendada pelo SmartScreen) | **Obrigatória** por certificado fidedigno (garantia de integridade) |
| **Onde grava chaves `HKCU`?** | Diretamente em `C:\Users\<username>\NTUSER.DAT` | Redirecionado para `%LocalAppData%\Packages\<APPID>\SystemAppData\Helium\User.dat` |
| **Onde grava chaves `HKLM`?** | Diretamente em `%SystemRoot%\System32\config\SOFTWARE` | Redirecionado para `...\SystemAppData\Helium\Registry.dat` |
| **Onde reside o histórico `OpenSavePIDMru`?** | No `NTUSER.DAT` principal do utilizador | Exclusivamente no **`User.dat`** dentro da pasta `Helium` do pacote |

---

## O Formato de Pacote MSIX

O **MSIX** é o formato padrão moderno de empacotamento e distribuição de aplicações da Microsoft (adotado na Microsoft Store e em implantações empresariais):

* **Isolamento**: cada aplicação corre num contentor leve que restringe o acesso direto aos recursos globais do sistema operativo.
* **Integridade**: o pacote tem obrigatoriamente de estar assinado digitalmente por um certificado fidedigno (qualquer adulteração de ficheiros invalida a execução).
* **Manifesto (`AppManifest.xml`)**: ficheiro XML estruturado que especifica o nome da aplicação, versão, arquitetura de CPU, dependências e permissões/capacidades solicitadas (ex.: acesso ao microfone, câmara ou rede).
* **Exemplos comuns**: Bloco de Notas (*Windows Notepad* moderno), Windows Terminal, Microsoft Teams, Paint, Dropbox.

---

## A Pasta `Helium` e o Registry Virtualizado

Para proteger a integridade global do sistema operativo e permitir desinstalações limpas sem resíduos, **uma aplicação empacotada em MSIX não escreve diretamente no Registry global do Windows (`NTUSER.DAT` ou `HKLM`)**.

Em vez disso, o subsistema de virtualização do Windows interceta e redireciona as operações de escrita da aplicação para ficheiros de **Registry privado e virtualizado** mantidos na subpasta designada **`Helium`**:

```text
%LocalAppData%\Packages\<APPID>\SystemAppData\Helium\
```

(Caminho absoluto expandido: `C:\Users\<username>\AppData\Local\Packages\<APPID>\SystemAppData\Helium\`).

### Ficheiros de Hive na Pasta `Helium`

Dentro do diretório `Helium` encontram-se ficheiros de hive com exatamente a mesma assinatura (`regf`) e estrutura binária do Registry convencional:

| Ficheiro na Pasta `Helium` | Equivalente no Registry Tradicional | Função e Conteúdo Pericial |
| :--- | :--- | :--- |
| **`User.dat`** | `NTUSER.DAT` (`HKCU`) | Réplica privada das chaves de utilizador da aplicação (inclui `ComDlg32`, MRUs e preferências da app). |
| **`Registry.dat`** | `SOFTWARE` (`HKLM`) | Réplica das configurações globais de máquina / estado do pacote. |
| **`UsrClasses.dat`** | `USRCLASS.DAT` (`HKCU\Software\Classes`) | Classes e objetos COM privados registados pelo pacote. |
| **`*.dat.LOG1` / `*.dat.LOG2`** | `NTUSER.DAT.LOG1` / `.LOG2` | Ficheiros de transação (*transaction logs*). **Devem ser sempre recolhidos conjuntamente** para permitir o *replay* de transações não consolidadas no hive principal. |

---

## Caso de Estudo Forense: Bloco de Notas (Notepad) no Windows 11

No Windows 11, o Bloco de Notas deixou de ser o binário clássico Win32 isolado e passou a ser distribuído como uma aplicação empacotada MSIX. Os seus dados de Registry residem em:

```text
%LocalAppData%\Packages\Microsoft.WindowsNotepad_8wekyb3d8bbwe\SystemAppData\Helium\User.dat
```

Ao carregar este ficheiro `User.dat` no **RegistryExplorer**, o perito encontra chaves exclusivas de interação com ficheiros que **não constam do `NTUSER.DAT` global do utilizador**:

```text
Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePIDMru
```

Esta chave no `User.dat` do pacote regista a lista detalhada e marcas temporais dos ficheiros de texto abertos e gravados recentemente através das caixas de diálogo do Bloco de Notas, incluindo caminhos completos e datas.

---

## Implicações Forenses e Procedimento de Extração

1. **Prevenção de Falsos Negativos em Perícia Tradicional**:
   * Um perito que examine apenas os hives convencionais (`SYSTEM`, `SOFTWARE`, `NTUSER.DAT` e `USRCLASS.DAT`) num sistema Windows 10/11 pode concluir erroneamente que o suspeito não abriu ficheiros sensíveis nem utilizou ferramentas como o Notepad ou o Windows Terminal.
2. **Procedimento de Extração e Montagem**:
   * Durante a triagem de imagens forenses, deve recolher-se todo o diretório `%LocalAppData%\Packages\*\SystemAppData\Helium\`.
   * Os hives `User.dat` e `Registry.dat` de cada aplicação relevante devem ser carregados e analisados com as mesmas ferramentas dedicadas (como `RegistryExplorer`, `RegRipper` ou `reg.exe load`), tratando cada `User.dat` como um hive de utilizador independente.

---

## Perguntas de revisão

1. **Porque é que uma aplicação empacotada em formato MSIX não escreve diretamente nos ficheiros `NTUSER.DAT` ou `SOFTWARE` do Windows e onde são guardadas essas alterações?**

> [!success]- Ver Resposta
> Para garantir o isolamento da aplicação num contentor leve, proteger a estabilidade do sistema operativo e permitir desinstalações totalmente limpas sem deixar lixo no Registry (*registry rot*). As operações de escrita da aplicação são virtualizadas e redirecionadas para hives privados (`User.dat`, `Registry.dat` e `UsrClasses.dat`) armazenados na pasta `%LocalAppData%\Packages\<APPID>\SystemAppData\Helium\`.

2. **Numa perícia a um computador com Windows 11, o analista verifica a chave `ComDlg32\OpenSavePidlMRU` no ficheiro `C:\Users\<user>\NTUSER.DAT` e não encontra qualquer registo de um ficheiro `.txt` aberto e guardado no Bloco de Notas (Notepad). Onde deve procurar esta evidência?**

> [!success]- Ver Resposta
> No Windows 11, o Bloco de Notas é uma aplicação MSIX empacotada. O perito deve extrair e abrir no `RegistryExplorer` o hive virtualizado **`User.dat`** localizado em `%LocalAppData%\Packages\Microsoft.WindowsNotepad_8wekyb3d8bbwe\SystemAppData\Helium\User.dat` (juntamente com os respetivos ficheiros `.LOG1` e `.LOG2`), e inspecionar aí a subchave `Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePIDMru`.

3. **Que ficheiros existem tipicamente dentro da pasta `Helium` de um pacote MSIX e qual a função de cada um?**

> [!success]- Ver Resposta
> Existem três ficheiros de hive principais acompanhados pelos seus logs de transação (`*.LOG1` e `*.LOG2`): (1) `User.dat`, que armazena a réplica privada das chaves `HKCU` da aplicação; (2) `Registry.dat`, que guarda as configurações globais de máquina/pacote equivalentes a `HKLM`; e (3) `UsrClasses.dat`, que regista as classes e objetos COM privados do pacote.

4. **Qual é a função do ficheiro `AppManifest.xml` num pacote MSIX e porque é que um atacante não pode alterar facilmente um binário dentro de um pacote MSIX instalado?**

> [!success]- Ver Resposta
> O `AppManifest.xml` declara a identidade da aplicação (nome, versão, arquitetura), dependências e as capacidades/permissões exigidas (rede, microfone, etc.). Um atacante não pode modificar livremente os ficheiros do pacote porque todo o pacote MSIX tem obrigatoriamente de estar assinado digitalmente por um certificado fidedigno, sendo a integridade criptográfica validada pelo sistema operativo.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Ficha Prática e Questionário - Windows Registry e Artefactos Forenses]] | `Bloco 05` |
| **Seguinte** | [[Timestamps e Épocas Temporais (UNIX Epoch vs. Windows FILETIME)]] | `Comum/` · `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 06` |

### Conceitos Relacionados

* [[Estrutura e Hives do Windows Registry]] · `Bloco 05`
* [[Ferramentas de Análise e Extração do Registry]] · `Bloco 05`
* [[Aplicações UWP (Universal Windows Platform) - Visão Geral]] · `Bloco 04`
* [[UWP - Artefactos Forenses e Estrutura de Dados]] · `Bloco 04`
