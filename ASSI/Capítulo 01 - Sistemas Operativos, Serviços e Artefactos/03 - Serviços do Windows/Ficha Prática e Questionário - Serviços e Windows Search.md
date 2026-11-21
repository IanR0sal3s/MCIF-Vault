---
title: Ficha Prática e Questionário - Serviços e Windows Search
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 3
fonte_aula: 01---ficha_laboratorial_v1_Zimmerman_NirSoft_SIDR---ULO_v2.pdf
tags:
  - assi
  - windows
  - wsearch
  - sysinternals
  - zimmerman
  - sidr
  - lab
aliases:
  - Ficha Prática 01
  - Lab 1 Windows Search
  - Laboratório 1 ASSI
atualizado: 2026-11-21
---

# Guia do Laboratório 1 — Ferramentas Forenses & Windows Search

**Porque importa este laboratório**: prepara o teu ambiente Windows com as **três suites base** usadas ao longo de toda a cadeira (**Sysinternals**, **Eric Zimmerman** e **NirSoft**) e ensina-te a extrair — e até compilar a partir do código-fonte — um analisador forense (**`sidr`**) para o [[Windows Search]].

---

## 1. Sysinternals Suite — Instalação Segura e `PATH`

* **Objetivo**: disponibilizar ferramentas de diagnóstico (`sigcheck`, `procexp`, `pslist`, etc.) em qualquer consola CMD.
* **Porquê instalar pela Microsoft Store**: evita falsos positivos do Windows Defender que ocorrem frequentemente ao descarregar o `.zip` manualmente.
* **Como verificar**:
  * Correr `sigcheck` ou `procexp` numa nova consola CMD;
  * Usar `where sigcheck` para descobrir em que pasta do sistema o Windows colocou o executável (na instalação manual via ZIP, é preciso adicionar a pasta à variável de ambiente `PATH`).

---

## 2. Ferramentas Eric Zimmerman — `Get-ZimmermanTools.ps1`

* **Objetivo**: descarregar toda a suite forense de Eric Zimmerman (`PECmd`, `LECmd`, `EvtxECmd`, `bstrings`, `TimelineExplorer`, etc.), que depende do **.NET Runtime (v9)**.
* **Porque precisa de `-ExecutionPolicy Bypass`**: o Windows bloqueia por omissão a execução de scripts `.ps1` por segurança; esta flag contorna a restrição apenas para aquela execução sem baixar permanentemente a segurança do sistema:
  ```cmd
  powershell -noexit -ExecutionPolicy Bypass -File Get-ZimmermanTools.ps1 -d Pasta
  ```
* **Atenção ao `PATH`**: os executáveis ficam dentro da subpasta `PASTA\net9` (ou `net6`), pelo que é esse caminho completo que deve ser adicionado ao `PATH` (testar com `bstrings`).

---

## 3. Extração do Windows Search com `sidr.exe` (Pré-compilado)

* **Objetivo**: transformar as bases do Windows Search (`%AllUsersProfile%\Microsoft\Search\Data\Applications\Windows\`) em ficheiros CSV legíveis para análise forense.
* **Boa prática antes de executar**: validar o executável descarregado junto do VirusTotal com `sigcheck /vt CAMINHO_PARA_sidr.exe`.
* **Execução**:
  ```cmd
  sidr.exe -f csv -o PASTA_RESULTADOS PASTA_WSEARCH
  ```
* **Porque pode ser preciso `net stop wsearch`**: enquanto o serviço `WSearch` está ativo, mantém os ficheiros da base de dados bloqueados; parar o serviço permite ler ou copiar os ficheiros para uma pasta temporária.

---

## 4. Compilar o `sidr` a partir do Código-Fonte (Rust)

* **Porque fazer isto**: em forense digital, compilar uma ferramenta open source a partir do código-fonte evita depender de binários pré-compilados desatualizados ou potencialmente sinalizados por antivírus.
* **Passos essenciais**:
  1. Instalar o ambiente Rust via `rustup` (pode exigir componentes C++ do Visual Studio) e validar com `rustc --version` e `cargo --version`;
  2. Obter o código-fonte (`git clone https://github.com/strozfriedberg/sidr.git` ou ZIP);
  3. Compilar com `cargo b` (modo *debug* → `target\debug\sidr.exe`) ou **`cargo b --release`** (executável otimizado → `target\release\sidr.exe`);
  4. Copiar `sidr.exe` para uma pasta no `PATH` e analisar os CSVs gerados (`File_Report`, atividade e histórico do Edge).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Windows Search]] | `mesmo bloco` |
| **Seguinte** | [[Aplicações UWP (Universal Windows Platform) - Visão Geral]] | `muda para Bloco 04` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 03` |
