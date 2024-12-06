# Traceroute em Python

Este repositório contém uma implementação de um rastreador de rotas ICMP (Internet Control Message Protocol) em Python. O script realiza o rastreamento de rotas para vários destinos globais utilizando pacotes ICMP.

## Descrição

O Traceroute é uma ferramenta de diagnóstico de rede que rastreia a rota que os pacotes tomam da máquina local até um host remoto. Este script customiza essa funcionalidade para capturar o caminho de IP sobre o qual os pacotes de rede viajam.

## Funcionalidades

### Envio de Pacotes ICMP
- O script envia pacotes ICMP "Echo Request" para rastrear a rota até o host de destino. Cada pacote tem um TTL (Time to Live) diferente, que aumenta incrementalmente para descobrir cada salto (hop) na rota.

### Cálculo do Tempo de Ida e Volta (RTT)
- Para cada pacote enviado, o script mede o tempo que leva para receber uma resposta, conhecido como RTT. Esse tempo é crucial para entender a latência da rede entre o host local e cada ponto de passagem até o destino.

### Determinação do Número Máximo de Saltos (Hops)
- O script define um limite de saltos (`MAX_HOPS`) para evitar loops infinitos na resolução de rotas. Isso garante que o script conclua a execução mesmo se o destino final não puder ser alcançado dentro de um número razoável de saltos.

### Identificação de Cada Salto na Rota até o Destino
- O script utiliza o TTL dos pacotes ICMP para identificar e imprimir cada salto na rota até o destino. Cada resposta recebida é associada a um endereço IP, que é resolvido para um nome de host, se possível, fornecendo uma visão clara da rota da rede.

## Pré-requisitos

Para executar este script, você precisará:

- Python 3.x
- Privilegios de administrador/root (necessário para criar sockets ICMP)
- Acesso à internet

## Como Usar

1. Clone o repositório para seu local de trabalho.
2. Abra um terminal como administrador/root.
3. Execute o script com o comando:

```bash
python traceroute.py
