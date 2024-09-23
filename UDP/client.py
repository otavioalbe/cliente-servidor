import socket
import threading
import pickle

class Protocolo:
    def __init__(self, msg=None, arquivo=None, arquivo_data=None, nome_usuario=None):
        self.msg = msg
        self.arquivo = arquivo
        self.arquivo_data = arquivo_data
        self.nome_usuario = nome_usuario  # Adicionando o nome do usuário no protocolo

def inicia_client():
    server_ip = '127.0.0.1'
    server_port = 65000

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(('127.0.0.1', 0))

    def receber_mensagens():
        while True:
            data, serverAddress = client.recvfrom(4096)
            protocolo = pickle.loads(data)

            # Verifica o tipo de mensagem recebida
            if protocolo.msg.startswith('/msg'):
                nome_remetente = protocolo.nome_usuario if protocolo.nome_usuario else "Desconhecido"
                mensagem = protocolo.msg.split(' ', 1)[1]
                print(f"Mensagem de {nome_remetente}: {mensagem}")

            elif protocolo.msg.startswith('/enviararquivo'):
                nome_arquivo = protocolo.msg.split()[1]
                print(protocolo.arquivo_data)
                with open(nome_arquivo, 'wb') as file:
                    file.write(protocolo.arquivo_data)
                print(f"Arquivo '{nome_arquivo}' recebido e salvo.")

            elif protocolo.msg == "/sair":
                print("Desconectado do servidor.")
                break

    # Inicia uma thread para receber mensagens do servidor
    threading.Thread(target=receber_mensagens).start()

    print("Bem-vindo Cliente!")
    print("Os comandos disponíveis são:")
    print("/reg {seu nome}")  # registra o cliente no servidor
    print("/msg {sua mensagem}")  # envia mensagem para o servidor
    print("/enviararquivo {nome do arquivo} {path do arquivo}")  # envia arquivo de texto para o servidor
    print("/sair")  # fecha conexão com servidor
    print()

    nome_usuario = None

    while True:
        msg = input("")
        protocolo = Protocolo(msg=msg)

        if msg.startswith('/reg'):
            # Extrai o nome do usuário no registro
            nome_usuario = msg.split(' ', 1)[1]
            protocolo.nome_usuario = nome_usuario
            client.sendto(pickle.dumps(protocolo), (server_ip, server_port))

        elif msg.startswith('/msg'):
            protocolo.nome_usuario = nome_usuario  # Inclui o nome do usuário na mensagem
            client.sendto(pickle.dumps(protocolo), (server_ip, server_port))

        elif msg.startswith('/enviararquivo'):
            protocolo.nome_usuario = nome_usuario  # Inclui o nome do usuário
            protocolo.arquivo = msg.split()[1]
            arquivo_path = msg.split()[2]
            print(arquivo_path)
            with open(arquivo_path, 'rb') as file:
                arquivo_data = file.read()
                protocolo.arquivo_data = arquivo_data
            client.sendto(pickle.dumps(protocolo), (server_ip, server_port))

        elif msg == '/sair':
            client.sendto(pickle.dumps(protocolo), (server_ip, server_port))
            break

        else:
            print("Erro, comando fora do protocolo")

inicia_client()
