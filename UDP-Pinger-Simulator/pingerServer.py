import random
from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Configurar o servidor para escutar na porta especificada
serverSocket.bind(('', serverPort))
print(f"Servidor UDP de Ping ativo na porta {serverPort}...")

while True:
    # Gerar número aleatório para simular perda de pacotes
    rand = random.randint(0, 10)

    # Receber pacote do cliente
    message, address = serverSocket.recvfrom(1024)
    message = message.upper()  # Transformar a mensagem para maiúsculas

    # Simular perda de pacote se o número aleatório for menor que 4
    if rand < 4:
        print("Simulando perda de pacote.")
        continue

    # Responder ao cliente
    serverSocket.sendto(message, address)
    print(f"Respondendo ao cliente {address} com a mensagem: {message.decode()}")
