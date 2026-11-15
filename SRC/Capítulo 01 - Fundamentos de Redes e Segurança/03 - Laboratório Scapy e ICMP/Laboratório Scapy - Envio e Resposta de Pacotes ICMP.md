---
title: Laboratório Scapy - Envio e Resposta de Pacotes ICMP
tipo: procedimento
mestrado: Cibersegurança e Informática Forense
uc: Segurança em Redes de Computadores
sigla_uc: SRC
capitulo: 1
bloco: 3
fonte_aula: 1scapy.py; pinging.py
tags:
  - src
  - scapy
  - icmp
  - python
  - redes
aliases:
  - Scapy ICMP
  - 1scapy.py
  - pinging.py
atualizado: 2026-11-15
---

# Laboratório Scapy — Envio e Resposta de Pacotes ICMP

Os scripts laboratoriais `pinging.py` e `1scapy.py` demonstram a manipulação programática de pacotes **ICMP** em Python utilizando a biblioteca `scapy` para envio de *probes* com *payload* personalizado e resposta automática (*spoofing*/echo reply) via *sniffing*.

> [!TIP] Lógica de Funcionamento e Valor de Segurança
> * **Porque existe (Redes / Teste)**: O `scapy` permite construir, injetar e analisar pacotes camada a camada (`IP() / ICMP() / payload`) sem depender das limitações de ferramentas padrão como o `ping`.
> * **Porque importa (Segurança)**: Demonstra na prática como o tráfego de rede pode ser inspecionado (`sniff`) e forjado (`IP(src=..., dst=...)`), evidenciando que a ausência de autenticação na camada IP/ICMP permite *spoofing* e canais encobertos em *payload*.
> * **Pontos Críticos e Armadilhas para Exame**:
>   * Em `1scapy.py`, o respondedor copia `id` e `seq` do pedido ICMP original e define `type=0, code=0` (*Echo Reply*), trocando `src` e `dst` do cabeçalho IP.
>   * A execução de `sniff()` e `send()` em *raw sockets* requer privilégios elevados (`root` / `CAP_NET_RAW`).

---

## 1. Envio de Pacote ICMP Personalizado (`pinging.py`)

O script `pinging.py` constrói um pacote IP/ICMP dirigido a `8.8.8.8` com uma string de *payload* personalizada e envia-o na camada 3 com `send()`:

```python
# Instalar scapy: pip install scapy
from scapy.all import *

print("pinging... 8.8.8.8")
ip = "8.8.8.8"
icmp = IP(dst=ip)/ICMP()/"HELP ME OBI-WAN KENOBY, YOU'RE MY ONLY HOPE"
resp = send(icmp)
print(resp)
```

* **`IP(dst=ip)/ICMP()/"..."`**: O operador `/` no `scapy` empilha camadas protocolares (Rede -> ICMP -> Dados).
* **`send(icmp)`**: Envia o pacote na camada 3 (sem esperar resposta, ao contrário de `sr1()`).

---

## 2. Sniffer e Respondedor Automático ICMP (`1scapy.py`)

O script `1scapy.py` fica em escuta contínua por pacotes ICMP (`filter='icmp'`), extrai os campos do pedido e envia um *ICMP Echo Reply* (`type=0, code=0`) com o *payload* `"Welcome to MCIF"`:

```python
import scapy.all as scapy

def icmp_responder():
    try:
        while True:
            packet = scapy.sniff(filter='icmp', count=1)
            if packet:
                request = packet[0]
                reply = (
                    scapy.IP(src=request[scapy.IP].dst, dst=request[scapy.IP].src)
                    / scapy.ICMP(
                        type=0,
                        code=0,
                        id=request[scapy.ICMP].id,
                        seq=request[scapy.ICMP].seq
                    )
                    / "Welcome to MCIF"
                )
                scapy.send(reply, verbose=False)
    except KeyboardInterrupt:
        print("Script terminated.")
```

| Campo Construído na Resposta | Origem / Valor | Finalidade |
| :--- | :--- | :--- |
| `IP(src=..., dst=...)` | `src = request[IP].dst`, `dst = request[IP].src` | Inverte origem e destino para devolver ao remetente |
| `ICMP(type=0, code=0)` | Constante `0 / 0` | Indica *ICMP Echo Reply* |
| `id` e `seq` | Copiados de `request[ICMP]` | Permite ao cliente associar a resposta ao pedido original |
| Payload | `"Welcome to MCIF"` | Dados personalizados transportados na resposta ICMP |

---

## Perguntas de revisão

1. **Porque é que `1scapy.py` copia os campos `id` e `seq` do pacote `request[scapy.ICMP]` para o pacote de resposta?**

> [!success]- Ver Resposta
> Porque o emissor original utiliza o identificador (`id`) e o número de sequência (`seq`) ICMP para correlacionar cada *Echo Reply* (`type=0, code=0`) com o respetivo *Echo Request* enviado.

2. **Qual a diferença entre usar `send()` em `pinging.py` e construir `IP(src=..., dst=...)` em `1scapy.py`?**

> [!success]- Ver Resposta
> `send()` envia um pacote construído na camada 3 sem aguardar resposta; ao especificar explicitamente `src=` no cabeçalho `IP()`, o `scapy` permite definir o endereço IP de origem (útil para responder em nome do destino original ou demonstrar *IP spoofing*).

## Notas relacionadas

- [[Modelo TCP-IP, Encapsulamento e Visibilidade de Tráfego HTTPS]]
- [[Conceitos de Segurança - CIA, Vulnerabilidade, Ameaça, Ataque e RFC 4949]]
