---
title: Footprinting - Conceitos, Objetivos e Motores de Pesquisa (Google Hacking)
tipo: conceito
mestrado: Cibersegurança e Informática Forense
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
capitulo: 3
bloco: 1
fonte_aula: 2026.27_MCIF_COD1_03_Reconhecimento_Footprinting.pdf (Slides 3–25)
tags: [cod1, footprinting, google-hacking, shodan, censys, netcraft]
aliases: [Footprinting, Google Hacking, Google Dorks, Shodan]
criado: 2026-11-15
atualizado: 2026-11-16
---

# Footprinting - Conceitos, Objetivos e Motores de Pesquisa (Google Hacking)

O *footprinting* é a primeira fase de recolha passiva de informação pública sobre a rede, sistemas e organização alvo através de motores de pesquisa (`Google`, `Netcraft`, `Shodan`, `Censys`) e operadores avançados (*Google Dorks*).

> [!TIP] Lógica de Funcionamento e Valor Operacional
> * **Porque existe (Sistema)**: Motores web e indexadores da Internet (`Shodan`, `Censys`) indexam continuamente páginas, documentos e serviços expostos sem interação direta do auditor.
> * **Porque importa (Pentesting / Segurança)**: Permite desenhar o mapa da rede, reduzir áreas de foco, descobrir páginas de login, tecnologias e fugas de ficheiros antes de enviar um único pacote de *port scan*.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * `Google` indexa conteúdo web/documentos (`site:`, `inurl:`, `intitle:`, `filetype:`), enquanto `Shodan`/`Censys` indexam **IPs, portos, banners e certificados**.
>   * Anúncios de emprego revelam a pilha tecnológica interna; caches de pesquisa preservam páginas já apagadas.

## 1. Conceito e Valor do Footprinting

**Footprinting** é o processo sistemático de recolha e angariação do maior número possível de informações sobre um alvo, reunindo dados sensíveis disponibilizados publicamente para identificar formas de espoletar intrusões nas suas redes e sistemas.

Os quatro resultados estratégicos do footprinting são:
1. **Conhecimento da postura de segurança:** Avaliar a maturidade e visibilidade pública da organização.
2. **Redução das áreas de foco:** Delimitar endereços IP, tipos de rede, nomes de domínio e acessos remotos específicos.
3. **Identificação de vulnerabilidades:** Selecionar ferramentas e técnicas adequadas às tecnologias reais descobertas.
4. **Desenho do mapa da rede:** Construir uma visão estruturada da infraestrutura exposta.

## 2. Objetivos de Recolha (Rede, Sistemas e Organização)

| Domínio | Informação a Recolhar |
| :--- | :--- |
| **Rede** | Nomes de domínio (externos e internos), blocos de endereços IP, IPs de sistemas acessíveis, serviços TCP/UDP disponíveis, protocolos de rede, controlos de acesso/autenticação, acessos remotos (`VPN`), fornecedores de `firewall` e `IDS/IPS`. |
| **Sistemas** | Nomes de utilizadores e grupos, nomes de sistemas (*hostnames*), serviços TCP/UDP, tabelas de encaminhamento, arquitetura dos sistemas, informações `SNMP`, tipo de acesso remoto, banners do sistema. |
| **Organização** | Detalhes sobre funcionários e estrutura orgânica, website e links internos/externos, localizações físicas e contactos telefónicos, endereços de e-mail, políticas de segurança publicadas, histórico/background, notícias e *press releases*. |

## 3. Motores de Pesquisa Especializados e Descoberta de Infraestrutura

- **Motores de pesquisa generalistas (`Google`, `Bing`, `DuckDuckGo`, `Yandex`):** Permitem descobrir portais públicos/restritos, páginas de login, intranets e unidades de negócio; caches de pesquisa preservam páginas entretanto apagadas.
- **`Netcraft` (`sitereport.netcraft.com`, `searchdns.netcraft.com`):** Identifica o sistema operativo, tecnologias web, subdomínios e histórico de *hosting*.
- **`Shodan` (`shodan.io`):** Motor de pesquisa de dispositivos ligados à Internet. Suporta filtros por tags como `city:`, `country:`, `geo:`, `hostname:`, `net:`, `os:`, `port:`, `category:`, `product:` (ex.: `city:Leiria port:80`, `hostname:ipleiria`, ou dorks em `github.com/nullfuzz-pentest/shodan-dorks`).
- **`Censys` (`censys.io`), `Fullhunt` (`fullhunt.io`), `FOFA` (`fofa.info`):** Motores para descoberta de hosts, certificados, domínios e serviços expostos (ex. no Censys: `location.country_code: PT and location.city: Leiria`, `"OpenSSH" AND operating_system.vendor: "debian"`).
- **Geolocalização e Infraestrutura Física:** `Google Maps`, `Google Earth`, `OpenStreetMap`, `bing.com/maps`, `Wikimapia` (úteis para reconhecer instalações, antenas, acessos físicos e perímetro).
- **Pesquisa de Pessoas e Outras Fontes:**
  - Redes sociais (`LinkedIn`, `Facebook`) e agregadores (`usersearch.org`, `social-searcher.com`, `spokeo.com`).
  - E-mails corporativos (`hunter.io`), informação financeira (`google.com/finance`), fóruns/blogs e **ofertas de emprego** (que revelam stack tecnológico, hardware, software e perfis internos).
  - Monitorização contínua com `google.com/alerts`.

## 4. Google Hacking Footprinting (Google Dorks)

O **Google Hacking** utiliza operadores avançados de pesquisa para construir *strings* complexas que localizam ficheiros sensíveis, diretórios expostos, credenciais ou servidores vulneráveis.

| Operador | Função | Exemplo Prático |
| :--- | :--- | :--- |
| `site:` | Restringe a pesquisa a um domínio/site | `filetype:pdf site:www.ipleiria.pt` |
| `inurl:` | Procura termos no URL | `inurl:admin` / `inurl:login inurl:user inurl:pass` |
| `intitle:` | Procura no título da página | `intitle:index.of` / `intitle:index.of.admin` |
| `intext:` | Procura no corpo de texto da página | `-intext:pass intext:user` |
| `filetype:` | Filtra por extensão de ficheiro | `"ceo" "email" "@" filetype:xls OR filetype:csv` |
| `cache:` | Mostra a versão em cache no Google | `cache:alvo.pt` |
| `link:` | Procura páginas que apontam para um URL | `link:alvo.pt` |
| `related:` | Procura páginas semelhantes | `related:alvo.pt` |
| `info:` | Apresenta resumo indexado do URL | `info:alvo.pt` |
| `index of` | Localiza listagens de diretórios abertas | `intitle:"index of" backup` |
| Operador OR | Operador booleano OU (símbolo pipe) | `filetype:xls OR filetype:csv` |
| `-` | Exclui termo dos resultados | `-site:www.alvo.pt site:alvo.pt` |

- **Repositório de referência:** **Google Hacking Database (GHDB)** em `exploit-db.com/google-hacking-database`.
- **Automatização:** Ferramentas como o `Pagodo` (`github.com/opsdisk/pagodo`) automatizam consultas GHDB contra domínios alvo.

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Técnicas adicionais úteis ao realizar footprinting passivo de uma organização:

- **Enumeração de Subdomínios via Certificate Transparency (CT Logs):** Serviços como `crt.sh` consultam registos públicos de emissão de certificados TLS/SSL (Let's Encrypt, DigiCert, etc.), revelando subdomínios internos ou recentes (`vpn.`, `dev.`, `staging.`) sem enviar qualquer tráfego aos servidores DNS do alvo.
- **Google Dorks Direcionados a Fugas Corporativas:** Combinar `site:alvo.pt` com `ext:env OR ext:sql OR ext:bak OR ext:log OR ext:conf` ou pesquisar `site:s3.amazonaws.com "alvo"` e `site:azurewebsites.net "alvo"` permite detetar buckets e aplicações cloud associadas à organização.

## Perguntas de revisão

1. **Qual a diferença operacional entre usar o `Google` e usar o `Shodan`/`Censys` no footprinting inicial?**
   > [!success]- Ver Resposta
   > O `Google` indexa sobretudo páginas web, documentos e diretórios HTTP/HTTPS através de crawlers web, enquanto o `Shodan` e o `Censys` varrem diretamente os endereços IP e portos da Internet, indexando banners de serviços (SSH, RDP, SMB, VNC, câmaras, IoT), sistemas operativos e certificados TLS expostos.

2. **Que informação estratégica pode ser extraída a partir de anúncios de ofertas de emprego de uma organização alvo?**
   > [!success]- Ver Resposta
   > Os anúncios de emprego revelam frequentemente a pilha tecnológica interna (versões de sistemas operativos, firewalls, SIEMs, linguagens de desenvolvimento, bases de dados, fornecedores cloud) e os perfis de equipa, auxiliando tanto na escolha de vetores técnicos como no desenho de pretextos de engenharia social.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[Capítulo 3 - Rastreamento e Reconhecimento]] | Início do capítulo |
| **Seguinte** | [[OSINT - Plataformas (GitHub, Trello), Redes Sociais, Website e E-mail]] | `muda para Bloco 02` |
| **Índice** | [[Capítulo 3 - Rastreamento e Reconhecimento]] · [[00 COD1]] | `Bloco 01` |

### Conceitos Relacionados

* [[WHOIS, DNS, Networking Footprinting e Engenharia Social]] · `Bloco 03`
* [[Footprinting Pentest e Contramedidas (Metodologia Prática)]] · `Bloco 04`
