---
title: Enumeração SMTP, DNS, FTP, IPsec e VoIP (SIP)
tipo: tecnica
mestrado: Cibersegurança e Informática Forense
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
capitulo: 5
bloco: 3
fonte_aula: 2026.27_MCIF_COD1_05_Enumeracao.pdf (Slides 31–46)
tags: [cod1, enumeracao, smtp, dns, ftp, ipsec, voip, sip, autorecon]
aliases: [Enumeração SMTP, DNS Zone Transfer, Enumeração IPsec, Enumeração VoIP]
criado: 2026-11-15
atualizado: 2026-11-16
---

# Enumeração SMTP, DNS, FTP, IPsec e VoIP (SIP)

A enumeração de serviços de perímetro e infraestrutura (`SMTP`, `DNS`, `FTP`, `IPsec`, `VoIP/SIP`) extrai contas válidas, zonas DNS completas (`AXFR`), ficheiros anónimos, parâmetros de VPN e extensões telefónicas.

> [!TIP] Lógica de Funcionamento e Valor Operacional
> * **Porque existe (Sistema)**: Protocolos de correio, resolução de nomes, transferência de ficheiros, VPN e telefonia IP expõem comandos de diagnóstico ou negociação.
> * **Porque importa (Pentesting / Segurança)**: Revela utilizadores válidos para *phishing*/*password spraying*, mapas internos via `AXFR` e algoritmos fracos em gateways VPN (`ike-scan`).
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Os 3 comandos SMTP de enumeração são **`VRFY`**, **`EXPN`** e **`RCPT TO`**.
>   * **`500/UDP` (`ISAKMP`)** identifica gateways VPN IPsec enumeráveis com `ike-scan`; **`SIP`** usa tipicamente `2000`, `2001`, `5050` e `5061` TCP/UDP.

## 1. Enumeração SMTP (`TCP 25`)

O protocolo SMTP disponibiliza três comandos que podem revelar se uma conta de utilizador existe no servidor quando este responde de forma distinta para utilizadores válidos e inválidos:
- **`VRFY`:** Valida diretamente se um utilizador existe.
- **`EXPN`:** Devolve o endereço real de entrega de aliases e listas de distribuição (*mailing lists*).
- **`RCPT TO`:** Define o destinatário de uma mensagem (usado durante uma sessão SMTP simulada para testar entregas válidas).

```bash
# Ligação manual interativa
telnet <endereço> 25

# Automação com smtp-user-enum
smtp-user-enum -M VRFY -D <dominio> -u <user_ou_wordlist> -t <SMTP_server>

# Scripts Nmap NSE e Metasploit
nmap --script-help "smtp-*"
# Metasploit: search smtp scanner
```

## 2. Enumeração DNS — Transferência de Zona (`TCP/UDP 53`)

A **transferência de zona (`AXFR`)** tenta obter uma cópia integral de todos os registos da zona DNS de um domínio configurados num servidor DNS autoritativo.

```bash
# Com host
host -t ns <dominio>
host -l <dominio> <DNS_server>

# Com dig
dig <dominio> any
dig @<DNS_server> <dominio> axfr

# Ferramentas dedicadas e Nmap
dnsrecon -d <dominio> -t axfr
dnsenum <dominio>
nmap --script=dns-zone-transfer -p 53 <DNS_server>
```

## 3. Enumeração FTP (`TCP 21`)

Na enumeração FTP verifica-se sobretudo se o acesso **anónimo** (`anonymous`) está ativo, as permissões de leitura/escrita e a versão do servidor:

```bash
# Scripts NSE seguros
nmap --script-help "*ftp* and safe"
sudo nmap -p 21 --script ftp-syst <IP>
sudo nmap -p 21 --script "*ftp* and safe" <IP>

# Teste manual de login anónimo e comandos básicos
ftp <IP>   # user: anonymous | comandos: dir, get, put, delete, mkdir

# Força bruta (apenas se autorizado no âmbito)
nmap --script ftp-brute --script-args userdb=users.txt,passdb=pass.txt -p 21 <IP>
```

## 4. Enumeração IPsec (`UDP 500`)

As VPNs **IPsec** recorrem a `ESP`, `AH` e `IKE` (`ISAKMP` no porto **`500/UDP`**) para negociar Associações de Segurança (`SA`) e chaves criptográficas. Um scan ao porto `500/UDP` confirma a presença do endpoint VPN e o `ike-scan` enumera algoritmos de cifra, hash, tipo de autenticação (ex.: Pre-Shared Key), grupo Diffie-Hellman e tempo de vida da SA:

```bash
sudo nmap -sU -p 500 <IP>
sudo ike-scan -M <IP>
```

## 5. Enumeração VoIP (`SIP`)

Os sistemas **VoIP** utilizam o protocolo **SIP** (*Session Initiation Protocol*) tipicamente nos portos **`2000`, `2001`, `5050` e `5061` TCP/UDP** para chamadas de voz/vídeo.

- **Dados enumeráveis:** gateways/servidores VoIP, sistemas IP-PBX, software cliente (*softphones*) e extensões telefónicas.
- **Riscos associados:** ataques DoS, *session hijacking*, *caller ID spoofing*, escutas, *SPIT* (Spam over Internet Telephony) e *Vishing* (VoIP phishing).
- **Ferramentas:** `svmap <IP>` (suíte `SIPVicious`) e módulos Metasploit (`search sip scanner`).

## 6. Automação Integrada de Reconhecimento e Enumeração: `AutoRecon`

A ferramenta **`AutoRecon`** (`github.com/Tib3rius/AutoRecon`) automatiza o fluxo multi-thread de scanning Nmap seguido da execução automática de ferramentas de enumeração específicas para cada porto/serviço descoberto (HTTP, SMB, SNMP, FTP, DNS, etc.), organizando os resultados numa árvore de diretorias por alvo.

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Pontos de atenção práticos durante auditorias externas e internas:

- **IPsec IKEv1 Aggressive Mode (`ike-scan -A`):** Se um gateway VPN IPsec antigo suportar *Aggressive Mode* com autenticação PSK, envia o hash da Pre-Shared Key sem proteção de identidade, permitindo captura com `ike-scan -A -P<ficheiro>` e tentativa de cracking offline com `psk-crack` / `hashcat`.
- **Enumeração de Utilizadores SMTP sem `VRFY`:** Servidores modernos desativam `VRFY`/`EXPN`, mas frequentemente continuam a responder `250 OK` vs. `550 User unknown` ao comando `RCPT TO` — por isso vale testar `-M RCPT` no `smtp-user-enum` quando `-M VRFY` falha.

## Perguntas de revisão

1. **Quais são os três comandos SMTP utilizados para tentar validar contas de utilizador e listas de distribuição?**
   > [!success]- Ver Resposta
   > `VRFY` (valida utilizadores), `EXPN` (expande aliases e listas de mailing) e `RCPT TO` (testa destinatários válidos).

2. **Que informações criptográficas podem ser enumeradas num endpoint VPN IPsec (`500/UDP`) com `ike-scan`?**
   > [!success]- Ver Resposta
   > Algoritmos de cifra e hash suportados, tipo de autenticação, algoritmo de distribuição de chaves (Diffie-Hellman) e tempo de vida da Associação de Segurança (SA).

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Enumeração SNMP (Community Strings, MIB e OIDs)]] | `Bloco 02` |
| **Seguinte** | [[Contramedidas de Enumeração e Metodologia Pentest]] | `muda para Bloco 04` |
| **Índice** | [[Capítulo 5 - Enumeração]] · [[00 COD1]] | `Bloco 03` |

### Conceitos Relacionados

* [[Conceitos de Enumeração e Enumeração NetBIOS, SMB e LDAP]] · `Bloco 01`
* [[Redes Privadas Virtuais (VPN) - IPSec e OpenVPN]] · `SRC · Cap. 2`
