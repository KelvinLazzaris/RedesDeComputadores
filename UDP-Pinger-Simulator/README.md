# Servidor e Cliente UDP em Python


# UDP Pinger Simulator

Este projeto implementa um simulador de **Ping via UDP** utilizando sockets em Python. Ele inclui um cliente e um servidor, que trabalham juntos para medir o tempo de ida e volta (**RTT**) de pacotes e simular condições de rede não confiável, como perda de pacotes.

## Objetivo
O objetivo do projeto é demonstrar os fundamentos do uso de sockets UDP para enviar e receber pacotes, calcular estatísticas de desempenho e simular condições reais de redes baseadas em UDP.

## Funcionalidades

### Cliente (pingerClient.py)
- Envia **10 pacotes Ping** para o servidor.
- Mede o **tempo de ida e volta (RTT)** de cada pacote.
- Registra pacotes perdidos e calcula a **taxa de perda de pacotes**.
- Exibe:
  - Resposta do servidor.
  - RTT de cada pacote.
  - Estatísticas finais: RTT mínimo, máximo, médio e taxa de perda.

### Servidor (pingerServer.py)
- Escuta pacotes UDP na porta especificada.
- Simula **perda de pacotes** em 40% dos casos, para emular redes não confiáveis.
- Retorna a mensagem enviada pelo cliente em **maiúsculas**.
- Responde apenas quando o pacote não é "perdido".