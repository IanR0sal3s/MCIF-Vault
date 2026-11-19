---
title: Entropia de Passwords e Entropia de Ficheiros (ent e Detect It Easy)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 5
fonte_aula: System Administration - Access Control.pdf
fontes:
  - "https://pastebin.com/d3NvGTU8"
  - "https://horsicq.github.io"
tags:
  - assi
  - administracao-sistemas
  - controlo-acessos
  - entropia
  - ent
  - detect-it-easy
  - python
  - forense
aliases:
  - Entropia de uma Password
  - Entropia de um Ficheiro
  - Comando ent Linux
  - Detect It Easy
atualizado: 2026-11-11
---

# Entropia de Passwords e Entropia de Ficheiros (`ent` e `Detect It Easy`)

A entropia mede a imprevisibilidade de palavras-passe em bits e o grau de aleatoriedade de ficheiros entre `0` e `8 bits/byte`, distinguindo texto simples de dados comprimidos ou cifrados com `ent` e `DIE`.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Ameaça)**: Quantificar a incerteza em bits permite avaliar objetivamente a resistência de uma palavra-passe à força bruta e detetar se um binário ou documento apresenta estrutura redundante ou aleatoriedade típica de compressão/cifragem.
> * **Porque importa (Segurança / Forense)**: Na triagem forense e análise de *malware*, valores próximos de `8.0 bits/byte` denunciam executáveis empacotados (`UPX`), ficheiros cifrados por *ransomware* ou contentores ocultos, orientando a aplicação de regras `YARA` e ferramentas de extração de `strings`.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Uma password com $n$ bits exige **$2^{n-1}$ tentativas em média** e **$2^n$ no máximo**.
>   * Em $E = \log_2(R^L) = L \times \log_2(R)$, a entropia cresce **linearmente com $L$** (comprimento) e apenas com **$\log_2(R)$** (diversidade do alfabeto).
>   * **Exemplos da aula**: `123456` ($R=6, L=6$) $\to \mathbf{15.51\text{ bits}}$; `288fc59a22c99621d8dba83650de964b` ($R=15, L=32$) $\to \mathbf{125\text{ bits}}$.
>   * **Ficheiros**: alta entropia ($\approx 7.9\text{ bits/byte}$, não comprime) vs. baixa entropia ($\approx 4.5\text{ bits/byte}$, comprime significativamente).

---

## 1. Entropia de Passwords: Fórmula, Crescimento e Script Python (Slides 36–39)

> [!TIP] Calculadora Interativa de Entropia (`L × log₂(R)`)
> Para testar ao vivo porque uma *passphrase* longa (*xkcd*) supera passwords curtas com muitos símbolos, abre [assi_passwords_entropia.html](../../../_assets/assi_passwords_entropia.html) (separador **3. Calculadora de Entropia**).

### 1.1. Definição, Tentativas Esperadas e Fórmula (Slides 36–37)
A **entropia** quantifica a imprevisibilidade de uma palavra-passe contra ataques de adivinhação ou força bruta:

* Se uma password possui **$n$ bits** de entropia, um atacante que teste combinações aleatórias necessita de:
  * **Em média**: **$2^{n-1}$ tentativas**;
  * **No máximo**: **$2^n$ tentativas**.

**Fórmula Matemática:**

$$E = \log_2(R^L) \iff E = L \times \log_2(R)$$

onde **$R$** representa o número de símbolos únicos do conjunto de caracteres considerado e **$L$** representa o comprimento total da password.

> [!IMPORTANT] Propriedade Fundamental para Exame (Slide 37)
> * A entropia cresce **linearmente com o comprimento $L$**;
> * A entropia cresce apenas com o **logaritmo de base 2 de $R$ ($\log_2 R$)**;
> * Por isso, **aumentar o comprimento $L$** produz um ganho de entropia muito superior a alargar o alfabeto $R$ numa palavra-passe curta.

### 1.2. Exemplos Resolvidos e Script Python 3 (Slides 38–39)
*(Nos exemplos da aula, $R$ contabiliza os símbolos únicos presentes na string analisada)*:

1. **`123456`**: $R = 6$, $L = 6 \implies E = 6 \times \log_2(6) = \mathbf{15.51\text{ bits}}$ ($\approx 16\text{ bits}$, muito fraca — média de $2^{15} = 32\,768$ tentativas).
2. **`288fc59a22c99621d8dba83650de964b`** (32 caracteres hexadecimais): $R = 15$, $L = 32 \implies E = 32 \times \log_2(15) = \mathbf{125\text{ bits}}$ (forte).

O script Python 3 apresentado na aula ([Pastebin — Script Python de Entropia](https://pastebin.com/d3NvGTU8)) usa `collections.Counter` para devolver a entropia de Shannon por carácter e o valor $L \times \log_2(R)$:

```python
import math
from collections import Counter

def entropy(s):
    p, lns = Counter(s), float(len(s))
    per_char_E = -sum(count/lns * math.log(count/lns, 2) for count in p.values())
    num_p = len(p.items())
    return per_char_E, lns * math.log(num_p, 2)
```

* Para `s = "123456"`: devolve `(2.584962500721156, 15.509775004326936)` (**`15.51 bits`**).
* Para `s = "288fc59a22c99621d8dba83650de964b"`: devolve `(3.6490224995673063, 125.02049913158268)` (**`125.02 bits`**).

---

## 2. Entropia de Ficheiros: Escala `0–8 bits/byte`, `ent` e `Detect It Easy` (Slides 40–41)

Como cada byte contém $8\text{ bits}$, a entropia de um ficheiro varia entre **`0` e `8.0 bits/byte`**:

| Nível de Entropia | Valor Típico | Estrutura, Compressibilidade e Exemplos |
| :--- | :---: | :--- |
| **Alta Entropia** | **$\approx 7.9\text{ bits/byte}$** | Elevada aleatoriedade / ausência de estrutura aparente; **não comprime significativamente**. Exemplos: arquivos comprimidos (`.zip`, `.gz`, `.7z`), dados cifrados (*ransomware*, VeraCrypt, BitLocker) ou executáveis empacotados (*packed malware* como `UPX`). |
| **Baixa Entropia** | **$\approx 4.5\text{ bits/byte}$** | Elevada redundância e estrutura; **comprime significativamente**. Exemplos: texto simples (`.txt`), código-fonte, HTML e ficheiros de log. |

### Anatomia das Ferramentas (`ent` no Linux vs. `Detect It Easy` no Windows)

**1. Linux — `ent`** (instalável via `sudo apt install ent`, Slide 41):

Ao executar `ent ls.txt` sobre um ficheiro de texto de `2750` bytes, observam-se cinco métricas periciais principais:

* **`Entropy = 4.532263 bits per byte.`**: confirma baixa entropia típica de texto ASCII;
* **`Optimum compression would reduce the size of this 2750 byte file by 43 percent.`**: estima uma redução de **`43%`** por compressão devido à redundância;
* **`Chi square distribution`**: mede o desvio face a uma distribuição uniforme aleatória;
* **`Arithmetic mean value of data bytes`**: média aritmética dos valores dos bytes (em dados verdadeiramente aleatórios converge para **`127.5`**);
* **Estimativa de $\pi$ por Monte Carlo e Coeficiente de Correlação Série**: avaliam independência estatística entre bytes consecutivos.

**2. Windows — `Detect It Easy (DIE)`** ([Detect It Easy (GitHub)](https://horsicq.github.io), Slide 41):

* Aplicação gráfica para análise de binários que calcula a entropia global e desenha o perfil de entropia por secção PE/ELF;
* No exemplo da aula, um binário comprimido/empacotado apresenta **`Total: 7.96365`** bits/byte e o diagnóstico automático **`packed (99%)`**.

---

## Além da aula

* **Deteção de Empacotamento (`UPX`) e Análise de Strings (`ASSI` Cap. 3 Blocos 01 e 03)**: Quando o `ent` ou o `Detect It Easy` acusam entropia próxima de `7.9 bits/byte` (`packed (99%)`), a etapa seguinte na triagem forense passa por verificar assinaturas de empacotadores como **`UPX`** com regras [[Execução e Compilação no YARA (yara e yarac), Casos Reais (UPX, WannaCry) e LLMs|YARA]] e confirmar a escassez de texto legível com [[Conceito de Strings e Comando strings em Unix-Linux|strings]] ou [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios|bstrings]].
* **Impacto da Baixa Entropia em Chaves Criptográficas**: A necessidade crítica de elevada entropia verdadeira na geração de chaves é ilustrada no estudo de caso [[Caso de Estudo Coldcard (1800 BTC) - Falha de Entropia e Reconstrução de Seeds]] e na avaliação de força de senhas em [[Segurança de Passwords, Paradigma xkcd e Diretrizes NIST (2003 vs SP 800-63-4)]].

---

## Perguntas de revisão

1. **Qual é a fórmula da entropia de uma password em função de $R$ e $L$, quantas tentativas exige para $n$ bits e qual dos dois parâmetros tem maior impacto?**

> [!success]- Ver Resposta
> A fórmula é **$E = \log_2(R^L) = L \times \log_2(R)$**. Para $n$ bits, um ataque aleatório exige **$2^{n-1}$ tentativas em média** e **$2^n$ no máximo**. O comprimento **$L$** tem impacto muito superior, pois a entropia cresce **linearmente com $L$** e apenas com **$\log_2(R)$** em função da diversidade do alfabeto.

2. **Compare os resultados de entropia para `123456` ($R=6, L=6$) e `288fc59a22c99621d8dba83650de964b` ($R=15, L=32$).**

> [!success]- Ver Resposta
> Para `123456`, $E = 6 \times \log_2(6) = \mathbf{15.51\text{ bits}}$ ($\approx 16$ bits, muito fraca, média de $2^{15} = 32\,768$ tentativas). Para a string hexadecimal de 32 caracteres, $E = 32 \times \log_2(15) = \mathbf{125\text{ bits}}$ (forte).

3. **Como se interpreta a entropia por byte num ficheiro (`~4.5` vs. `~7.9 bits/byte`) e que informação fornecem `ent` e `Detect It Easy (DIE)`?**

> [!success]- Ver Resposta
> A entropia varia entre `0` e `8.0 bits/byte`: **`~4.5 bits/byte`** indica baixa entropia, redundância estrutural e elevada compressibilidade (ex.: texto `.txt`, onde `ent ls.txt` reporta `4.532263 bits/byte` e **`43%`** de compressão ótima, além de Chi-quadrado, média aritmética de `127.5` para aleatoriedade, Monte Carlo $\pi$ e correlação série). **`~7.9 bits/byte`** indica dados aleatórios e incompressíveis (comprimidos, cifrados ou empacotados), onde o **`DIE`** reporta por exemplo `Total: 7.96365` e **`packed (99%)`**.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Limite do bcrypt (Okta Bypass), Credential Stuffing e Caso FortiBleed]] | `mesmo bloco` |
| **Seguinte** | [[Caso de Estudo Coldcard (1800 BTC) - Falha de Entropia e Reconstrução de Seeds]] | `mesmo bloco` |
| **Índice** | [[Capítulo 2 - Administração de Sistemas]] · [[00 ASSI]] | `Bloco 05` |

### Conceitos Relacionados

* [[Segurança de Passwords, Paradigma xkcd e Diretrizes NIST (2003 vs SP 800-63-4)]] · `mesmo bloco`
* [[Execução e Compilação no YARA (yara e yarac), Casos Reais (UPX, WannaCry) e LLMs]] · `Cap. 3`
* [[Conceito de Strings e Comando strings em Unix-Linux]] · `Cap. 3`
* [[Eric Zimmerman bstrings - Parâmetros, Expressões Regulares e Exercícios]] · `Cap. 3`
