---
title: Gestão e Manipulação de VSS (CLI, PowerShell e Permissões)
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
  - vssadmin
  - wmic
  - powershell
  - icacls
  - ransomware
aliases:
  - Gestão de VSS
  - vssadmin
  - Comandos VSS
  - Manipulação de Shadow Copies
atualizado: 2026-11-21
---

# Gestão e Manipulação de VSS (CLI, PowerShell e Permissões)

A administração e auditoria do [[Volume Shadow Service (VSS) - Arquitetura e Funcionamento|VSS]] exige privilégios de **Administrador** e realiza-se via `vssadmin`, PowerShell (`Win32_ShadowCopy`), `wmic` (descontinuado) e `icacls`.

## 1. `wmic` (Descontinuado) e Vetor de Ransomware

```cmd
wmic shadowcopy call create Volume=C:\           :: Criar cópia sombra (legado)
wmic.exe SHADOWCOPY DELETE /nointeractive        :: Apagar todas sem confirmação (usado por ransomware)
```

> [!WARNING] Descontinuação no Windows 11
> O comando `wmic.exe` foi **descontinuado** nas versões recentes do Windows 11. Em sistemas modernos recorre-se ao **PowerShell** ou ao **`vssadmin`**.

---

## 2. PowerShell (Interface WMI)

```powershell
# Criar cópia sombra acessível a clientes/ferramentas forenses (Admin)
$shadow = (Get-WmiObject -List Win32_ShadowCopy).Create("C:\", "ClientAccessible")
$shadow

# Listar volumes shadow existentes
Get-WmiObject Win32_ShadowCopy | Select-Object ID, VolumeName, DeviceObject, InstallDate
```

---

## 3. Armazenamento (`System Volume Information`) e Permissões (`icacls`)

As cópias sombra residem em **`C:\System Volume Information`**, pasta protegida por omissão apenas para a conta **`SYSTEM`** (mesmo um Administrador recebe *Access is denied*).

```cmd
:: Conceder Controlo Total (:F) na pasta e recursivamente (/t)
icacls "C:\System Volume Information" /grant UTILIZADOR:F
icacls "C:\System Volume Information" /grant UTILIZADOR:F /t

:: Restaurar permissões originais após a recolha
icacls "C:\System Volume Information" /remove UTILIZADOR /t
icacls "C:\System Volume Information" /remove UTILIZADOR
```

---

## 4. Utilitário `vssadmin` (Admin)

| Comando | Função |
| :--- | :--- |
| **`vssadmin list shadows`** | Lista snapshots existentes, datas e caminho de dispositivo (`\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopyN`). |
| **`vssadmin delete shadows /shadow={ID}`** | Apaga a cópia sombra identificada pelo GUID. |
| **`vssadmin list writers`** | Lista aplicações que escrevem dados consistentes no snapshot (*Writers*). |
| **`vssadmin list providers`** | Lista fornecedores que criam snapshots (*Providers*). |
| **`vssadmin list shadowstorage`** | Mostra o espaço usado, alocado e máximo em disco (ao atingir o máximo, aplica rotação **FIFO**). |
| **`vssadmin list volumes`** | Lista partições ativas elegíveis para VSS. |

Para montar e navegar nos caminhos `GLOBALROOT` obtidos em `vssadmin list shadows`, ver [[Acesso Forense e Montagem de Shadow Copies]].

---

## Perguntas de revisão

1. **Porque é que grupos de *ransomware* executam `wmic.exe SHADOWCOPY DELETE /nointeractive`, e o que mudou quanto ao `wmic` no Windows 11?**

> [!success]- Ver Resposta
> Para apagar silenciosamente (sem pedir confirmação) todos os pontos de restauro e impedir a recuperação gratuita dos ficheiros cifrados. No Windows 11 recente, o `wmic` foi descontinuado, sendo substituído por PowerShell e `vssadmin`.

2. **Onde são armazenadas as cópias sombra, que conta tem acesso por omissão e que comando altera e restaura essas permissões?**

> [!success]- Ver Resposta
> Em `C:\System Volume Information`, acessível por omissão apenas à conta **`SYSTEM`**. Usa-se `icacls` com `/grant UTILIZADOR:F /t` para conceder acesso e `/remove UTILIZADOR /t` para restaurar as permissões.

3. **Que subcomando do `vssadmin` devolve o caminho `\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopyN` e qual mostra o espaço em disco ocupado?**

> [!success]- Ver Resposta
> `vssadmin list shadows` devolve o caminho `GLOBALROOT` (e GUIDs); `vssadmin list shadowstorage` mostra o espaço usado, alocado e máximo.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Volume Shadow Service (VSS) - Arquitetura e Funcionamento]] | `mesmo bloco` |
| **Seguinte** | [[Acesso Forense e Montagem de Shadow Copies]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 09` |

### Conceitos Relacionados

* [[LastActivityView e Reconstituição Temporal Live]] · `mesmo bloco`
