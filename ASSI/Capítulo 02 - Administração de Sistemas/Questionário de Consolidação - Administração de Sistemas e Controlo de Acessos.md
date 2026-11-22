---
title: Questionário de Consolidação - Administração de Sistemas e Controlo de Acessos
tipo: exercicio
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 2
fonte_aula: 01_EI_ASSI_1S2026-27_SysAdmin_data_management_v1---ULO.pdf; 02_EI_ASSI_1S2026-27_SysAdmin_access_control_V1---ULO.pdf
tags:
  - assi
  - exercicio
  - questionario
  - revisao
  - administracao-sistemas
  - controlo-acessos
aliases:
  - Questionário Capítulo 2 ASSI
  - Revisão Administração de Sistemas
atualizado: 2026-11-22
---

# Questionário de Consolidação — Administração de Sistemas e Controlo de Acessos

Autoavaliação estilo exame (Grupo I — escolha múltipla + Grupo II — resposta aberta curta) para validar a compreensão dos **Blocos 01 a 06** do [[Capítulo 2 - Administração de Sistemas]].

---

## Grupo I — Escolha Múltipla

### 1. Sanitização de HDDs vs. SSDs
Uma organização pretende abater discos rígidos magnéticos (`HDD`) e unidades `SSD` NVMe contendo dados confidenciais. Qual afirmação está **correta**?
* **A)** O *degaussing* destrói os dados em SSDs NAND Flash e permite reutilizar os HDDs após formatação rápida.
* **B)** Três passagens DoD 5220.22-M garantem eliminação total em pens USB e SSDs, incluindo blocos de *over-provisioning*.
* **C)** O *degaussing* inutiliza HDDs (destrói as *servo tracks* de fábrica) e não tem efeito em SSDs/Flash; para NVMe deve usar-se `Format NVM` (*Cryptographic Erase*) ou `nvme sanitize`.
* **D)** Passar um HDD pelo `DiskMantler` (60 segundos) destrói definitivamente todos os dados magnéticos dos pratos.

### 2. Hierarquia Normativa (`Policy` vs. `Standard` vs. `Procedure`)
Numa política de armazenamento amovível com `VeraCrypt`, a instrução *"cifrar com VeraCrypt usando AES-Twofish, Serpent-AES ou AES-Twofish-Serpent"* corresponde a que nível?
* **A)** *Policy*
* **B)** *Standard*
* **C)** *Procedure*
* **D)** *Audit Trail*

### 3. Pen Drives USB Falsas (`ValiDrive` — Ficha 11)
Uma pen USB comprada por `$19.99` anuncia `1 TB` ao sistema operativo, mas só possui `64 GB` físicos reais. Como atua o `ValiDrive`?
* **A)** Executa testes aleatórios não destrutivos (*spot-check*) em 576 regiões ao longo da capacidade declarada, distinguindo *Validated Storage* (verde) de *Missing Storage* (vermelho).
* **B)** Formata a pen a baixo nível destruindo todos os dados existentes para medir o espaço físico real.
* **C)** Lê apenas o descritor `reported capacity` do firmware USB e compara-o com o número de série.
* **D)** Executa sobrescrita sequencial completa de toda a *Fake Part* para recuperar os setores reais.

### 4. `BitLocker's YellowKey` (`CVE-2026-45585`)
Que condição e mitigação caracterizam a vulnerabilidade `BitLocker's YellowKey`?
* **A)** Exploração remota via SMB em Windows 10; mitigada desativando o `SecureBoot` na UEFI.
* **B)** Afeta apenas discos Linux `LUKS2` configurados sem password de arranque na BIOS.
* **C)** Permite decifrar volumes `VeraCrypt` através de um *Account-level SAS Token* exposto.
* **D)** Requer acesso físico em Windows 11 ($\ge$ `24H2`) / Server 2025 com BitLocker `TPM-only` sem PIN, abusando do WinRE; mitigada com `KB5089549` e `TPM+PIN`.

### 5. `SMS Blaster` vs. Smishing Tradicional
Qual é a principal particularidade técnica de uma estação portátil `SMS Blaster`?
* **A)** Requer a lista prévia de números telefónicos das vítimas para enviar mensagens através da rede do operador.
* **B)** Imita uma torre celular com sinal dominante e força o *downgrade* para `2G` (sem cifragem nem autenticação), difundindo SMS sem precisar dos números; mitigável desligando `2G` no Android 12+.
* **C)** Funciona exclusivamente em redes `5G` explorando a autenticação mútua entre terminal e estação base.
* **D)** Interceta códigos `Passkey` através de Bluetooth a longa distância em zonas movimentadas.

### 6. Diretrizes `NIST SP 800-63-4` (2024) vs. NIST 2003
O que mudou fundamentalmente nas recomendações de passwords do `NIST SP 800-63-4` face a 2003?
* **A)** Proibiu exigir alterações periódicas obrigatórias (salvo evidência de *data breach* ou *credential stuffing*), privilegiando comprimento ($\ge 8$, idealmente $\ge 15$ até $64$ caracteres) e permitindo ASCII/Unicode.
* **B)** Passou a exigir rotação obrigatória a cada 60 dias e proibiu caracteres Unicode e espaços em branco.
* **C)** Recomendou substituir palavras-passe longas por sequências curtas de 8 caracteres com substituições (`Tr0ub4dor&3`).
* **D)** Tornou o SMS *Out-of-Band* o método preferencial de autenticação multifator para contas críticas.

### 7. Entropia de Passwords e de Ficheiros
Considerando $E = L \times \log_2(R)$ e a escala de entropia por byte (`0–8 bits/byte`), qual afirmação está **correta**?
* **A)** A entropia cresce linearmente com $R$ e logaritmicamente com $L$; um ficheiro cifrado `.kdbx` apresenta entropia $\approx 4.5\text{ bits/byte}$.
* **B)** Uma password de $n$ bits exige em média $2^n$ tentativas num ataque de força bruta exaustivo.
* **C)** O `ent` e o `Detect It Easy` servem exclusivamente para calcular a entropia de passwords curtas em texto limpo.
* **D)** A entropia cresce linearmente com $L$ e com $\log_2(R)$; um ficheiro de texto simples tem entropia baixa ($\approx 4.5\text{ bits/byte}$) e um ficheiro comprimido ou cifrado tem entropia alta ($\approx 7.9\text{ bits/byte}$).

### 8. Limite do `bcrypt` (`Okta Bypass`)
Porque provocou `bcrypt(userId + ":" + username + ":" + password)` um *authentication bypass* na Okta quando `username > 56 bytes`?
* **A)** Porque o `bcrypt` não suporta *per-credential salt* quando recebe entradas concatenadas.
* **B)** Porque o `bcrypt` (baseado em *Blowfish*) processa apenas os primeiros `56–72 bytes` da entrada e trunca silenciosamente o restante, ignorando a `password`.
* **C)** Porque o `bcrypt` fica vulnerável a *Rainbow Tables* pré-computadas quando recebe nomes longos.
* **D)** Porque o `bcrypt` converte automaticamente a password para texto limpo sempre que ultrapassa 56 bytes.

### 9. `TOTP` (`RFC 6238`) vs. `Passkeys` (`FIDO2`)
Qual a principal vantagem de segurança das `Passkeys` (`FIDO2`) face a códigos `TOTP` de 6 dígitos?
* **A)** As `Passkeys` enviam a chave privada cifrada ao servidor de autenticação em cada sessão.
* **B)** O `TOTP` depende obrigatoriamente da rede celular `SS7` para sincronizar o contador temporal.
* **C)** As `Passkeys` vinculam criptograficamente o par de chaves assimétricas ao domínio exato (imunes a phishing/proxies AitM como `OTP.Agency`) e exigem Bluetooth para prova de proximidade em fluxos *cross-device*.
* **D)** As `Passkeys` eliminam qualquer risco mesmo que o smartphone da vítima seja roubado e desbloqueado.

### 10. Armazenamento Seguro e `hashcat`
O que executa o comando `hashcat -m 0 -a 3 -1 ?u?l -o cracked.txt hashes.txt ?1?1?1?1?1?1?1`?
* **A)** Ataque de força bruta por máscara (`-a 3`) sobre hashes `MD5` (`-m 0`), testando palavras-passe de 7 letras misturando maiúsculas e minúsculas (`-1 ?u?l`).
* **B)** Ataque de dicionário (`-a 3`) sobre hashes `NTLM` (`-m 0`), testando palavras da lista `rockyou.txt`.
* **C)** Ataque de máscara sobre hashes `SHA-256` (`-m 0`), testando 7 caracteres ASCII imprimíveis (`?a`).
* **D)** Ataque híbrido sobre bases de dados `KeePassXC` com 7 dígitos numéricos.

---

## Grupo II — Resposta Aberta Curta

### 11. Porque falha o `per-credential salt` sozinho (sem `Key Stretching`) contra um atacante que exfiltra a base de dados?
> [!success]- Ver Tópicos de Resposta
> O `per-credential salt` garante que passwords iguais geram hashes diferentes e invalida *lookup* / *Rainbow Tables* pré-computadas. Contudo, se o hash subjacente for rápido (ex.: `MD5` ou `SHA-256`), um atacante com GPUs testa milhares de milhões de candidatas por segundo contra cada credencial individual. É por isso obrigatório combinar *salt* único com **`Key Stretching`** lento (`Argon2` > `PBKDF2` > `scrypt` > `bcrypt`), que torna cada tentativa dispendiosa em CPU/RAM sem prejudicar o login legítimo.

### 12. Explique o risco operacional do caso `FortiBleed` (2026) e do incidente de *SAS Tokens* da Microsoft AI (2023).
> [!success]- Ver Tópicos de Resposta
> * **`FortiBleed` (2026):** ataque de agregação que reuniu credenciais válidas de `86,644` firewalls Fortinet (fugas antigas, força bruta, configurações via `CVE-2018-13379` e hashes quebrados) que permaneceram utilizáveis por falta de **rotação de passwords** pós-incidente e ausência de **2FA**.
> * **Microsoft AI / `Wiz` (2023):** publicação no GitHub de um **`Account-level SAS`** (para toda a conta de armazenamento, 18 contentores, validade 2020–2051) em vez de um *Blob/Service SAS* restrito, expondo **38 TB** de backups privados, segredos internos e >30 000 mensagens do Teams.

---

## Gabarito — Grupo I

| # | Resposta | Referência para Rever |
| :---: | :---: | :--- |
| **1** | **C** | [[Sanitização e Destruição de Discos Magnéticos (HDDs) - Wiping, Degaussing e Destruição Física]] · [[Arquitetura SSD e Memória NAND (Wear Leveling e Garbage Collection)]] |
| **2** | **C** | [[Gestão de Ativos (Asset Management) e Políticas de Armazenamento Amovível (VeraCrypt)]] |
| **3** | **A** | [[Pen Drives USB Falsas e Verificação com ValiDrive (Ficha 11)]] |
| **4** | **D** | [[System e OS Hardening e Vulnerabilidade BitLocker YellowKey (CVE-2026-45585)]] |
| **5** | **B** | [[Smishing, Estações SMS Blaster (Downgrade 2G) e Quishing (Códigos QR)]] |
| **6** | **A** | [[Segurança de Passwords, Paradigma xkcd e Diretrizes NIST (2003 vs SP 800-63-4)]] |
| **7** | **D** | [[Entropia de Passwords e Entropia de Ficheiros (ent e Detect It Easy)]] |
| **8** | **B** | [[Limite do bcrypt (Okta Bypass), Credential Stuffing e Caso FortiBleed]] |
| **9** | **C** | [[Autenticação 2FA (Protocolo TOTP RFC 6238) e Passkeys (FIDO2 - WebAuthn e CTAP)]] |
| **10** | **A** | [[Cracking e Auditoria de Passwords com Hashcat (Hashcat 101 e Máscaras)]] |

---

## Navegação

- [[Capítulo 2 - Administração de Sistemas|Voltar ao MOC do Capítulo 2]]
- [[Cheat Sheet - Administração de Sistemas e Controlo de Acessos|Consultar a Cheat Sheet do Capítulo 2]]
- [[00 ASSI|Voltar ao Índice Geral de ASSI]]
