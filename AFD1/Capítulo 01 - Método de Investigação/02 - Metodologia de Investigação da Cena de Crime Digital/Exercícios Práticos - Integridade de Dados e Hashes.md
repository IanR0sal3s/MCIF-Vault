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
atualizado: 2026-11-11
---

# Exercícios Práticos — Integridade de Dados e Hashes

Exercícios práticos de verificação em lote de integridade **`SHA-256`** (`sha256sum` e `HashCalc`) e demonstração da exposição de palavras simples a tabelas pré-computadas no *CrackStation*.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Método / Sistema)**: Validar centenas de ficheiros manualmente é impraticável; manifestos de *hash* (`SHA256.txt`) automatizam a deteção bit-a-bit, enquanto os testes de inversão mostram os limites de *hashes* sem *salt* para entradas curtas ou previsíveis.
> * **Porque importa (Forense / Tribunal)**: A verificação em lote (`sha256sum -c`) garante na cadeia de custódia que nenhum ficheiro adquirido foi corrompido ou alterado entre a recolha e o laboratório.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Flag `-n` em `echo -n "Miguel"`**: sem `-n`, o comando envia `"Miguel\n"` (`7` bytes em vez de `6`), gerando um resumo completamente diferente devido ao efeito de avalanche.
>   * **Hash canónico de `"Miguel"`**: `9293065579a06b12f9b1031e396387c11898b9d50e0e4f7c148073630f79199c`.
>   * **Tabelas pré-computadas (*CrackStation*)**: funções criptográficas não são matematicamente invertíveis, mas palavras comuns sem *salt* são encontradas instantaneamente por consulta de dicionários pré-calculados.

---

## Exercício 1 — Automatizar a Comparação de Valores de Hash

Objetivo: calcular e validar automaticamente a integridade de todos os ficheiros contidos num diretório (ex.: `C:\Windows` ou `/etc`).

### 1. Calcular os valores `SHA-256` e guardar num manifesto
Em sistemas Linux, utilizar o utilitário `sha256sum` redirecionando a saída para um ficheiro de texto:

```bash
sha256sum * > SHA256.txt        # funciona em Linux
```

### 2. Verificar automaticamente os valores de hash contra o manifesto
Para validar se algum ficheiro foi alterado face aos resumos guardados em `SHA256.txt`:

```bash
sha256sum -c SHA256.txt         # funciona em Linux
```

### 3. Alternativa Gráfica em Windows

* Ferramenta gráfica de cálculo de *hashes*: **[HashCalc (SlavaSoft)](https://www.slavasoft.com/hashcalc/)**.

---

## Exercício 2 — Quebrar Valores de Hash por Dicionário

Objetivo: demonstrar que funções de *hash* são unidirecionais, mas entradas curtas ou pertencentes a dicionários comuns podem ser descobertas por pesquisa em bases de dados de *hashes* pré-calculados (*lookup tables* / *rainbow tables*).

### 1. Calcular o `SHA-256` de uma palavra comum (ex.: `Miguel`)
Em Linux, usar `echo -n` para não incluir o carácter de nova linha `\n` no cálculo do *hash*:

```bash
echo -n "Miguel" | sha256sum    # comando Linux
```

* Valor `SHA-256` resultante para `"Miguel"`: `9293065579a06b12f9b1031e396387c11898b9d50e0e4f7c148073630f79199c`

### 2. Testar a reversão por dicionário online

1. Copiar o valor de *hash* obtido e colá-lo no serviço **[CrackStation](https://crackstation.net/)**.
2. **Questão de análise**: O site conseguiu encontrar a palavra original?
   * *Conclusão técnica*: Sim. Para nomes próprios e palavras de dicionário sem *salt*, plataformas como o *CrackStation* mantêm dicionários massivos pré-computados de `MD5`, `SHA-1`, `SHA-256` e `SHA-512`, identificando instantaneamente a palavra de origem.

---

## Anatomia dos Comandos e Comparação de Ferramentas

### Decomposição de Opções (`sha256sum` e `echo -n`)

| Componente / Flag | Significado Técnico e Comportamento | Efeito Prático / Armadilha |
| :--- | :--- | :--- |
| **`sha256sum`** | Utilitário GNU Coreutils que calcula/verifica resumos `SHA-256` (64 dígitos hex) | Lê ficheiros ou `stdin` (neste último caso identifica a origem como `-`) |
| **`*`** | Expansão da *shell* (*globbing*) para todos os ficheiros da diretoria atual | Não desce recursivamente para subdiretorias sem opções adicionais |
| **`> SHA256.txt`** | Redirecionamento de `stdout` para criar/sobrescrever o manifesto | Regista pares `<hash_64_hex>  <nome_ficheiro>` linha a linha |
| **`-c` (`--check`)** | Lê os pares `<hash>` e `<ficheiro>` do manifesto e recalcula cada alvo | Imprime `OK` ou `FAILED` por ficheiro e devolve código de erro se houver falhas |
| **`echo -n`** | Suprime o carácter de nova linha (`\n` / `0x0A`) que `echo` acrescenta por omissão | Garante entrada exata de `6` bytes (`Miguel`) em vez de `7` bytes (`Miguel\n`) |
| **`\|`** (*pipe*) | Encaminha `stdout` do `echo -n` diretamente para `stdin` do `sha256sum` | Evita criar ficheiros temporários em disco durante o cálculo de strings |

### Ferramentas dos Exercícios

| Ferramenta | Plataforma e Tipo | Papel nos Exercícios |
| :--- | :--- | :--- |
| **`sha256sum`** | Linux (CLI) | Geração de manifestos em lote (`* > SHA256.txt`) e validação automática (`-c`) |
| **`HashCalc`** | Windows (GUI) | Cálculo gráfico de múltiplos algoritmos de *hash* para ficheiros e strings |
| **`CrackStation`** | Web (*Lookup Tables*) | Pesquisa de *hashes* (`MD5`, `SHA-1`, `SHA-256`, `SHA-512`) contra dicionários pré-computados |

---

## Implicações Forenses

* **Importância do `-n` no `echo`**: Sem a opção `-n`, o comando `echo "Miguel"` envia `"Miguel\n"` (`7` bytes em vez de `6`), produzindo um *hash* completamente diferente devido ao efeito de avalanche das funções criptográficas.
* **Verificação em Lote na Cadeia de Custódia**: O uso de `sha256sum -c` permite verificar rapidamente centenas de ficheiros extraídos ou imagens forenses aquando da receção no laboratório, sinalizando imediatamente qualquer ficheiro corrompido ou modificado (`FAILED`).

---

## Perguntas de revisão

1. **Qual é a diferença entre `sha256sum * > SHA256.txt` e `sha256sum -c SHA256.txt`?**

> [!success]- Ver Resposta
> O primeiro comando calcula o `SHA-256` de todos os ficheiros da diretoria atual e grava a lista de resumos no manifesto `SHA256.txt`. O segundo usa a flag `-c` para ler `SHA256.txt`, recalcular o `SHA-256` de cada ficheiro listado e reportar se todos continuam íntegros (`OK`) ou se algum foi alterado ou desapareceu (`FAILED`).

2. **Porque é obrigatório utilizar a opção `-n` no comando `echo -n "Miguel" | sha256sum` quando se pretende calcular o *hash* exato de uma string?**

> [!success]- Ver Resposta
> Porque, sem `-n`, o `echo` acrescenta automaticamente um carácter de nova linha (`\n`), passando `7` bytes (`"Miguel\n"`) em vez de `6` (`"Miguel"`), o que produz um *hash* totalmente diferente devido ao efeito de avalanche.

3. **Como é que o *CrackStation* consegue descobrir a palavra que deu origem a um *hash* `SHA-256` se as funções de *hash* criptográficas não são matematicamente invertíveis?**

> [!success]- Ver Resposta
> Não inverte matematicamente a função; consulta bases de dados massivas com tabelas pré-computadas (*lookup tables* / *rainbow tables*) de palavras comuns, nomes próprios e dicionários sem *salt*, encontrando correspondência imediata quando o resumo coincide.

4. **Que ferramenta gráfica equivalente pode ser usada em Windows para calcular valores de *hash* nos exercícios do Capítulo 1?**

> [!success]- Ver Resposta
> A ferramenta gráfica recomendada nos diapositivos para Windows é o **HashCalc** (da SlavaSoft).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Pesquisa de Evidências e Reconstrução de Eventos]] | `mesmo bloco` |
| **Seguinte** | [[Princípios e Rota do Manuseamento de Evidência Digital]] | `muda para Bloco 03` |
| **Índice** | [[Capítulo 1 - Método de Investigação]] · [[00 AFD1]] | `Bloco 02` |

### Conceitos Relacionados

* [[Preservação do Sistema e Integridade de Dados]] · `mesmo bloco`
* [[Fases da Investigação Forense Digital]] · `mesmo bloco`
* [[Extração da AmCache e Comparação Forense com a ShimCache]] · `ASSI · Cap. 1`
* [[Análise Forense e Criação a Pedido do Prefetch]] · `ASSI · Cap. 1`
* [[PKfail - Cadeia de Ataque e Deteção Forense]] · `ASSI · Cap. 1`
* [[Armazenamento Seguro de Passwords (Salting e Key Stretching) e Casos RockYou e LastPass]] · `ASSI · Cap. 2`
* [[Cracking e Auditoria de Passwords com Hashcat (Hashcat 101 e Máscaras)]] · `ASSI · Cap. 2`
