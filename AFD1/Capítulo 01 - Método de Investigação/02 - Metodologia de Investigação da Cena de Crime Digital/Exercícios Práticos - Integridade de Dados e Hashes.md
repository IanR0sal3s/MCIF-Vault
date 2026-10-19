---
title: Exercícios Práticos - Integridade de Dados e Hashes
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 1
bloco: 2
fonte_aula: MCIF – Digital Forensic Analysis 1 - Investigation Method.pdf
tags:
  - afd1
  - forense
  - exercicio
  - sha256sum
  - hashcalc
  - crackstation
aliases:
  - Exercícios Data Integrity
  - sha256sum
  - CrackStation
atualizado: 2026-10-19
---

# Exercícios Práticos — Integridade de Dados e Hashes

Exercícios práticos do Capítulo 1 focados na **automação do cálculo e verificação de integridade com `SHA-256`** em ambientes Linux (`sha256sum`) e Windows (`HashCalc`), bem como na demonstração prática da vulnerabilidade de resumos criptográficos gerados a partir de palavras simples ou previsíveis através de tabelas pré-computadas (*CrackStation*).

---

## Exercício 1 — Automatizar a Comparação de Valores de Hash

Objetivo: calcular e validar automaticamente a integridade de todos os ficheiros contidos num diretório (ex.: `C:\Windows` ou `/etc`).

### 1. Calcular os valores SHA-256 de todos os ficheiros e guardar num manifesto
Em sistemas Linux, utilizar o utilitário `sha256sum` redirecionando a saída para um ficheiro de texto:

```bash
sha256sum * > SHA256.txt        # funciona em Linux
```

### 2. Verificar automaticamente os valores de hash contra o manifesto
Para validar se algum ficheiro foi alterado face aos resumos guardados em `SHA256.txt`:

```bash
sha256sum -c SHA256.txt         # funciona em Linux
```

### Dica para Sistema Operativo Windows
* Ferramenta gráfica de cálculo de *hashes*: **HashCalc** (`https://www.slavasoft.com/hashcalc/`).

---

## Exercício 2 — Quebrar Valores de Hash (*Crack Hash Values*)

Objetivo: demonstrar que funções de *hash* são unidirecionais, mas entradas curtas ou pertencentes a dicionários comuns podem ser descobertas por pesquisa em bases de dados de *hashes* pré-calculados (*lookup tables* / *rainbow tables*).

### 1. Calcular o SHA-256 de uma palavra comum (ex.: `Miguel`)
Em Linux, usar `echo -n` (a flag `-n` é essencial para **não incluir o carácter de nova linha `\n`** no cálculo do *hash*):

```bash
echo -n "Miguel" | sha256sum    # comando Linux
```

* Valor SHA-256 resultante para `"Miguel"`:
  `9293065579a06b12f9b1031e396387c11898b9d50e0e4f7c148073630f79199c`

### 2. Testar a reversão por dicionário online
1. Copiar o valor de *hash* obtido e colá-lo em `https://crackstation.net/`.
2. **Questão de análise**: O site conseguiu encontrar a palavra original?
   * *Conclusão técnica*: Sim, para nomes próprios e palavras de dicionário sem *salt*, plataformas como o *CrackStation* mantêm dicionários massivos pré-computados de `MD5`, `SHA-1`, `SHA-256` e `SHA-512`, identificando instantaneamente a palavra de origem.

---

## Implicações Forenses

* **Importância do `-n` no `echo`**: Sem a opção `-n`, o comando `echo "Miguel"` envia `"Miguel\n"` (`7` bytes em vez de `6`), produzindo um *hash* completamente diferente devido ao efeito de avalanche das funções criptográficas.
* **Verificação em Lote na Cadeia de Custódia**: O uso de `sha256sum -c` permite verificar rapidamente centenas de ficheiros extraídos ou imagens forenses aquando da receção no laboratório, sinalizando imediatamente qualquer ficheiro corrompido ou modificado (`FAILED`).

---

## Perguntas de revisão

- Qual é a diferença entre `sha256sum * > SHA256.txt` e `sha256sum -c SHA256.txt`?
- Porque é obrigatório utilizar a opção `-n` no comando `echo -n "Miguel" | sha256sum` quando se pretende calcular o *hash* exato de uma string?
- Como é que o *CrackStation* consegue descobrir a palavra que deu origem a um *hash* `SHA-256` se as funções de *hash* criptográficas não são matematicamente invertíveis?

## Notas relacionadas

- [[Preservação do Sistema e Integridade de Dados]]
- [[Fases da Investigação Forense Digital]]
- [[Capítulo 1 - Método de Investigação]]
