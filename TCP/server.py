import socket
import threading
import pickle

class Protocolo:
    def __init__(self, msg=None, arquivo=None, arquivo_data=None):
        self.msg = msg
        self.arquivo = arquivo
        self.arquivo_data = arquivo_data

clients = []

def recebe_e_envia_mensagens_client(client_socket, endereco):
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break

            protocolo = pickle.loads(data)
            comando = protocolo.msg.split()[0]
            print(f"Comando recebido de {endereco}: {comando}")

            if protocolo.msg.startswith('/msg'):
                mensagem = protocolo.msg.split(' ', 1)[1]
                print(f"Mensagem de {endereco}: {mensagem}")
                for client in clients:
                    if client != client_socket:
                        client.send(pickle.dumps(protocolo))

            elif protocolo.msg.startswith('/enviararquivo'):
                print(f"Nome do arquivo recebido de {endereco}: {protocolo.arquivo}")
                print(f"Texto do arquivo recebido de {endereco}: {protocolo.arquivo_data}")
                for client in clients:
                    if client != client_socket:
                        client.send(pickle.dumps(protocolo))

            elif protocolo.msg == "/sair":
                print(f"Cliente {endereco} desconectado.")
                client_socket.send(pickle.dumps(protocolo))
                clients.remove(client_socket)
                client_socket.close()
                break

            else:
                print(f"Erro: comando fora do protocolo de {endereco}")
                break

        except:
            print(f"Erro ao receber mensagem de {endereco}")
            clients.remove(client_socket)
            client_socket.close()
            break

def inicia_server():
    host = '127.0.0.1'
    port = 65000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print("Servidor TCP iniciado")

    while True:
        client_socket, endereco = server.accept()
        clients.append(client_socket)
        print(f"Novo cliente conectado: {endereco}")

        # Inicia uma nova thread para o cliente conectado
        threading.Thread(target=recebe_e_envia_mensagens_client, args=(client_socket, endereco)).start()

inicia_server()
