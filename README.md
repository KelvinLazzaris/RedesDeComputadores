# RedesDeComputadores

## Coleção de Projetos de Redes em Python

Este repositório contém uma variedade de implementações relacionadas a redes utilizando Python. Cada subprojeto demonstra conceitos fundamentais de redes como ICMP ping, servidores proxy, comunicação SMTP, traceroute, simulações de ping usando UDP e servidores web simples.

## Projetos Inclusos

### ICMP Pinger
- **Descrição**: Implementa um comando de ping usando o protocolo ICMP para medir a latência entre hosts.
- **Funcionalidades**: Envio e recebimento de pacotes ICMP, cálculo de RTTs, e apresentação de estatísticas de ping.
- **Arquivo Principal**: `icmppinger.py`

### Proxy Server
- **Descrição**: Um servidor proxy simples que pode armazenar conteúdos em cache para reduzir a latência e carga na rede.
- **Funcionalidades**: Interceptação de requisições HTTP, caching de conteúdo, e simulação de um comportamento de rede real com perda de pacotes.
- **Arquivo Principal**: `proxyserver.py`

### SMTP Communication
- **Descrição**: Script para enviar e-mails usando o protocolo SMTP diretamente através de sockets.
- **Funcionalidades**: Autenticação SMTP, envio de e-mails com suporte a anexos usando codificação base64.
- **Arquivo Principal**: `smtp.py`

### Traceroute
- **Descrição**: Um script para realizar o traceroute para um host remoto, mostrando a rota que os pacotes tomam na rede.
- **Funcionalidades**: Envio de pacotes ICMP, rastreamento de rotas, e identificação de pontos de falha na rota.
- **Arquivo Principal**: `traceroute.py`

### Pinger Simulator
- **Descrição**: Simula o envio e recebimento de pacotes ping usando o protocolo UDP, incluindo a simulação de perda de pacotes.
- **Funcionalidades**: Envio de pacotes UDP, medição de RTTs, cálculo de estatísticas de perda de pacotes.
- **Arquivos Principais**: `pingerClient.py`, `pingerServer.py`

### Web Server
- **Descrição**: Um servidor web básico que pode servir páginas HTML e manipular múltiplas conexões de clientes simultaneamente.
- **Funcionalidades**: Recebimento e processamento de solicitações HTTP, resposta com conteúdos estáticos como páginas HTML, e tratamento de erros HTTP.
- **Arquivos Principais**: `cliente.py`, `index.html`, `websocket.py`

## Pré-requisitos

- Python 3.x
- Privilegios de administrador/root para alguns scripts que necessitam de acesso a sockets raw.
- Conexão de rede ativa para testar a funcionalidade de rede.

## Como Usar

Cada subdiretório dentro deste repositório contém scripts individuais. Para executar qualquer script:
1. Navegue até o diretório do subprojeto.
2. Execute o script usando Python. Por exemplo:
   ```bash
   python icmppinger.py
