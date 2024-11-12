from socket import *

# Configuração do endereço e porta do servidor
serverName = 'localhost'
serverPort = 6789

# Criar o socket do cliente
clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    # Estabelecer conexão com o servidor
    clientSocket.connect((serverName, serverPort))

    # Enviar solicitação HTTP ao servidor
    request = "GET /index.html HTTP/1.1\r\nHost: localhost\r\n\r\n"
    clientSocket.send(request.encode())

    # Receber e acumular a resposta do servidor
    response = b""
    while True:
        part = clientSocket.recv(4096)
        if not part:
            break
        response += part

    # Extrair e exibir o conteúdo do corpo da resposta HTTP, se presente
    response_str = response.decode()
    if '\r\n\r\n' in response_str:
        headers, body = response_str.split('\r\n\r\n', 1)
        print('Conteúdo do Arquivo:')
        print(body)
    else:
        print('Resposta incompleta ou inválida do servidor:')
        print(response_str)

except Exception as e:
    print(f'Ocorreu um erro: {e}')

finally:
    # Encerrar o socket do cliente
    clientSocket.close()