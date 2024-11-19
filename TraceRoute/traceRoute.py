from socket import *
import os
import struct
import time
import select

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 5
TIMEOUT = 2.0
TRIES = 2

def checksum(data):
    csum = 0
    count_to = (len(data) // 2) * 2
    count = 0

    while count < count_to:
        this_val = (data[count + 1]) * 256 + (data[count])
        csum += this_val
        csum &= 0xffffffff
        count += 2

    if count_to < len(data):
        csum += (data[len(data) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet():
    my_checksum = 0
    ID = os.getpid() & 0xFFFF

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    data = struct.pack("d", time.time())

    my_checksum = checksum(header + data)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, htons(my_checksum), ID, 1)
    packet = header + data
    return packet

def get_route(hostname):
    try:
        dest_addr = gethostbyname(hostname)
    except gaierror as e:
        print(f"Erro ao resolver o hostname: {e}")
        return

    print(f"Rastreando rota para {hostname} ({dest_addr})")

    for ttl in range(1, MAX_HOPS + 1):
        for tries in range(TRIES):
            try:
                # Cria um socket ICMP com privilégios de root (pode exigir sudo)
                with socket(AF_INET, SOCK_RAW, IPPROTO_ICMP) as my_socket:
                    my_socket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
                    my_socket.settimeout(TIMEOUT)

                    # Constrói e envia o pacote
                    packet = build_packet()
                    my_socket.sendto(packet, (hostname, 0))
                    send_time = time.time()

                    # Espera por uma resposta
                    what_ready = select.select([my_socket], [], [], TIMEOUT)
                    if what_ready[0] == []:  # Nenhuma resposta
                        print(f"{ttl}    *        *        *    Request timed out.")
                        continue

                    # Recebe o pacote e processa o tempo
                    recv_packet, addr = my_socket.recvfrom(1024)
                    recv_time = time.time()

                    icmp_header = recv_packet[20:28]
                    types, code, checksum, packet_id, sequence = struct.unpack("bbHHh", icmp_header)

                    if packet_id == os.getpid() & 0xFFFF:
                        try:
                            host = gethostbyaddr(addr[0])[0]
                        except herror:
                            host = addr[0]

                        rtt = (recv_time - send_time) * 1000
                        if types == 11:
                            print(f"  {ttl}    rtt={rtt:.0f} ms    {addr[0]} ({host})")
                        elif types == 3:
                            print(f"  {ttl}    rtt={rtt:.0f} ms    {addr[0]} ({host})")
                        elif types == 0:
                            print(f"  {ttl}    rtt={rtt:.0f} ms    {addr[0]} ({host})")
                            return
            except timeout:
                print(f"{ttl}    *        *        *    Request timed out.")
            except error as e:
                print(f"Erro ao enviar/receber pacote ICMP: {e}")
                return

# América do Norte
get_route("8.8.8.8")

# Europa
get_route("80.67.169.40")

# Ásia
get_route("202.14.67.4")

# Oceania
get_route("139.130.4.5")