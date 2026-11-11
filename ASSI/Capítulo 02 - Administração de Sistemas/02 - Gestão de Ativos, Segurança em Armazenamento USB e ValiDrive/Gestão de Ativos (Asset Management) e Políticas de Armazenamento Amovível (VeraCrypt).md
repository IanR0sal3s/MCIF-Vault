---
title: Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
bloco: 2
fonte_aula: System Administration - System and Data Management.pdf
tags:
  - assi
  - administracao-sistemas
  - asset-management
  - equifax
  - mac-address
  - removable-storage
  - veracrypt
  - aes
  - twofish
  - serpent
aliases:
  - Asset Management
  - Gestão de Ativos
  - Policy Standard Procedure
  - VeraCrypt Armazenamento Amovível
  - Proibição de USB na IBM
atualizado: 2026-11-11
---

# Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)

O **Asset Management** monitoriza licenças, certificados (caso **Equifax**), garantias, MACs desconhecidos e conformidade, estruturando a segurança USB em **Policy**, **Standard** e **Procedure** com **VeraCrypt**.

> [!TIP] Lógica de Funcionamento e Valor Forense
> * **Porque existe (Sistema)**: Sem inventário dinâmico e alertas automatizados sobre licenças, certificados digitais, garantias e conformidade de *endpoints*, a infraestrutura acumula pontos cegos operacionais. No armazenamento amovível, a tríade **Policy–Standard–Procedure** converte regras abstratas de segurança em configurações concretas e auditáveis de software.
> * **Porque importa (Segurança / Forense)**: Um único certificado expirado de inspeção SSL/TLS cegou os sistemas da **Equifax** durante 76 dias após a intrusão inicial (`CVE-2017-5638`). Da mesma forma, pens USB não cifradas transformam perdas físicas triviais em violações massivas de dados — justificando quer proibições globais (IBM, 2018), quer cifragem em cascata obrigatória (`VeraCrypt`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * **Caso Equifax (2017)**: a entrada ocorreu pelo Apache Struts (`CVE-2017-5638`), mas a exfiltração de ~147 milhões de registos passou despercebida por **76 dias** devido a certificados internos expirados há **10–19 meses**;
>   * **Limitações do endereço MAC**: a deteção de dispositivos desconhecidos apenas por MAC falha perante ***MAC spoofing*** e **MAC aleatório por omissão no Android**;
>   * **Distinção `Policy` vs. `Standard` vs. `Procedure`**: a `Policy` exige cifragem obrigatória; o `Standard` exige `AES` + outro algoritmo forte; o `Procedure` impõe o **VeraCrypt** com **`AES-Twofish`**, **`Serpent-AES`** ou **`AES-Twofish-Serpent`**.

---

## 1. Gestão de Ativos (*Asset Management*): Os Quatro Domínios de Alerta (Slide 27)

Uma administração de sistemas segura exige mecanismos de monitorização e geração de relatórios com **alertas automáticos** em quatro áreas críticas:

### 1.1. Renovações de Licenças e Expiração de Certificados Digitais

* Acompanhar preventivamente renovações de licenciamento de software e datas de expiração de certificados digitais internos e públicos.
* **Caso de Estudo — *Equifax Data Breach* (2017)** ([DigiCert — Equifax Lessons](https://www.digicert.com/blog/lessons-from-the-equifax-data-breach)):
  * A agência de crédito Equifax sofreu a exposição de dados pessoais e financeiros de ~147 milhões de cidadãos;
  * Embora o acesso inicial tenha explorado uma falha no Apache Struts (**`CVE-2017-5638`**), os atacantes exfiltraram dados cifrados durante **76 dias sem deteção** porque um certificado digital interno usado no equipamento de inspeção de tráfego SSL/TLS tinha **expirado há cerca de 10 meses (até 19 meses em alguns sistemas)**, cegando a monitorização de rede.

### 1.2. Expiração de Garantias de Hardware (*Hardware Warranty Expiration*)

* Monitorizar o fim de garantia, *End-of-Life (EOL)* e *End-of-Support (EOS)* de servidores, *switches*, *firewalls* e unidades de armazenamento para planear substituições atempadas antes de falhas ou ausência de *patches*.

### 1.3. Deteção de Dispositivos Desconhecidos por Endereço MAC

* Identificar ligações não autorizadas à rede interna através do alerta para qualquer **endereço MAC nunca antes visto**.
* **Duas Limitações Técnicas Críticas (`NOTE` — Slide 27)**:
  1. **Falsificação fácil (*MAC spoofing*)**: um atacante altera trivialmente o endereço MAC de uma interface para imitar um equipamento legítimo;
  2. **Endereços aleatórios por omissão no Android**: o sistema operativo Android utiliza endereços MAC aleatórios por omissão ao ligar-se a redes Wi-Fi, exigindo controlos de acesso baseados em certificados / `802.1X` em vez de listas estáticas de MAC.

### 1.4. Deteção de Dispositivos em Incumprimento (*Devices Which Do Not Respect Plans*)

* Sinalizar automaticamente máquinas que violem as políticas corporativas instituídas:
  * **Armazenamento de dados não cifrado** (*unencrypted storage*);
  * **Ausência de software antivírus / antimalware** ativo e atualizado.

---

## 2. Armazenamento Amovível: Caso IBM e Governação `VeraCrypt` (Slides 28–30, 34)

### 2.1. O Risco do Armazenamento Amovível e a Proibição na IBM (Slides 29 e 34)
As pens USB, cartões SD e discos externos introduzem um risco operacional duplo:

* **Perda de dados**: extraviar uma única pen USB sem cifragem pode desencadear uma violação massiva de dados;
* **Infeção de sistemas**: contágio por *malware* ou *spyware* através de suportes externos.

**Caso Real — Proibição Global na IBM (Maio de 2018 — Slide 34)**: a IBM proibiu todos os funcionários a nível mundial de utilizar pens USB, cartões SD e *flash drives* amovíveis ([BBC News — IBM USB Ban](http://www.bbc.com/news/technology-44069488)), impondo a transferência exclusiva de ficheiros através de plataformas internas seguras na rede corporativa.

### 2.2. Hierarquia Normativa: *Policy* vs. *Standard* vs. *Procedure* (Slides 29–30)
Quando a organização autoriza armazenamento amovível, tem de articular os três níveis documentais (ilustrados pelo [GCA Toolkit — USB Use Policy](https://gcatoolkit.org/usb-use-policy/) e pelo software [VeraCrypt](https://www.veracrypt.fr/en/Home.html)):

| Nível Normativo | Função na Governação de Segurança | Formulação Concreta para Armazenamento Amovível (Slide 30) |
| :--- | :--- | :--- |
| **1. `Policy`** (Política) | Regra de alto nível que define o requisito obrigatório (*o que é exigido*). | **A cifragem é obrigatória para todo o armazenamento amovível**. |
| **2. `Standard`** (Norma) | Critério técnico uniforme para cumprir a política (*que parâmetros mínimos usar*). | **Os algoritmos mínimos de cifragem devem combinar `AES` com outro algoritmo forte**. |
| **3. `Procedure`** (Procedimento) | Instrução operacional detalhada (*que ferramenta e opções executar na prática*). | • Cifrar o armazenamento amovível com **`VeraCrypt`**.<br>• Utilizar exclusivamente uma das seguintes cascatas:<br>  1. **`AES-Twofish`**;<br>  2. **`Serpent-AES`**;<br>  3. **`AES-Twofish-Serpent`**. |

---

## Além da aula

* **Articulação com a Perícia Forense a Dispositivos USB (`ASSI` Cap. 1 e `AFD1` Cap. 1)**: Quando um dispositivo amovível viola a política organizacional ou é usado na exfiltração de informação, a investigação recorre aos artefactos do Windows Registry (`USBSTOR`, `MountedDevices`, `VolumeSerialNumber` e `setupapi.dev.log`) analisados em [[Artefactos Forenses de Dispositivos USB]] e às regras de catalogação hierárquica (ex.: `PC01.PEN01`) de [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]].
* **Cifragem `VeraCrypt` e *Cryptographic Erasure* (`ASSI` Cap. 2 Bloco 01)**: A adoção obrigatória do `VeraCrypt` em suportes amovíveis suporta também o método de *Cryptographic Erasure* na sanitização de unidades flash e SSDs detalhado em [[Eliminação Segura de Dados em SSDs SATA, NVMe e Memórias Flash]].

---

## Perguntas de revisão

1. **Quais são os quatro domínios de monitorização e alerta em *Asset Management* e qual foi a causa da demora de 76 dias na deteção do ataque à Equifax?**

> [!success]- Ver Resposta
> Os quatro domínios são: (1) renovações de licenças e expiração de certificados digitais, (2) expiração de garantias de hardware, (3) deteção de dispositivos desconhecidos na rede via endereço MAC e (4) deteção de máquinas sem cifragem ou sem antivírus. No caso da **Equifax** (2017, `CVE-2017-5638`), os atacantes exfiltraram dados durante **76 dias sem deteção** porque o certificado interno do sistema de inspeção de tráfego SSL/TLS tinha expirado há cerca de 10 meses (até 19 meses noutros sistemas).

2. **Que duas limitações técnicas reduzem a fiabilidade da deteção de dispositivos desconhecidos baseada apenas em endereços MAC?**

> [!success]- Ver Resposta
> Primeiro, os endereços MAC podem ser facilmente falsificados (*MAC spoofing*). Segundo, o sistema operativo Android utiliza endereços MAC aleatórios por omissão ao ligar-se a redes Wi-Fi, tornando necessário complementar a monitorização com autenticação forte como `802.1X`.

3. **Qual é a diferença entre *Policy*, *Standard* e *Procedure* e qual a aplicação exata destes três níveis à segurança de pens USB com `VeraCrypt`?**

> [!success]- Ver Resposta
> A **Policy** define a obrigação geral (*a cifragem é obrigatória para todo o armazenamento amovível*); o **Standard** especifica o requisito técnico mínimo (*`AES` combinado com outro algoritmo forte*); e o **Procedure** determina a execução prática (*cifrar com `VeraCrypt` utilizando exclusivamente as cascatas `AES-Twofish`, `Serpent-AES` ou `AES-Twofish-Serpent`*).

---

## Notas relacionadas

- [[Capítulo 2 - Administração de Sistemas]]
- [[Vetores de Ataque USB (BadUSB, Rubber Ducky, LNK, USB-Killer) e Defesas (GPO, Pad Jack, ESD Dogs)]]
- [[Pen Drives USB Falsas e Verificação com ValiDrive (Ficha 11)]]
- [[Eliminação Segura de Dados em SSDs SATA, NVMe e Memórias Flash]]
- [[System e OS Hardening e Vulnerabilidade BitLocker YellowKey (CVE-2026-45585)]]
- [[Licenciamento de Software, Fugas em Partilha de Dados (SAS Tokens) e Falhas de Redação]]
- [[Artefactos Forenses de Dispositivos USB]]
- [[Registo, Etiquetagem e Fotografia Pericial (Regras LabCIF)]]
