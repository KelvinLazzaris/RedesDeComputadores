from socket import *
import sys
import threading

# Função para lidar com cada conexão do cliente
def handle_client(connectionSocket):
    try:
        # Receber e decodificar a mensagem do cliente
        message = connectionSocket.recv(1024).decode()
        
        # Processamento da solicitação: extração e envio do arquivo solicitado
        if len(message.split()) > 1:
            filename = message.split()[1]
            
            # Leitura do conteúdo do arquivo solicitado
            with open(filename[1:]) as f:
                outputdata = f.read()

            # Resposta de sucesso ao cliente
            connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())

        else:
            # Resposta de erro para solicitações mal-formadas
            connectionSocket.send('HTTP/1.1 400 Bad Request\r\n\r\n'.encode())
            connectionSocket.send("<html><head></head><body><h1>400 Bad Request</h1></body></html>\r\n".encode())

    except IOError:
        # Resposta de erro para arquivo não encontrado
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

    finally:
        # Encerrar o socket do cliente
        connectionSocket.close()


# Configuração do servidor
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(5)

print('Servidor pronto para receber conexões...')

# Loop principal para aceitar e lidar com conexões de clientes
while True:
    connectionSocket, addr = serverSocket.accept()
    print(f'Conexão estabelecida com: {addr}')

    # Criação de uma nova thread para cada conexão do cliente
    client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
    client_thread.start()

# Fechar o servidor (código nunca atingido devido ao loop infinito)
serverSocket.close()
sys.exit()