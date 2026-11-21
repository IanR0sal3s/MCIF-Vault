---
title: Acesso Forense e Montagem de Shadow Copies
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 9
fonte_aula: 02_ArtefactosWindows---2026-27_ULO_v2.pdf
tags:
  - assi
  - windows
  - vss
  - forense
  - mklink
  - vscmount
  - shadowcopyview
  - eric-zimmerman
  - nirsoft
aliases:
  - Montagem de Shadow Copies
  - Acesso a VSS
  - VSCMount
  - ShadowCopyView
  - Ficha 3 VSS
atualizado: 2026-11-21
---

# Acesso Forense e Montagem de Shadow Copies

Como as Shadow Copies residem apenas no *namespace* interno do kernel (`\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopyN`) sem letra de unidade, o perito expõe-nas ao sistema de ficheiros através de três métodos: `mklink /d`, `VSCMount` ou `ShadowCopyView` (**Ficha 3 VSS**).

## 1. Comparação dos 3 Métodos

| Método | Ferramenta | Vantagem Principal | Comando / Ação |
| :--- | :--- | :--- | :--- |
| **1. Nativo (CLI)** | `mklink /d` (`cmd.exe`) | Não requer software externo; monta 1 snapshot. | `mklink /d SHADOW.shortcut \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2\` |
| **2. Em Massa (CLI)** | **`VSCMount`** (Eric Zimmerman) | Monta **todas** as Shadow Copies do volume de uma vez. | `vscmount --dl C --mp c:\DEMO` |
| **3. Gráfico (GUI)** | **`ShadowCopyView`** (NirSoft) | Navegação visual e extração preservando metadados. | Selecionar ficheiros → extrair (`F8`) |

---

## 2. Método Nativo: `mklink /d` (Modo Administrador)

1. Obter o caminho do snapshot com `vssadmin.exe list shadows`;
2. Criar o atalho simbólico de diretório (`/d`):
   ```cmd
   mklink /d SHADOW.shortcut \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2\
   ```
3. Navegar em `SHADOW.shortcut` (ex.: copiar hives bloqueados `SYSTEM`, `SOFTWARE`, `NTUSER.DAT`);
4. Remover a ligação simbólica sem afetar o snapshot: `rmdir SHADOW.shortcut`.

> [!CAUTION] Armadilha de Exame: A Barra Final Obrigatória (`\`)
> No `mklink /d`, é **obrigatório incluir a barra invertida final (`\`)** no caminho `GLOBALROOT`. Sem ela, o Windows não reconhece o destino como raiz de diretório e o atalho fica inacessível.

---

## 3. `VSCMount` (Zimmerman) e `ShadowCopyView` (NirSoft)

* **`VSCMount`**:
  ```cmd
  vscmount --dl C --mp c:\DEMO
  ```
  * `--dl C` (*Drive Letter*): volume alvo; `--mp c:\DEMO` (*Mount Point*): cria automaticamente a pasta **`c:\DEMO_C`** contendo subpastas simbólicas para cada snapshot com data em UTC. Para desmontar, basta apagar a pasta criada.
* **`ShadowCopyView`** (NirSoft): interface gráfica que lista todos os snapshots existentes e permite navegar nas pastas e recuperar ficheiros diretamente (`F8` — *Copy Selected Files To...*).

**Referência bibliográfica da aula**: Ghafarian, A. & Hills, E. D. (2018), *Forensic Analysis of Windows 10 Volume Shadow Copy Service* (IMCIC 2018).

---

## Perguntas de revisão

1. **Porque falha o acesso a uma Shadow Copy montada com `mklink /d SHADOW.shortcut \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy2`?**

> [!success]- Ver Resposta
> Porque falta a **barra invertida final (`\`)** no caminho `GLOBALROOT`. Sem essa barra, o destino não é tratado como raiz de diretório.

2. **Qual a vantagem do `VSCMount` sobre o `mklink /d` e onde fica montado o resultado de `vscmount --dl C --mp c:\DEMO`?**

> [!success]- Ver Resposta
> O `VSCMount` monta automaticamente **todas** as Shadow Copies da unidade indicada (`--dl C`) de uma só vez, criando o ponto de montagem **`c:\DEMO_C`** com subpastas datadas em UTC.

3. **Como remover com segurança uma ligação simbólica criada com `mklink /d` sem destruir a Shadow Copy?**

> [!success]- Ver Resposta
> Usando `rmdir SHADOW.shortcut`, que apaga apenas o apontador simbólico.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Gestão e Manipulação de VSS (CLI, PowerShell e Permissões)]] | `mesmo bloco` |
| **Seguinte** | [[Taxonomia dos Artefactos de Execução no Windows]] | `muda para Bloco 10` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 09` |

### Conceitos Relacionados

* [[Volume Shadow Service (VSS) - Arquitetura e Funcionamento]] · `mesmo bloco`
* [[LastActivityView e Reconstituição Temporal Live]] · `mesmo bloco`
* [[Investigação Forense Digital - Análise Live vs Post-Mortem]] · `AFD1 · Cap. 1`
* [[Princípios e Rota do Manuseamento de Evidência Digital]] · `AFD1 · Cap. 1`
* [[Camadas de Organização de Dados e Análise de Sistemas de Ficheiros]] · `AFD1 · Cap. 3`
