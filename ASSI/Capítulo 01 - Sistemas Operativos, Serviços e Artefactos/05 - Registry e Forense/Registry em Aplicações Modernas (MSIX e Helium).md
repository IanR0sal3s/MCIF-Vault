---
title: Registry em Aplicações Modernas (MSIX e Helium)
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
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

Com a evolução das aplicações Windows da arquitetura Win32 tradicional para os modelos [[Aplicações UWP (Universal Windows Platform) - Visão Geral|UWP]] e pacotes **MSIX**, o modelo de persistência no Registry sofreu uma mudança profunda. O sistema operativo introduziu o isolamento por contentores e a virtualização do Registry por aplicação.

## O Formato de Pacote MSIX

O **MSIX** é o formato padrão moderno de empacotamento e distribuição de aplicações da Microsoft (adotado na Microsoft Store e instalações empresariais):
* **Isolamento**: cada aplicação corre num contentor leve que restringe o acesso direto aos recursos do sistema operativo.
* **Integridade**: o pacote tem obrigatoriamente de estar assinado digitalmente por um certificado fidedigno.
* **Manifesto (`AppManifest.xml`)**: ficheiro XML que especifica o nome da app, versão, arquitetura, dependências e permissões/capacidades solicitadas (ex.: microfone, rede).
* **Exemplos comuns**: Bloco de Notas (*Windows Notepad* moderno), Windows Terminal, Microsoft Teams, Paint, Dropbox.

## A Pasta `Helium` e o Registry Virtualizado

Para proteger a integridade global do sistema operativo e permitir desinstalações limpas, **uma aplicação empacotada em MSIX não escreve diretamente no Registry do Windows (`NTUSER.DAT` ou `HKLM`)**.

Em vez disso, o Windows redireciona as operações de escrita da aplicação para ficheiros de **Registry privado e virtualizado** mantidos na subpasta designada **`Helium`**:

```text
%LocalAppData%\Packages\<APPID>\SystemAppData\Helium\
```

(Caminho expandido: `C:\Users\<username>\AppData\Local\Packages\<APPID>\SystemAppData\Helium\`).

### Ficheiros de Hive na Pasta `Helium`

Dentro do diretório `Helium` encontram-se ficheiros de hive com a mesma estrutura binária do Registry convencional:
* **`User.dat`**: réplica privada das chaves de `HKCU` da aplicação.
* **`Registry.dat`**: réplica das configurações globais de máquina / pacote.
* **`UsrClasses.dat`**: classes e objetos COM privados do pacote.
* Ficheiros associados de transação: `*.dat.LOG1` e `*.dat.LOG2` (devem ser recolhidos conjuntamente para permitir *replay* de transações não consolidadas).

## Caso de Estudo: Bloco de Notas (Notepad) no Windows 11

No Windows 11, o Bloco de Notas deixou de ser o clássico `notepad.exe` Win32 e passou a ser uma aplicação empacotada:

```text
%LocalAppData%\Packages\Microsoft.WindowsNotepad_8wekyb3d8bbwe\SystemAppData\Helium\User.dat
```

Ao carregar este `User.dat` no **RegistryExplorer**, o perito encontra chaves exclusivas de interação com ficheiros que **não constam do NTUSER.DAT do utilizador**:

```text
Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePIDMru
```

Esta chave regista a lista detalhada e marcas temporais dos ficheiros de texto abertos e gravados recentemente no Bloco de Notas, incluindo caminhos completos e datas.

## Implicações Forenses

1. **Risco de Falsos Negativos em Perícia Tradicional**:
   * Um perito que investigue apenas os hives convencionais (`SYSTEM`, `SOFTWARE` e `NTUSER.DAT`) pode concluir erroneamente que o utilizador não abriu ficheiros sensíveis ou não usou determinadas ferramentas.
   * Aplicações modernas como o Windows Terminal e o novo Bloco de Notas gravam o seu histórico operacional exclusivamente nos ficheiros `User.dat` dentro da pasta `Helium`.
2. **Procedimento de Extração**:
   * O hive `User.dat` da aplicação deve ser extraído e analisado com as mesmas ferramentas dedicadas (como `RegistryExplorer` ou `reg.exe load`), tratando-o como um hive independente.

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Aplicações UWP (Universal Windows Platform) - Visão Geral]]
- [[UWP - Artefactos Forenses e Estrutura de Dados]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
