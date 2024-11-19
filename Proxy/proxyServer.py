from socket import *
import sys
import os


if len(sys.argv) <= 1:
    print('Uso: "python ProxyServer.py server_ip"\n[server_ip: Endereço IP do Servidor Proxy]')
    sys.exit(2)


# Cria um socket do servidor, vincula-o a uma porta e começa a escutar
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], 8888))
tcpSerSock.listen(5)
print("Proxy server iniciado e escutando na porta 8888...")


# Estrutura de dados para cache
cache = {}


def save_to_cache(filename, content):
    with open(filename, "w") as f:
        f.write(content)


def get_from_cache(filename):
    try:
        with open(filename, "r") as f:
            return f.read()
    except FileNotFoundError:
        return None


while True:
    print('Pronto para servir...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('Conexão aceita de:', addr)


    # Recebe a mensagem do cliente
    message = tcpCliSock.recv(1024).decode()
    print("Mensagem recebida:", message)


    # Extrai o nome do arquivo da mensagem
    try:
        filename = message.split()[1].partition("/")[2]
        print("Nome do arquivo solicitado:", filename)
    except IndexError:
        print("Erro: Formato de solicitação inválido.")
        tcpCliSock.send("HTTP/1.0 400 Bad Request\r\n\r\n".encode())
        tcpCliSock.close()
        continue


    # Verifica se o arquivo está no cache
    if filename in cache:
        print("Arquivo encontrado no cache. Enviando resposta ao cliente.")
        content = get_from_cache(cache[filename])
        if content:
            tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
            tcpCliSock.send(content.encode())
            print('Resposta enviada do cache')
        else:
            print("Erro: Conteúdo do cache não encontrado.")
            tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode())
            tcpCliSock.close()
            continue
    else:
        # Cria um socket no servidor proxy
        c = socket(AF_INET, SOCK_STREAM)
        hostn = filename.replace("www.", "", 1)
        print("Conectando ao servidor:", hostn)


        try:
            # Conecta ao servidor na porta 80
            c.connect((hostn, 80))
            c.sendall(f"GET / HTTP/1.0\r\nHost: {filename}\r\n\r\n".encode())


            # Lê a resposta do servidor remoto
            response = c.recv(4096).decode()
            print("Resposta recebida do servidor remoto.")


            # Verifica o código de status da resposta
            status_line = response.split("\r\n")[0]
            if "404 Not Found" in status_line:
                print("Arquivo não encontrado no servidor remoto.")
                tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode())
                tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
                tcpCliSock.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())
            else:
                # Armazena no cache e envia a resposta ao cliente
                tcpCliSock.send(response.encode())
                # Salva a resposta no cache
                cache[filename] = f"./{filename}"
                save_to_cache(cache[filename], response)
                print("Arquivo armazenado no cache.")


        except Exception as e:
            print("Erro na solicitação:", e)
            tcpCliSock.send("HTTP/1.0 502 Bad Gateway\r\n".encode())
            tcpCliSock.send("Content-Type:text/html\r\n\r\n".encode())
            tcpCliSock.send("<html><body><h1>502 Bad Gateway</h1></body></html>\r\n".encode())


    tcpCliSock.close()