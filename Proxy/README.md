# Proxy Server em Python

Este repositório contém um script Python para um servidor proxy simples que intercepta solicitações HTTP, podendo servir conteúdo de um cache local ou buscá-lo de um servidor remoto, dependendo da disponibilidade.

## Descrição

O servidor proxy funciona como um intermediário para solicitações de clientes buscando recursos de outros servidores. Ele melhora a eficiência e a velocidade do acesso a recursos frequentemente solicitados ao armazenar cópias locais e reduzir a carga sobre os servidores remotos.

## Funcionalidades

### Inicialização do Servidor
- **Função**: Executada no início do script
- **Descrição**: O script inicia configurando e vinculando um socket do servidor a uma porta específica (8888 por padrão) e começa a escutar solicitações.

### Gerenciamento de Cache
- **Funções**: `save_to_cache`, `get_from_cache`
- **Descrição**: Estas funções gerenciam o cache do servidor. `save_to_cache` armazena conteúdo no cache local, enquanto `get_from_cache` tenta recuperar conteúdo do cache, reduzindo a necessidade de acessar o servidor remoto.

### Processamento de Solicitações
- **Localização no código**: Loop principal `while True`
- **Descrição**: O servidor aceita conexões de clientes, lê suas mensagens, extrai a URL solicitada e verifica se o conteúdo solicitado já está em cache. Se estiver, o servidor responde diretamente do cache; se não, ele busca o recurso no servidor remoto.

### Tratamento de Erros
- **Descrição**: O script trata vários casos de erro, como formatos de solicitação inválidos e falhas na conexão com o servidor remoto, enviando as respostas de erro HTTP adequadas (400, 404, 502) para o cliente.

## Pré-requisitos

- Python 3.x
- Conhecimento básico de protocolos de rede, especialmente TCP/IP e HTTP
- Acesso à internet para testes com servidores remotos

## Como Usar

1. Clone o repositório para sua máquina local.
2. Execute o script em um terminal:

```bash
python proxyServer.py <server_ip>
