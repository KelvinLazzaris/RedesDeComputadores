import time
from socket import *

serverName = "127.0.0.1"
serverPort = 12000

# Criar um socket UDP
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)  # Definir tempo limite de 1 segundo para respostas

# Inicializar variáveis para estatísticas
total_pings = 10
rtts = []  # Lista para armazenar tempos de ida e volta (RTTs)
lost_packets = 0  # Contador de pacotes perdidos

# Enviar 10 pacotes Ping para o servidor
for sequence_number in range(1, total_pings + 1):
    # Mensagem com número de sequência e horário de envio
    message = f"Ping {sequence_number} {time.time()}"
    try:
        # Registrar tempo de envio do pacote
        send_time = time.time()
        # Enviar mensagem ao servidor
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        
        # Receber resposta do servidor
        response, serverAddress = clientSocket.recvfrom(1024)
        # Registrar tempo de recebimento e calcular o RTT
        receive_time = time.time()
        rtt = receive_time - send_time
        rtts.append(rtt)

        # Exibir resposta e RTT
        print(f"Resposta do servidor: {response.decode()}")
        print(f"RTT: {rtt:.4f} segundos")
    except timeout:
        # Caso o tempo limite seja excedido, registrar perda
        print("Requisição expirou")
        lost_packets += 1

# Fechar o socket após enviar os pings
clientSocket.close()

# Cálculo de estatísticas
if rtts:
    min_rtt = min(rtts)
    max_rtt = max(rtts)
    avg_rtt = sum(rtts) / len(rtts)
    packet_loss_rate = (lost_packets / total_pings) * 100

    # Exibir estatísticas finais
    print("\n--- Estatísticas do Ping ---")
    print(f"RTT mínimo: {min_rtt:.4f} segundos")
    print(f"RTT máximo: {max_rtt:.4f} segundos")
    print(f"RTT médio: {avg_rtt:.4f} segundos")
    print(f"Taxa de perda de pacotes: {packet_loss_rate:.2f}%")
else:
    print("Nenhum pacote foi recebido.")
