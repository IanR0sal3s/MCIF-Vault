---
title: svchost.exe
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 3
tipo: conceito
tags:
  - assi
  - windows
  - processos
  - servicos
  - svchost
  - registry
aliases:
  - svchost
  - Service Host
  - svchost.exe
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
atualizado: 2026-11-21
---

# O Processo `svchost.exe` (Service Host)

O **`svchost.exe`** (*Service Host*) é o executável anfitrião do Windows (`%SystemRoot%\system32\svchost.exe`) que aloja múltiplos serviços implementados como bibliotecas **DLL**, otimizando o uso de recursos do sistema.

## 1. Funcionamento e Localização no Registry

* **Porque existem vários `svchost.exe`**: o Windows agrupa serviços DLL sob instâncias partilhadas (`WIN32_SHARE_PROCESS`) em vez de criar um `.exe` independente para cada serviço (ao contrário do `Spooler`, que usa `WIN32_OWN_PROCESS` em `spoolsv.exe`).
* **Caminho legítimo**: `%SystemRoot%\system32\svchost.exe`.
* **Lista de grupos no Registry**:
  `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Svchost`

### Comandos de Auditoria
```cmd
:: Mapear cada instância de svchost.exe aos serviços nela alojados
tasklist /SVC

:: Contar o número de instâncias de svchost.exe em execução
tasklist /svc | find /c "svchost.exe"

:: Consultar os grupos Svchost no Registry e contar chaves com sfk
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Svchost" | sfk filter -+HKEY | sfk filter -count
```

---

## Além da aula

* **Camuflagem (*Masquerading*)**: atacantes frequentemente dão o nome `svchost.exe` a binários maliciosos colocados fora de `C:\Windows\System32\` (ex.: `%TEMP%` ou `C:\Windows\`), aproveitando o facto de ser normal ver dezenas de processos com esse nome.

---

## Perguntas de revisão

1. **Qual é a principal função da aplicação `svchost.exe` no Windows?**

> [!success]- Ver Resposta
> Servir de hospedeiro (*service host*) para a execução de múltiplos serviços do Windows implementados como DLLs, otimizando recursos do sistema.

2. **Onde estão registados no Registry os grupos de serviços que correm sob `svchost.exe` e que comando lista os serviços de cada processo ativo?**

> [!success]- Ver Resposta
> Na chave `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Svchost`. Para ver os serviços de cada processo ativo usa-se `tasklist /SVC`.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Serviços Windows]] | `mesmo bloco` |
| **Seguinte** | [[Serviço BITS]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 03` |

### Conceitos Relacionados

* [[Serviço Delivery Optimization]] · `mesmo bloco`
* [[Processos e linha de comandos no Windows]] · `Bloco 02`
