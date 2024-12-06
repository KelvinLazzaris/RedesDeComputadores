# Script de Ping em Python

Este repositório contém um script Python que implementa a funcionalidade de ping usando o protocolo ICMP para medir a latência de rede até um host especificado.

## Descrição

Este script de ping envia pacotes ICMP "Echo Request" para um endereço de destino especificado e aguarda por uma resposta "Echo Reply". Ele mede o tempo de ida e volta (RTT) desses pacotes para calcular a latência da rede. Além disso, o script pode detectar quando os pacotes são perdidos e calcular estatísticas de perda de pacotes e tempos de resposta.

## Funcionalidades

### Calcular Checksum
- **Função**: `calcular_checksum`
- **Descrição**: Esta função calcula o checksum de um pacote ICMP para garantir a integridade dos dados enviados e recebidos. O checksum é necessário para validar a integridade de cada pacote ICMP.

### Enviar Ping
- **Função**: `enviar_ping`
- **Descrição**: Prepara e envia um pacote ICMP "Echo Request" para um endereço de destino. A função empacota o cabeçalho e os dados do ICMP, calcula o checksum e envia o pacote através de um socket raw.

### Receber Ping
- **Função**: `receber_ping`
- **Descrição**: Aguarda e recebe a resposta ICMP "Echo Reply". A função verifica se o pacote recebido corresponde ao pacote enviado (usando identificador) e calcula o tempo de ida e volta baseado no timestamp incluído no pacote de resposta.

### Realizar Ping
- **Função**: `realizar_ping`
- **Descrição**: Combina as funcionalidades de enviar e receber ping para calcular o atraso (latência) para um único pacote.

### Ping
- **Função**: `ping`
- **Descrição**: Executa múltiplos pings para um destino, calcula e exibe estatísticas como RTT mínimo, médio, máximo e percentual de perda de pacotes.

## Pré-requisitos

- Python 3.x
- Privilegios de administrador/root (necessário para criar e enviar pacotes ICMP)
- Conexão de rede ativa

## Como Usar

1. Clone o repositório para sua máquina local.
2. Execute o script em um terminal como administrador/root para evitar problemas de permissão com sockets raw:

```bash
python iccmppinger.py
