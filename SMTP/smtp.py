import ssl
from socket import *
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def criar_socket():
    try:
        # Configuração do servidor de e-mail
        mailserver = ('smtp.gmail.com', 587)
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect(mailserver)
        resposta = clientSocket.recv(1024).decode()
        print(f"Resposta do servidor (Conexão): {resposta}")
        if resposta[:3] != '220':
            raise Exception("Erro ao conectar ao servidor SMTP.")
        return clientSocket
    except Exception as e:
        raise Exception(f"Erro ao criar o socket: {e}")

def iniciar_tls(clientSocket):
    try:
        # Iniciar TLS
        clientSocket.send('STARTTLS\r\n'.encode())
        resposta = clientSocket.recv(1024).decode()
        print(f"Resposta do servidor (STARTTLS): {resposta}")
        if resposta[:3] != '220':
            raise Exception("Erro ao iniciar STARTTLS.")
        context = ssl.create_default_context()
        return context.wrap_socket(clientSocket, server_hostname='smtp.gmail.com')
    except Exception as e:
        raise Exception(f"Erro ao iniciar TLS: {e}")

def autenticar(clientSocket, remetente, senha):
    try:
        # Enviar AUTH LOGIN
        clientSocket.send('AUTH LOGIN\r\n'.encode())
        resposta = clientSocket.recv(1024).decode()
        print(f"Resposta do servidor (AUTH LOGIN): {resposta}")
        if resposta[:3] != '334':
            raise Exception("Erro no comando AUTH LOGIN.")

        # Enviar nome de usuário
        clientSocket.send(base64.b64encode(remetente.encode()) + b'\r\n')
        resposta = clientSocket.recv(1024).decode()
        print(f"Resposta do servidor (Usuário): {resposta}")
        if resposta[:3] != '334':
            raise Exception("Erro ao enviar nome de usuário.")

        # Enviar senha
        clientSocket.send(base64.b64encode(senha.encode()) + b'\r\n')
        resposta = clientSocket.recv(1024).decode()
        print(f"Resposta do servidor (Senha): {resposta}")
        if resposta[:3] != '235':
            raise Exception("Erro ao autenticar usuário.")
    except Exception as e:
        raise Exception(f"Erro ao autenticar: {e}")

def enviar_email(clientSocket, remetente, destinatario, msg):
    try:
        # MAIL FROM
        clientSocket.send(f'MAIL FROM:<{remetente}>\r\n'.encode())
        resposta = clientSocket.recv(1024).decode()
        print(f"Resposta do servidor (MAIL FROM): {resposta}")
        if resposta[:3] != '250':
            raise Exception("Erro no comando MAIL FROM.")

        # RCPT TO
        clientSocket.send(f'RCPT TO:<{destinatario}>\r\n'.encode())
        resposta = clientSocket.recv(1024).decode()
        print(f"Resposta do servidor (RCPT TO): {resposta}")
        if resposta[:3] != '250':
            raise Exception("Erro no comando RCPT TO.")

        # DATA
        clientSocket.send('DATA\r\n'.encode())
        resposta = clientSocket.recv(1024).decode()
        print(f"Resposta do servidor (DATA): {resposta}")
        if resposta[:3] != '354':
            raise Exception("Erro no comando DATA.")

        # Enviar mensagem
        clientSocket.send(msg.encode())
        clientSocket.send('\r\n.\r\n'.encode())
        resposta = clientSocket.recv(1024).decode()
        print(f"Resposta do servidor (Envio da mensagem): {resposta}")
        if resposta[:3] != '250':
            raise Exception("Erro ao enviar a mensagem.")
    except Exception as e:
        raise Exception(f"Erro ao enviar e-mail: {e}")

def construir_mensagem(remetente, destinatario, assunto, mensagem, arquivo_anexo):
    # Criar mensagem no formato MIME
    msgMIME = MIMEMultipart()
    msgMIME['From'] = remetente
    msgMIME['To'] = destinatario
    msgMIME['Subject'] = assunto

    # Adicionar o corpo do e-mail
    msgMIME.attach(MIMEText(mensagem, 'plain'))

    # Adicionar anexo, se existir
    if arquivo_anexo:
        try:
            with open(arquivo_anexo, 'rb') as attachment:
                mime_base = MIMEBase('application', 'octet-stream')
                mime_base.set_payload(attachment.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header('Content-Disposition', f'attachment; filename={arquivo_anexo}')
            msgMIME.attach(mime_base)
        except FileNotFoundError:
            print(f"Arquivo {arquivo_anexo} não encontrado. Continuando sem anexo.")

    return msgMIME.as_string()

def main():
    remetente = "exemploremetente@gmail.com"
    senha = "Senha_de_aplicativo"  # Senha de aplicativo gerada
    destinatario = "exemplodestinatario@gmail.com"
    assunto = "Assunto desejado"
    mensagem = "Mensagem desejada"
    arquivo_anexo = r"caminho\do\anexo" # Ficará vazio se não houver anexo

    msg = construir_mensagem(remetente, destinatario, assunto, mensagem, arquivo_anexo)

    try:
        clientSocket = criar_socket()
        clientSocket.send('HELO Alice\r\n'.encode())
        clientSocket.recv(1024)
        clientSocket = iniciar_tls(clientSocket)
        autenticar(clientSocket, remetente, senha)
        enviar_email(clientSocket, remetente, destinatario, msg)
        clientSocket.send('QUIT\r\n'.encode())
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        clientSocket.close()

if __name__ == "__main__":
    main()