---
title: Artefacto Forense ShellBags
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
tipo: conceito
tags:
  - windows
  - registry
  - shellbags
  - usrclass
  - zimmerman
  - forense
aliases:
  - ShellBags
  - BagMRU
  - Bags
  - SBECmd
  - ShellBags Explorer
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v2.pdf
fontes:
  - "https://www.bleepingcomputer.com/news/microsoft/windows-11-adds-support-for-11-file-archives-including-7-zip-and-rar/"
atualizado: 2026-09-23
---

# Artefacto Forense ShellBags

Os **ShellBags** são artefactos do Windows Registry concebidos para armazenar as preferências de visualização e layout de pastas na interface gráfica (Windows Explorer e caixas de diálogo *Open/Save*). O objetivo do sistema operativo é memorizar o tamanho da janela, modo de exibição de ícones (detalhes, lista, miniaturas) e ordenação para restaurar o aspeto quando o utilizador voltar a aceder à pasta.

Em contrapartida pericial, os ShellBags mantêm um **registo histórico persistente de todas as pastas navegadas pelo utilizador**, mesmo que essas pastas tenham sido apagadas, renomeadas ou residam em dispositivos amovíveis (pens USB) e partilhas de rede entretanto desligadas.

---

## Localização no Registry e Ficheiros de Hive

A localização dos ShellBags depende da versão do sistema operativo:

* **Windows XP**: mantido no ficheiro `NTUSER.DAT` sob `HKCU\Software\Microsoft\Windows\ShellNoRoam\BagMRU`.
* **Windows 7, 8, 10 e 11**: mantido no ficheiro de utilizador **`USRCLASS.DAT`** (`C:\Users\<username>\AppData\Local\Microsoft\Windows\UsrClass.dat`) sob:

```text
HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU
HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags
```

### Estrutura das Chaves:
* **`BagMRU`**: árvore hierárquica indexada por identificadores numéricos que espelha a estrutura de pastas navegada (recorrendo a blocos binários de estruturas `SHITEMID`).
* **`Bags`**: armazena os parâmetros gráficos de renderização de cada pasta referenciada na `BagMRU`.

---

## ShellBags e Ficheiros Compactados (Arquivos)

O Windows Explorer trata certos formatos de arquivo compactado como **pastas virtuais comprimidas**, permitindo ao utilizador "navegar" no seu interior como se fossem diretórios regulares:

1. **Ficheiros ZIP**: suporte nativo desde o Windows Me. A navegação dentro de qualquer `.zip` cria registos ShellBags idênticos aos de uma pasta normal.
2. **Novidade Windows 11 versão 22H2 (Setembro de 2023)**:
   * A Microsoft adicionou suporte nativo no Explorador para a leitura de **11 novos formatos de arquivos comprimidos**:
     * `.tar`, `.tar.gz`, `.tar.bz2`, `.tar.xz`, `.tgz`, `.tbz2`, `.tzst`, `.txz`
     * `.rar` e **`.7z`**
     * Formatos compactados com o algoritmo **ZStandard (ZST)** desenvolvido pela Meta.
   * *Impacto pericial*: a abertura de arquivos `.7z` e `.rar` no Explorador do Windows 11 gera entradas completas no ShellBags, permitindo ao perito comprovar a inspeção de ficheiros comprimidos pelo suspeito.

---

## Ferramentas Forenses de Extração

Devido à complexidade das estruturas de dados SHITEMID em hexadecimal, a análise manual via `regedit` é inviável. Destacam-se as ferramentas periciais da suite de **Eric Zimmerman**:

### 1. `SBECmd.exe` (Linha de Comandos)
Utilitário de linha de comandos de alta velocidade para processar ficheiros `UsrClass.dat` extraídos de imagens forenses:

```cmd
sbecmd.exe -d C:\Caminho\Onde\Esta\UsrClass.dat --csv C:\Caminho\Relatorio_CSV
```

* Gera relatórios tabulados em CSV contendo caminhos absolutos, tipo de pasta (Directory, Zip file contents), número de nós, e marcas temporais de primeiro e último acesso.

### 2. `ShellBags Explorer` (Interface Gráfica)
Interface interativa que reconstrói a árvore de diretórios exata que o utilizador viu na shell, assinalando a cor e ícone pastas locais, unidades de rede, suportes amovíveis e ficheiros compactados.

---

## Conclusão e Limitações Forenses

> [!IMPORTANT] Valor Probatório dos ShellBags
> * **O que provam**: provam conclusivamente que foi solicitado à shell do Windows renderizar a vista de um determinado diretório para aquele utilizador numa determinada data/hora. Prova conhecimento da existência da pasta e atos de navegação.
> * **O que NÃO provam**: os ShellBags associam-se à **navegação no contentor (pasta)**. Não constituem prova pericial de que os ficheiros individuais existentes dentro dessa pasta tenham sido lidos, copiados ou abertos. Para provar a abertura de ficheiros requer-se correlação com outros artefactos ([[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)|RecentDocs]], [[Artefacto Forense UserAssist|UserAssist]] ou ficheiros LNK).

## Notas relacionadas

- [[Estrutura e Hives do Windows Registry]]
- [[Ferramentas de Análise e Extração do Registry]]
- [[Artefactos Forenses de Interação do Utilizador (MRU e TypedPaths)]]
- [[Artefactos Forenses de Dispositivos USB]]
- [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]]
