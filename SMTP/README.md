# Envio de E-mail com Python usando Sockets

Este repositório contém um script Python que demonstra como enviar um e-mail utilizando sockets diretamente através do protocolo SMTP com a autenticação e segurança TLS.

## Descrição

O script realiza a conexão com o servidor SMTP do Gmail, autentica um usuário e envia um e-mail, que pode incluir um anexo. Ele utiliza bibliotecas padrão do Python para lidar com sockets, MIME para formatação de e-mails, e SSL para a segurança da conexão.

## Funcionalidades

### Criação de Socket
- **Função**: `criar_socket`
- **Descrição**: Esta função cria um socket TCP/IP e conecta-se ao servidor SMTP do Gmail. Ela verifica a resposta inicial do servidor para confirmar que a conexão foi estabelecida corretamente.

### Inicialização do TLS
- **Função**: `iniciar_tls`
- **Descrição**: Após a conexão inicial, esta função envia o comando `STARTTLS` para iniciar uma subcamada de segurança usando TLS. Isso garante que a comunicação subsequente seja criptografada.

### Autenticação
- **Função**: `autenticar`
- **Descrição**: Esta função realiza a autenticação do usuário utilizando o comando `AUTH LOGIN`. As credenciais (nome do usuário e senha) são enviadas em base64 conforme requerido pelo protocolo SMTP.

### Envio de E-mail
- **Função**: `enviar_email`
- **Descrição**: Com o usuário já autenticado, essa função procede com o envio do e-mail. Ela configura o remetente e o destinatário com os comandos `MAIL FROM` e `RCPT TO`, inicia a composição da mensagem com o comando `DATA`, e finaliza o envio da mensagem.

### Construção da Mensagem MIME
- **Função**: `construir_mensagem`
- **Descrição**: Esta função cria um objeto `MIMEMultipart` para compor o e-mail. Ela permite adicionar tanto texto quanto anexos ao e-mail, utilizando o formato MIME para garantir que os elementos sejam formatados e codificados corretamente.

## Pré-requisitos

- Python 3.x
- Acesso à internet
- Credenciais válidas do Gmail (nome de usuário e senha de aplicativo)

## Como Usar

1. Clone o repositório para sua máquina local.
2. Modifique o script com suas credenciais de e-mail (remetente e senha) e informações do destinatário.
3. Execute o script em um ambiente que permita execução de scripts Python com privilégios de rede:

```bash
python smtp.py
