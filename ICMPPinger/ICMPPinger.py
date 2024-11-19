import os
import socket
import struct
import select
import time

# Definição de constantes
temporizador = time.time  # Temporizador padrão
REQUISICAO_ICMP = 8       # Código para "Echo Request"

def calcular_checksum(dados):
    soma = 0
    comprimento_pares = (len(dados) // 2) * 2
    contador = 0

    while contador < comprimento_pares:
        valor = dados[contador + 1] * 256 + dados[contador]
        soma = soma + valor
        soma = soma & 0xffffffff
        contador = contador + 2

    if comprimento_pares < len(dados):
        soma = soma + dados[len(dados) - 1]
        soma = soma & 0xffffffff

    soma = (soma >> 16) + (soma & 0xffff)
    soma = soma + (soma >> 16)
    resultado = ~soma
    resultado = resultado & 0xffff
    resultado = resultado >> 8 | (resultado << 8 & 0xff00)
    return resultado

def receber_ping(socket_ping, identificador, tempo_limite):
    tempo_restante = tempo_limite
    while True:
        inicio_selecao = temporizador()
        pronto = select.select([socket_ping], [], [], tempo_restante)
        duracao_selecao = (temporizador() - inicio_selecao)
        if pronto[0] == []:
            return None

        tempo_recebido = temporizador()
        pacote_recebido, endereco = socket_ping.recvfrom(1024)
        cabecalho_icmp = pacote_recebido[20:28]
        tipo, codigo, checksum, id_pacote, sequencia = struct.unpack("bbHHh", cabecalho_icmp)

        if id_pacote == identificador:
            if tipo == 0:  # Echo Reply
                tamanho_tempo = struct.calcsize("d")
                tempo_envio = struct.unpack("d", pacote_recebido[28:28 + tamanho_tempo])[0]
                return tempo_recebido - tempo_envio
            else:
                if tipo == 3:  # Destination Unreachable
                    mensagens_erro = {
                        0: "Rede de Destino Inalcançável",
                        1: "Host de Destino Inalcançável",
                        2: "Protocolo Inalcançável",
                        3: "Porta Inalcançável",
                        4: "Fragmentação Necessária",
                        5: "Rota de Origem Falhou",
                    }
                    mensagem_erro = mensagens_erro.get(codigo, "Erro ICMP desconhecido")
                    print(f"Erro ICMP: {mensagem_erro}")
                    return None

        tempo_restante = tempo_restante - duracao_selecao
        if tempo_restante <= 0:
            return None

def enviar_ping(socket_ping, endereco_destino, identificador):
    endereco_destino = socket.gethostbyname(endereco_destino)
    checksum_inicial = 0
    cabecalho = struct.pack("bbHHh", REQUISICAO_ICMP, 0, checksum_inicial, identificador, 1)
    tamanho_tempo = struct.calcsize("d")
    dados = (192 - tamanho_tempo) * "Q"
    dados = struct.pack("d", temporizador()) + dados.encode('utf-8')
    checksum_calculado = calcular_checksum(cabecalho + dados)
    cabecalho = struct.pack(
        "bbHHh", REQUISICAO_ICMP, 0, socket.htons(checksum_calculado), identificador, 1
    )
    pacote = cabecalho + dados
    socket_ping.sendto(pacote, (endereco_destino, 1))

def realizar_ping(endereco_destino, tempo_limite):
    protocolo_icmp = socket.getprotobyname("icmp")
    try:
        socket_ping = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocolo_icmp)
    except socket.error as erro:
        codigo_erro, mensagem = erro.args
        if codigo_erro == 1:
            mensagem = mensagem + (
                " - Note que mensagens ICMP só podem ser enviadas por processos com privilégios de administrador."
            )
        raise socket.error(mensagem)

    identificador = os.getpid() & 0xFFFF
    enviar_ping(socket_ping, endereco_destino, identificador)
    atraso = receber_ping(socket_ping, identificador, tempo_limite)
    socket_ping.close()
    return atraso

def ping(endereco_destino, tempo_limite=1, total_pacotes=4):
    tempos_rtt = []
    pacotes_perdidos = 0

    for i in range(total_pacotes):
        print("ping %s..." % endereco_destino, end=" ")
        try:
            atraso = realizar_ping(endereco_destino, tempo_limite)
        except socket.gaierror as erro:
            print("falhou. (erro de socket: '%s')" % erro.args[1])
            pacotes_perdidos = total_pacotes
            break

        if atraso is None:
            print("falhou. (timeout dentro de %s seg.)" % tempo_limite)
            pacotes_perdidos += 1
        else:
            atraso = atraso * 1000
            tempos_rtt.append(atraso)
            print("Ping realizado em %0.4fms" % atraso)

        time.sleep(1)  # Espera de 1 segundo entre os pings

    if tempos_rtt:
        rtt_min = min(tempos_rtt)
        rtt_max = max(tempos_rtt)
        rtt_media = sum(tempos_rtt) / len(tempos_rtt)
    else:
        rtt_min = rtt_max = rtt_media = 0.0

    perda_pacotes = (pacotes_perdidos / total_pacotes) * 100

    print("\n--- %s Estatísticas ---" % endereco_destino)
    print("%d pacotes enviados, %d pacotes recebidos, %.1f%% de perda de pacotes" % (
        total_pacotes, total_pacotes - pacotes_perdidos, perda_pacotes))
    if tempos_rtt:
        print("RTT min/média/máx = %.3f/%.3f/%.3f ms" % (rtt_min, rtt_media, rtt_max))
    else:
        print("Nenhuma resposta recebida.")

if __name__ == '__main__':
    ping("naoexisteredesweb.com")
    ping("127.0.0.1")
    ping("us.archive.ubuntu.com")
    ping("sg.archive.ubuntu.com")
    ping("de.archive.ubuntu.com")
    ping("au.archive.ubuntu.com")