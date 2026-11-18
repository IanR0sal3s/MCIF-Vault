---
title: OSINT - Plataformas (GitHub, Trello), Redes Sociais, Website e E-mail
tipo: tecnica
mestrado: Cibersegurança e Informática Forense
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
capitulo: 3
bloco: 2
fonte_aula: 2026.27_MCIF_COD1_03_Reconhecimento_Footprinting.pdf (Slides 26–40)
tags: [cod1, osint, github, redes-sociais, website-footprinting, email-footprinting]
aliases: [OSINT GitHub, Website Footprinting, E-mail Footprinting]
criado: 2026-11-15
atualizado: 2026-11-16
---

# OSINT - Plataformas (GitHub, Trello), Redes Sociais, Website e E-mail

A recolha OSINT em plataformas colaborativas (`GitHub`, `Trello`, `Pastebin`), redes sociais, websites e cabeçalhos de e-mail expõe segredos em código, tecnologias web e rotinas internas da organização.

> [!TIP] Lógica de Funcionamento e Valor Operacional
> * **Porque existe (Sistema)**: Ferramentas de colaboração pública, cabeçalhos HTTP/SMTP e arquivos históricos (`archive.org`) preservam metadados técnicos e organizacionais.
> * **Porque importa (Pentesting / Segurança)**: Revela credenciais esquecidas em commits, versões de CMS/servidores (`Server`, `X-Powered-By`), estrutura de ficheiros offline (`HTTrack`/`wget`) e vetores de *spear phishing*.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Apagar uma chave num commit posterior do `GitHub` não a remove do histórico (ferramentas: `gitleaks`, `gitrob`, `keyhacks`).
>   * Cabeçalhos `Received:` em e-mails revelam IPs de origem e servidores SMTP intermédios.

## 1. Plataformas de Partilha de Código e Informação (`GitHub`, `Trello`, `Pastebin`)

Plataformas colaborativas e repositórios públicos (`GitHub`, `Trello`, `Bitbucket`, `Sharecode`, `Pastebin`, `searchcode.com`) são fontes frequentes de fugas acidentais de credenciais, chaves privadas e configurações internas:

- **Pesquisa manual com GitHub Dorks:** Analisar repositórios e histórico de *commits* usando termos como:
  - `"filename:.ftpconfig"`
  - `"filename:.dockercfg auth"`
  - `"extension: pem private"`
  - `"filename: id_rsa"`
  - Coleções de dorks: `github.com/techgaun/github-dorks`.
- **Validação de API Keys:** `github.com/streaak/keyhacks` ajuda a verificar se chaves de API descobertas continuam ativas e quais as permissões associadas.
- **Automação no GitHub:** `gitleaks`, `secret-bridge` (Duo Labs), `gitrob` e `gitGraber` varrem repositórios, organizações e commits históricos em busca de segredos.

## 2. Footprinting Através das Redes Sociais

Atacantes recorrem frequentemente a perfis falsos e engenharia social passiva/ativa para recolher informação junto de colaboradores (datas de nascimento, CVs, familiares, eventos corporativos, fornecedores, parceiros e URLs internos).

| Fonte (Ações) | O que o Atacante Obtém |
| :--- | :--- |
| **Utilizadores — Atualizações de perfil** | Contactos, localização, cargo atual. |
| **Utilizadores — Ligações/comentários/fotos** | Rede de amigos, familiares e hábitos. |
| **Utilizadores — Grupos, jogos, eventos** | Interesses e atividades (útil para *spear phishing*). |
| **Organizações — Inquéritos e promoções** | Estratégia de negócio e identificação de produtos. |
| **Organizações — Suporte ao utilizador** | Vetores para engenharia social (*helpdesk*). |
| **Organizações — Recrutamento e background checks** | Informações sobre infraestrutura e tipo de negócio. |

## 3. Website Footprinting e Recolha Competitiva

O **Website Footprinting** analisa o sítio web da organização para identificar software/versões, sistema operativo, subdiretórios, parâmetros URL, campos/queries de base de dados, scripting e CMS:

- **Análise de Cabeçalhos HTTP e Código-Fonte:**
  - Cabeçalhos relevantes: `Connection`, `Content-Type` (MIME), `Server`, `X-Powered-By`.
  - No código-fonte: comentários de programadores, estrutura de ficheiros e scripts.
  - Ferramentas: `HTTP Header Live`, `Wappalyzer`, `BuiltWith` (`builtwith.com`), `URLcrazy`, `pentest-tools.com`, `99webtools.com/link-extractor.php`.
- **Web Crawlers / Spiders:** Extração automatizada de nomes, e-mails e ficheiros (`urlscan.io`, `metagoofil`, `GSA Email Spider`, `Web Data Extractor`).
- **Site Mirroring (Cópia Offline):** Descarregar integralmente o site para análise offline de diretórios e ficheiros ocultos usando `HTTrack` / `WebHTTrack` ou `wget`:
  ```bash
  wget -mk -w 10 http://alvo.exemplo/
  ```
- **Versões Antigas (Histórico Web):** `archive.org` (Wayback Machine) e `netcraft.com` permitem recuperar ficheiros, páginas ou código-fonte entretanto removidos.
- **Informação Competitiva:** Responder a *When, How, Who, Where* (início de atividade, evolução, liderança, localizações), relatórios de contas, planos de negócio, monitorização de tráfego (`alexa.com`, `web-stat`) e reputação online / ORM (`trackur.com`, `rankur.com`).

## 4. E-mail Footprinting

- **Análise de Cabeçalhos de E-mail:** Permite extrair endereço IP do remetente, servidores SMTP por onde a mensagem passou (`Received:`), datas/horas exatas de envio e receção e mecanismos de autenticação (SPF/DKIM/DMARC). Ferramentas de apoio: `ipaddresslocation.org/email-tracking/email-header.php`, `whatismyipaddress.com/trace-email`.
- **Tracking de E-mails Enviados:** Serviços como `whoreadme.com`, `yesware.com` ou `zendio.com` registam quando a mensagem foi lida, cliques em links, abertura de anexos, tempo de leitura, dispositivo e localização aproximada.

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Técnicas complementares de OSINT organizacional antes da fase de scanning ativo:

- **Análise de Metadados de Documentos (`ExifTool`):** Complementando o `metagoofil` e o `FOCA`, transferir PDFs, `.docx` e `.xlsx` indexados pelo Google (`site:alvo.pt filetype:pdf`) e correr `exiftool *.pdf` revela nomes de utilizadores internos da rede, versões exatas de software de escritório (Microsoft Office, Adobe, LibreOffice) e caminhos internos de servidores de ficheiros.
- **Breach & Credential Intelligence:** Verificar se e-mails corporativos (`@alvo.pt`) surgiram em fugas de dados públicas anteriores (ex.: `Have I Been Pwned` ou bases de *credential stuffing*) ajuda a avaliar o risco de reutilização de passwords em portais VPN/OWA, sempre respeitando estritamente o âmbito autorizado.

## Perguntas de revisão

1. **Porque é que a análise do histórico de commits no `GitHub` é mais eficaz do que apenas olhar para o estado atual do repositório?**
   > [!success]- Ver Resposta
   > Porque mesmo que um programador apague uma password, chave SSH (`id_rsa`) ou API key num commit posterior, o segredo permanece registado nos commits anteriores do histórico Git, podendo ser detetado por ferramentas como `gitleaks` ou `gitrob`.

2. **Que dados técnicos podem ser obtidos através dos cabeçalhos HTTP e do *site mirroring*?**
   > [!success]- Ver Resposta
   > Os cabeçalhos HTTP (`Server`, `X-Powered-By`, `Content-Type`) expõem o servidor web, linguagens/frameworks e versões, enquanto o *site mirroring* (`HTTrack`, `wget -mk`) copia toda a árvore de diretórios e ficheiros para análise offline de comentários no código-fonte, paths e parâmetros.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Footprinting - Conceitos, Objetivos e Motores de Pesquisa (Google Hacking)]] | `Bloco 01` |
| **Seguinte** | [[WHOIS, DNS, Networking Footprinting e Engenharia Social]] | `muda para Bloco 03` |
| **Índice** | [[Capítulo 3 - Rastreamento e Reconhecimento]] · [[00 COD1]] | `Bloco 02` |

### Conceitos Relacionados

* [[Footprinting Pentest e Contramedidas (Metodologia Prática)]] · `Bloco 04`
