# Servidor e Cliente TCP em Python

Este repositório contém um exemplo de um **servidor** e um **cliente** TCP em Python, onde o servidor é capaz de processar requisições HTTP simples de um cliente para fornecer arquivos solicitados.

## Descrição do Projeto

O projeto demonstra uma comunicação básica entre cliente e servidor utilizando **sockets TCP**. O servidor é configurado para aceitar conexões de clientes e enviar arquivos solicitados por eles, simulando o comportamento de um servidor HTTP básico.

### Arquivos

- **`websocket.py`**: Código do servidor que aceita conexões de clientes, interpreta solicitações HTTP e retorna o conteúdo do arquivo solicitado. Caso o arquivo não seja encontrado, responde com um erro 404 (Not Found).
- **`cliente.py`**: Código do cliente que se conecta ao servidor, envia uma solicitação HTTP para obter um arquivo específico e exibe a resposta recebida.

## Funcionamento do Servidor (`websocket.py`)

1. Cria um socket TCP IPv4 usando `AF_INET` e `SOCK_STREAM`.
2. Usa `bind()` para associar o socket a um endereço IP (localhost) e uma porta específica (6789).
3. Coloca o servidor em modo de escuta com `listen(5)`, permitindo que ele aceite até 5 conexões pendentes.
4. Entra em um loop infinito para aceitar conexões de clientes.
5. Cada conexão aceita é atendida em uma nova thread para permitir múltiplas conexões simultâneas.
6. A função `handle_client` processa cada solicitação:
   - Interpreta o caminho do arquivo solicitado pelo cliente.
   - Retorna o conteúdo do arquivo solicitado com um cabeçalho `200 OK`, ou um erro `404 Not Found` se o arquivo não for encontrado.
   - Caso a solicitação esteja malformada, retorna um erro `400 Bad Request`.

## Funcionamento do Cliente (`cliente.py`)

1. Cria um socket TCP IPv4 e se conecta ao servidor (`localhost` na porta `6789`).
2. Envia uma solicitação HTTP `GET` para o arquivo especificado (por exemplo, `index.html`).
3. Recebe a resposta do servidor em blocos de 4096 bytes.
4. Decodifica e exibe o conteúdo do arquivo, ou exibe uma mensagem de erro se o arquivo não for encontrado ou se a solicitação estiver incorreta.

## Como Executar

1. Clone este repositório para o seu ambiente local.
2. Execute o servidor:
   ```bash
   python websocket.py
3. Em uma nova janela do terminal, execute o cliente:
   ```bash
   python cliente.py

O cliente enviará uma solicitação para o servidor e exibirá o conteúdo do arquivo solicitado, caso ele exista.
