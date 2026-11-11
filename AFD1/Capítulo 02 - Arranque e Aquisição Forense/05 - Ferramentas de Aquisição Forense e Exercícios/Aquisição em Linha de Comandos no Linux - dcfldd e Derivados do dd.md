---
title: Aquisição em Linha de Comandos no Linux - dcfldd e Derivados do dd
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Análise Forense Digital I
sigla_uc: AFD1
capitulo: 2
bloco: 5
fonte_aula: MCIF – Digital Forensic Analysis 1 - Forensic Boot.pdf
tags:
  - afd1
  - forense
  - aquisicao
  - linux
  - dcfldd
  - dd
  - dc3dd
  - ddrescue
  - hashwindow
  - sha256
aliases:
  - dcfldd
  - dc3dd
  - ddrescue
  - dd_rescue
  - rdd
  - dcfldd usage example
atualizado: 2026-11-11
---

# Aquisição em Linha de Comandos no Linux — `dcfldd` e Derivados do `dd`

O `dcfldd` (DCFL) adapta o utilitário Unix `dd` para aquisição forense ao calcular múltiplos *hashes* em tempo real por janelas, agregar erros, preencher *bad sectors* com zeros e dividir imagens `RAW`.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema / Método)**: O utilitário Unix clássico `dd` copia blocos binários sem calcular resumos criptográficos, sem reportar progresso e sem mecanismos periciais nativos para registar e padronizar erros de leitura.
> * **Porque importa (Forense)**: Sem `conv=noerror,sync` + `hashconv=after`, um disco com setores defeituosos produziria um *hash* de aquisição diferente do ficheiro gravado em disco e desalinharia as partições seguintes; além disso, janelas `hashwindow=1G` isolam eventuais corrupções futuras sem invalidar a imagem inteira.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **7 Melhorias face ao `dd`**: (1) *hashes* em tempo real (`md5`, `sha1`, `sha256`, `sha512`); (2) ficheiro separado de *bad sectors*; (3) agregação de erros consecutivos; (4) verificação automática (`vf=`); (5) progresso em tempo real; (6) *splitting* nativo; (7) preenchimento de *bad sectors* com zeros para reprodutibilidade.
>   * **Outros Derivados Forenses do `dd`**: `dc3dd` (DoD Cyber Crime Center), `ddrescue`, `dd_rescue` e `rdd`.
>   * **`hashconv=after`**: Calcula o resumo **após** a substituição de setores ilegíveis por zeros (`sync`), garantindo correspondência exata com o `sha256sum` posterior.
>   * **Janelas Iguais no `SHA256.txt`**: O mesmo valor `30e14955...` repetido em várias janelas consecutivas de `1 MB` indica blocos compostos exclusivamente por zeros (`0x00`).

---

## 1. A Ferramenta `dcfldd` e Diferenças Face ao `dd` Clássico

* **Origem**: Desenvolvida pelo **DCFL (*Department of Defense Computer Forensics Lab*)** dos EUA.
* **Natureza**: Ferramenta forense diretamente derivada do utilitário de linha de comandos `dd`.

### Sete Diferenças Fundamentais do `dcfldd` face ao `dd`

1. **Cálculo integrado de *hashes***: Calcula valores de *hash* durante a própria transferência de dados e suporta os algoritmos **`md5`**, **`sha1`**, **`sha256`** e **`sha512`**.
2. **Registo separado de setores defeituosos**: Consegue escrever os *bad sectors* identificados para um ficheiro separado.
3. **Agregação de erros de leitura**: Consegue agregar mensagens de erros de setores defeituosos consecutivos (ex.: `Had 1,023 'Input/output errors' between blocks 17-233`).
4. **Verificação de integridade**: Verifica automaticamente os valores de *hash* (`vf=` / *verify*).
5. **Relatório de progresso**: Apresenta no ecrã o progresso da aquisição em tempo real (blocos/megabytes copiados e tempo estimado).
6. **Divisão (*splitting*) de ficheiros**: Permite dividir nativamente o ficheiro de imagem em ficheiros mais pequenos (sem depender do comando externo `split`).
7. **Reprodutibilidade pericial nos erros**: Para garantir a reprodutibilidade e o alinhamento, **os setores defeituosos são preenchidos com zeros no ficheiro de imagem**.

### Outros Derivados Forenses do `dd`
Para além do `dcfldd`, existem diversas ferramentas forenses derivadas do `dd`:

* **`dc3dd`** (muito semelhante ao `dcfldd`, mantido pelo *DoD Cyber Crime Center*), **`ddrescue`**, **`dd_rescue`**, **`rdd`**, entre outros.

### Comandos de Ajuda e Documentação no Linux

* `dcfldd --version` $\rightarrow$ verifica a versão instalada.
* `dcfldd --help` $\rightarrow$ lista todas as opções suportadas.
* `man dcfldd` $\rightarrow$ abre o manual completo.
* Fontes complementares recomendadas: página do `dcfldd` em `forensicswiki.org` e artigo do `dd` na Wikipédia.

---

## 2. Dissecação Completa de um Comando de Aquisição com `dcfldd`

Comando completo apresentado na aula para adquirir uma unidade física em formato `RAW` segmentado com duplo *hashing* por janelas e tolerância a erros:

```bash
dcfldd if=/dev/sourcedrive hash=md5,sha256 hashwindow=1G md5log=md5.txt sha256log=sha256.txt hashconv=after bs=512 conv=noerror,sync split=10G splitformat=aa of=image.dd
```

### Tabela Explicativa de Todos os Parâmetros

| Parâmetro | Significado e Função Pericial |
| :--- | :--- |
| **`if=/dev/sourcedrive`** | Ficheiro de dispositivo de entrada que representa a unidade física de origem a adquirir. |
| **`hash=md5,sha256`** | Solicita o cálculo simultâneo dos valores de *hash* **`md5`** e **`sha256`**. |
| **`hashwindow=1G`** | Calcula valores de *hash* parciais a cada **`1 GB`** de dados lidos (*hash blocks* para evitar que um erro único invalide todo o disco). |
| **`md5log=md5.txt`**<br/>**`sha256log=sha256.txt`** | Define o nome dos ficheiros de texto onde serão guardados os valores de *hash* calculados para cada algoritmo. |
| **`hashconv=after`** | Determina que os valores de *hash* são calculados **após o tratamento de erros** — garantindo que o *hash* calculado durante a aquisição inclui os zeros inseridos pelo `sync` e coincide exatamente com o *hash* do ficheiro de imagem final escrito em disco! |
| **`bs=512`** | Utiliza um tamanho de bloco de **`512 bytes`** (igual ao tamanho do setor físico de um HDD). |
| **`conv=noerror,sync`** | • **`noerror`**: Não interrompe a execução em caso de erros de leitura.<br/>• **`sync`**: Mantém a imagem sincronizada/alinhada quando surgem erros, preenchendo o bloco ilegível com zeros (`0x00`). |
| **`split=10G`** | Divide a imagem `RAW` resultante em ficheiros individuais de **`10 GB`**. |
| **`of=image.dd`** | Nome base do ficheiro de saída. |
| **`splitformat=aa`** | Formato dos sufixos dos ficheiros individuais gerados pela divisão: `image.dd.aa`, `image.dd.ab`, `image.dd.ac`, ... |

---

## 3. Estrutura do Ficheiro de Hashes Gerado (`SHA256.txt`)

Quando o `dcfldd` é executado com `hashwindow` (no exemplo abaixo, janelas de `1 MB` = `1048576 bytes` num disco virtual de `53 MB`), o ficheiro `SHA256.txt` regista o intervalo exato de bytes de cada janela, o respetivo resumo `SHA-256` e o *hash* global (`Total`) no final:

```text
cat SHA256.txt
0 - 1048576: 1756ad07245b68744644fa147bbed4dbf5b148ba61839d01e7421ff20098c681
1048576 - 2097152: 908348ee7e44372531d1311143d9ef3a2829fe30f93831b5a81e450a9d366168
2097152 - 3145728: 30e14955ebf1352266dc2ff8067e68104607e750abb9d3b36582b8af909fcb58
3145728 - 4194304: 30e14955ebf1352266dc2ff8067e68104607e750abb9d3b36582b8af909fcb58
4194304 - 5242880: 30e14955ebf1352266dc2ff8067e68104607e750abb9d3b36582b8af909fcb58
5242880 - 6291456: 30e14955ebf1352266dc2ff8067e68104607e750abb9d3b36582b8af909fcb58
...
52428800 - 53477376: 30e14955ebf1352266dc2ff8067e68104607e750abb9d3b36582b8af909fcb58
Total (sha256): 5767d9dcd2e48b3a0dce1b9a143ecf7a664364660637c5f348d1054afb4a1784
```

---

## Implicações Forenses

* **Porquê `hashconv=after` é Crítico Perante Setores Defeituosos?**: Se o disco original tiver *bad sectors*, o parâmetro `conv=noerror,sync` substitui os bytes ilegíveis por zeros (`0x00`) na imagem de saída. Se o *hash* fosse calculado *antes* dessa substituição (`hashconv=before`), o *hash* registado no log nunca coincidiria com o `sha256sum image.dd` calculado mais tarde sobre a imagem adquirida. Usar `hashconv=after` assegura que o *hash* registado reflete exatamente os bytes gravados na imagem forense.
* **Identificação Visual de Blocos de Zeros no Ficheiro de Hashes**: Observe-se no exemplo de `cat SHA256.txt` acima que a partir do byte `2097152` até ao fim do disco (`53477376`), todas as janelas de `1 MB` têm exatamente o mesmo hash `30e14955ebf1352266dc2ff8067e68104607e750abb9d3b36582b8af909fcb58` — que é precisamente o resumo `SHA-256` de `1 MB` preenchido integralmente com bytes zero (`0x00`), permitindo identificar de imediato áreas vazias/não alocadas do disco!

---

## Além da aula

* **Ligação com os Exercícios de Hash do Capítulo 1 de AFD1**:
  * O ficheiro `SHA256.txt` gerado pelo `dcfldd` e a validação posterior dos segmentos `image.dd.aa` articulam-se diretamente com a verificação em lote com `sha256sum` estudada em [[Exercícios Práticos - Integridade de Dados e Hashes]] e com os fundamentos criptográficos de [[Preservação do Sistema e Integridade de Dados]].

---

## Perguntas de revisão

1. **Que melhorias forenses introduz a ferramenta `dcfldd` em relação ao utilitário `dd` padrão do Unix?**

> [!success]- Ver Resposta
> Sete melhorias fundamentais: (1) cálculo de *hashes* em tempo real (`md5`, `sha1`, `sha256`, `sha512`); (2) escrita de *bad sectors* para ficheiro separado; (3) agregação de erros consecutivos de leitura; (4) verificação automática de *hash* (`vf=`); (5) relatório de progresso em tempo real; (6) divisão (*splitting*) nativa em segmentos menores; e (7) preenchimento de *bad sectors* com zeros para garantir reprodutibilidade.

2. **Explique detalhadamente a função dos argumentos `hashwindow=1G`, `hashconv=after` e `conv=noerror,sync` num comando de aquisição com `dcfldd`.**

> [!success]- Ver Resposta
> * **`hashwindow=1G`**: calcula e regista *hashes* parciais a cada `1 GB`, evitando que um único erro futuro invalide a imagem inteira.
> * **`conv=noerror,sync`**: `noerror` impede a paragem do comando perante erros de leitura, e `sync` preenche os blocos ilegíveis com zeros (`0x00`) para manter o alinhamento da imagem.
> * **`hashconv=after`**: garante que o *hash* é calculado **depois** da substituição dos erros por zeros, assegurando que o *hash* de aquisição coincide com o do ficheiro de imagem gravado em disco.

3. **Porque é que num ficheiro `SHA256.txt` gerado com `hashwindow` aparecem frequentemente várias linhas consecutivas com exatamente o mesmo valor de hash?**

> [!success]- Ver Resposta
> Porque essas janelas (ex.: de `1 MB` = `1048576 bytes`) contêm exclusivamente bytes a zero (`0x00`), típicas de áreas vazias ou não alocadas do disco, produzindo sempre exatamente o mesmo resumo criptográfico (no exemplo da aula, `30e14955ebf1352266dc2ff8067e68104607e750abb9d3b36582b8af909fcb58`).

4. **Para que servem os argumentos `bs=512`, `split=10G` e `splitformat=aa` no comando `dcfldd`, e que outros derivados forenses do `dd` existem em Linux?**

> [!success]- Ver Resposta
> `bs=512` alinha o bloco de aquisição com o setor físico padrão de `512 bytes` de um HDD; `split=10G` e `splitformat=aa` dividem a imagem `RAW` em ficheiros de `10 GB` com sufixos alfabéticos (`image.dd.aa`, `image.dd.ab`, ...). Outros derivados forenses do `dd` incluem **`dc3dd`**, **`ddrescue`**, **`dd_rescue`** e **`rdd`**.

## Notas relacionadas

- [[Aquisição e Montagem em Linux - Formato EWF (ewf-tools, ewfmount e xmount)]]
- [[Ferramentas Gráficas de Aquisição Forense (Guymager, Paladin Toolbox, Tableau Imager e FTK Imager)]]
- [[Princípios de Aquisição Forense, Resposta Inicial e Camadas de Abstração]]
- [[Procedimentos de Aquisição - Post-Mortem vs Live, Erros de Disco, HPA-DCO e Write Blockers]]
- [[Armazenamento da Aquisição - Clonagem vs Imagem, Formatos, Aquisição Remota e Assinatura de Hashes]]
- [[Preservação do Sistema e Integridade de Dados]]
- [[Exercícios Práticos - Integridade de Dados e Hashes]]
- [[Capítulo 2 - Arranque e Aquisição Forense]]
