---
title: SRC — Segurança em Redes de Computadores
tipo: indice
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
tags:
  - moc
  - src
  - redes
  - seguranca
aliases:
  - SRC
  - 00 SRC
  - Segurança em Redes de Computadores
  - Security in Computer Networks
atualizado: 2026-11-15
---

# Segurança em Redes de Computadores (SRC)

Unidade curricular do **Mestrado em Cibersegurança e Informática Forense (MCIF)** da **Escola Superior de Tecnologia e Gestão (ESTG)** do **Politécnico de Leiria**.

* **Docente**: Luís Frazão (Departamento de Engenharia Informática — DEI; slides do Módulo 2 por Mário Antunes)
* **Semestre**: 1.º Semestre

---

## Programa e Capítulos

| Capítulo                                               | Designação                                                                                                                                                                                                                                                                                                                                                                                                                 | Estado / Cobertura                                                           |
| :----------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| **[[Capítulo 1 - Fundamentos de Redes e Segurança]]**  | **Fundamentos de Redes e Segurança**<br/>Arquitetura TCP/IP e encapsulamento, visibilidade de tráfego HTTPS, governação da Internet (IXPs, cabos submarinos, DNS/AS, RFCs), conceitos de segurança (NIST, CIA, `RFC 4949`), serviços e mecanismos (`X.800`), princípios de desenho seguro, *attack surfaces*, *attack trees* e laboratório `scapy`/ICMP.                                                                   | Concluído (26 slides + Stallings Cap. 1 + 2 scripts `scapy`, 6 notas)        |
| **[[Capítulo 2 - Criptografia Aplicada]]**             | **Criptografia Aplicada (*Applied Cryptography*)**<br/>Modelo convencional e criptanálise, cifras clássicas, cifras de blocos (`Feistel`, `DES`, `AES`) vs. *stream* (`RC4`), criptografia assimétrica e `RSA`, funções de *hash* (`MD5`, `SHA-2`, `SHA-3`, `RIPEMD`), `MAC`/`HMAC`, assinaturas digitais, PKI/`OpenSSL`, `GnuPG`, `SSH`, `TLS 1.3`, `IPSec`/`OpenVPN` e `TBL #2`.                                         | Concluído (77 slides + Stallings + TBL #2, 9 notas + 1 Cheat Sheet)          |
| **[[Capítulo 3 - Segurança em IoT]]**                  | **Segurança em IoT (*Internet of Things Security*)**<br/>Desafios e ataques por camada IoT (*Perception*, *Network*, *Application*, *Processing*, *Business*), requisitos específicos e contramedidas (*Sharma*), segurança em `BLE` (*Pairing Feature Exchange*, *LE Legacy* vs. *LE Secure Connections* — *Lacava*), `LPWAN` e arquitetura/modelo de ameaças `LoRaWAN` (*Stanco*) e `TBL #3` (`MQTT`, `BLE`, `LoRaWAN`). | Concluído (3 artigos — secções destacadas + TBL #3, 6 notas + 1 Cheat Sheet) |
| **[[Capítulo 4 - Deteção de Intrusões e Zero Trust]]** | **Deteção de Intrusões (IDS) e *Zero Trust Architecture* (ZTA)**<br/>Taxonomia de `IDS` (`SIDS` vs. técnicas híbridas, `HIDS`/`NIDS`, fontes de dados, matriz de confusão e métricas, evasão e desafios — *Khraisat et al.*) e fundamentos de *Zero Trust Architecture* (`NIST SP 800-207`: princípios, componentes lógicos `PE`/`PA`/`PEP`, `PKI`/`ID Management` e separação *Control Plane* vs. *Data Plane*).          | Concluído (2 documentos — secções destacadas, 3 notas)                       |

### Folhas de Consulta Rápida (Cheat Sheets de Apoio)

* **[[Cheat Sheet - Criptografia, Hash, PKI e VPNs]]**: Guia de bolso do Capítulo 2 para notação criptográfica, simétrica vs. assimétrica, propriedades de *hash*/`MAC`, `OpenSSL` CA, `GnuPG`, `SSH` e `IPSec`/`OpenVPN`.
* **[[Cheat Sheet - Segurança em IoT (BLE, LoRaWAN e MQTT)]]**: Guia de bolso do Capítulo 3 para camadas IoT, modos de emparelhamento `BLE`, chaves e servidores `LoRaWAN` e segurança em `MQTT`.

---

## Fontes Oficiais Mapeadas

* **Módulo 1**: `1_fundamentals.pdf` (26 slides), `ch1_Computer_Network_Security_Concepts.pdf` (Stallings, Cap. 1 — 27 pág.), `1scapy.py`, `pinging.py`.
* **Módulo 2**: `aula_02_update.pdf` (68 slides — Mário Antunes), `2_crypto_projectKickoff.pdf` (9 slides), `aula02_leituras_resumo.pdf` (Stallings, Cap. 3, 4, 9, 10.12, 11, 12 — 62 pág.), `TBL_Cryptography_EN_202627.pdf` (10 questões).
* **Módulo 3** *(secções destacadas a amarelo)*: `Sharma_yellow.pdf` (*Sharma & Bhushan, 2026*), `Lacava_yellow.pdf` (*Lacava et al., 2022*), `Stanco_yellow.pdf` (*Stanco et al., 2024*), `TBL_3_EN_IoT.pdf` (10 cenários).
* **Módulo 4** *(secções destacadas a amarelo)*: `s42400-019-0038-7.pdf` (*Khraisat et al., 2019 — Survey of IDS*), `NIST.SP.800-207.pdf` (*NIST SP 800-207 — Zero Trust Architecture*).

---

## Navegação

* [[Home|Voltar ao Hub Central do MCIF]]
