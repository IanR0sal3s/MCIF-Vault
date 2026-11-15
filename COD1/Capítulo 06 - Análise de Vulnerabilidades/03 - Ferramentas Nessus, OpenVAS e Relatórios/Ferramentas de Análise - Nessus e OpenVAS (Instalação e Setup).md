---
title: "Ferramentas de Análise - Nessus e OpenVAS (Instalação e Setup)"
uc: Cibersegurança Ofensiva e Defensiva I
sigla_uc: COD1
tipo: nota
capitulo: 6
topico: ferramentas-nessus-openvas
tags: [cod1, nessus, openvas, gvm, nikto, nmap-nse, relatorios]
---
# Ferramentas de Análise - Nessus e OpenVAS (Instalação e Setup)

**Capítulo:** [[Capítulo 6 - Análise de Vulnerabilidades]]

> [!TIP] Lógica de Funcionamento e Valor Operacional
> O `Nessus` e o `OpenVAS` (`Greenbone Vulnerability Management`) automatizam milhares de verificações de vulnerabilidades conhecidas, configurações fracas e patches em falta, enquanto o `Nikto` e os scripts `NSE` do `Nmap` oferecem verificação rápida via linha de comandos.

## 1. Panorama de Ferramentas de Análise de Vulnerabilidades

- **Infraestrutura e Rede:** `Nessus` (`tenable.com/nessus`), `OpenVAS` (`openvas.org`), `Nexpose` (`rapid7.com/nexpose`), `Qualys` (`qualys.com`), `GFI LanGuard` (`gfi.ai/languard`), `SAINT` (`carson-saint.com`), `beSECURE/Fortra`.
- **Aplicações Web:** `Nikto`, `Burp Suite` / `Dastardly`, `Acunetix`, `Vega`, `Uniscan` / `RapidScan`.
- **Nmap NSE (Scripts de Vulnerabilidades):** Localizados em `/usr/share/nmap/scripts/` (`scripts.db`).
  - Distinção crítica: scripts **`safe`** vs. **`intrusive`** (os intrusivos podem explorar falhas ou causar instabilidade).
  ```bash
  # Listar scripts de vulnerabilidade/exploit
  cat /usr/share/nmap/scripts/scripts.db | grep -E '"vuln"|"exploit"'

  # Executar scripts de vulnerabilidades
  nmap --script=<script.nse> <IP>
  nmap -sV --script vulners <IP>
  nmap -sV --script vulscan <IP>
  ```
- **Nikto (Scanner Web CLI):** Opções principais referidas na aula: `-H` (ajuda), `-h` (host alvo), `-ssl` (forçar SSL/HTTPS), `-p` (porto), `-T` (tuning de testes).

## 2. Instalação e Setup do **Nessus** (Kali Linux)

1. Descarregar o pacote `.deb` oficial do Nessus (ex.: `Nessus-10.12.6-debian10_amd64.deb` via `tenable.com/downloads/nessus`).
2. Instalar e iniciar o serviço:
   ```bash
   sudo dpkg -i Nessus-10.12.6-debian10_amd64.deb
   sudo systemctl start nessusd.service
   ```
3. Aceder à interface web em `https://127.0.0.1:8834`, escolher **Nessus Essentials** (licença gratuita para até 16 IPs de laboratório), registar nome/e-mail para receber o código de ativação, definir utilizador/password e aguardar a compilação dos plugins.
4. **Uso prático:** Explorar políticas de scan (básico, avançado e **autenticado** com credenciais SSH/SMB para reduzir falsos negativos), seleção de plugins e análise de relatórios.

## 3. Instalação e Setup do **OpenVAS / GVM** (Kali Linux)

1. Atualizar repositórios e instalar o OpenVAS:
   ```bash
   sudo apt update && sudo apt install openvas -y
   ```
2. Configurar e validar a instalação:
   ```bash
   sudo gvm-setup
   sudo gvm-check-setup
   sudo gvm-start
   ```
   *(Guardar a password gerada para o utilizador `admin` durante o `gvm-setup`.)*
3. Aceder à interface web em `https://127.0.0.1:9392`.

### Troubleshooting Comum no Setup do OpenVAS (PostgreSQL & Feeds)
- **Erro de versão do PostgreSQL (ex.: cluster 14 vs. 15):** Verificar clusters com `pg_lsclusters`. Se existir um cluster vazio na versão 15 e os dados estiverem na 14:
  ```bash
  sudo pg_dropcluster 15 main --stop
  sudo pg_upgradecluster 14 main
  ```
- **Erro de feed SCAP / NVT desatualizado:**
  ```bash
  sudo greenbone-feed-sync --type SCAP
  ```

## 4. Relatórios de Análise de Vulnerabilidades

Os relatórios gerados por ferramentas como `Nessus` e `OpenVAS` revelam os riscos detetados após o varrimento, alertam para possíveis vetores de ataque, ordenam falhas por severidade (`CVSS`) e sugerem contramedidas concretas para orientar a equipa de sistemas na remediação.

## Além da aula

> [!NOTE] Conteúdo Complementar (Além da aula)
> Boas práticas ao utilizar scanners automáticos num pentest organizacional:

- **Scans Autenticados vs. Não Autenticados:** Um scan não autenticado vê apenas a superfície externa; num pentest *grey-box* ou auditoria interna, um scan autenticado (com conta SSH ou domínio de leitura) no `Nessus`/`OpenVAS` revela imediatamente *patches* em falta e software local vulnerável com muito menos falsos positivos.
- **Validação Manual Obrigatória:** Scanners baseiam-se frequentemente em *banner matching* (ver apenas a versão anunciada pelo servidor, ignorando *backports* de segurança aplicados por distribuições como Debian/RHEL). Antes de reportar uma vulnerabilidade Crítica/Alta, valide sempre o achado manualmente ou confirme a versão exata do pacote.

## Perguntas de revisão

1. **Em que portos locais ficam acessíveis as interfaces web do `Nessus` e do `OpenVAS` após instalação?**
   > [!success]- Ver Resposta
   > O `Nessus` escuta por omissão em `https://127.0.0.1:8834` e o `OpenVAS` (`GVM`) em `https://127.0.0.1:9392`.

2. **Qual a diferença entre scripts NSE `safe` e `intrusive` no `Nmap`?**
   > [!success]- Ver Resposta
   > Scripts `safe` limitam-se a recolher informação sem explorar falhas nem perturbar o serviço, enquanto scripts `intrusive` podem tentar explorar ativamente vulnerabilidades ou causar indisponibilidade/crashes nos sistemas alvo.

## Notas relacionadas
- [[Análise e Gestão de Vulnerabilidades - Ciclo de Vida e Classificação]]
- [[Sistemas de Pontuação (CVSS e CVE) e Abordagens de Avaliação]]
- [[Cheat Sheet - Playbook de Pentesting e Footprinting Organizacional]]
