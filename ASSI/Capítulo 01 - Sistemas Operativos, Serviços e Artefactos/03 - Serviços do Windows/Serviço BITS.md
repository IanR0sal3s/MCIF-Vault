---
title: Serviço BITS
mestrado: Cibersegurança e Informática Forense
uc: Administração Segura de Sistemas Informáticos
sigla_uc: ASSI
capitulo: 1
bloco: 3
tipo: conceito
tags:
  - assi
  - windows
  - servicos
  - bits
  - lolbin
  - forense
aliases:
  - BITS
  - Background Intelligent Transfer Service
  - bitsadmin
  - BitsParser
fonte_aula: 01_FA_services+WSearch+Registry---2026-27_ULO_v4.pdf
atualizado: 2026-11-21
---

# Serviço BITS (Background Intelligent Transfer Service)

O **BITS (*Background Intelligent Transfer Service*)** é um serviço do Windows que corre em processo partilhado via [[svchost.exe]] e utiliza **períodos de inatividade da rede** (largura de banda ociosa) para transferir ficheiros em segundo plano.

## 1. Utilização Legítima vs. Abuso Malicioso

* **Usos legítimos**: Windows Update, Microsoft Store e atualizações em segundo plano.
* **Uso malicioso**: é frequentemente abusado por software malicioso (como *Living off the Land*) para descarregar *payloads* ou exfiltrar dados de forma discreta através de um processo legítimo do sistema (`svchost.exe`).

---

## Além da aula

* **Gestão CLI**: o utilitário nativo `bitsadmin` permite criar/consultar tarefas (ex.: `bitsadmin /transfer <nome> /download /priority normal <URL> <caminho_absoluto>`).
* **Evidências forenses**:
  * **Event Log**: `Microsoft-Windows-Bits-Client/Operational` (Event ID `3` = início, `4` = conclusão, `59`/`60` = alterações de estado).
  * **Base de dados ESE**: `C:\ProgramData\Microsoft\Network\Downloader\qmgr.db` (e `edb.log`), analisável *post-mortem* (incluindo *carving* de entradas apagadas) com `BitsParser.py --carvedb -i qmgr.db`.

---

## Perguntas de revisão

1. **Qual a função do serviço BITS e em que modelo de processo corre?**

> [!success]- Ver Resposta
> Transfere ficheiros em segundo plano usando largura de banda ociosa da rede (ex.: Windows Update, Microsoft Store). Corre em processo partilhado alojado no `svchost.exe`.

2. **Porque é que o BITS é atrativo para software malicioso?**

> [!success]- Ver Resposta
> Porque permite transferir ficheiros (descarregar *payloads* ou exfiltrar dados) usando um componente nativo confiável do Windows (`svchost.exe`), reduzindo a probabilidade de deteção.

---

## Navegação e Notas Relacionadas

| Percurso | Nota | Contexto |
| :--- | :--- | :--- |
| **Anterior** | [[svchost.exe]] | `mesmo bloco` |
| **Seguinte** | [[Serviço Delivery Optimization]] | `mesmo bloco` |
| **Índice** | [[Capítulo 1 - Sistemas Operativos, Serviços e Artefactos Forenses]] · [[00 ASSI]] | `Bloco 03` |

### Conceitos Relacionados

* [[Serviços Windows]] · `mesmo bloco`
* [[Windows Search]] · `mesmo bloco`
