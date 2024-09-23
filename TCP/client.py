import socket
import threading
import pickle

class Protocolo:
    def __init__(self, msg=None, arquivo=None, arquivo_data=None):
        self.msg = msg
        self.arquivo = arquivo
        self.arquivo_data = arquivo_data
    
def inicia_client():
    server_ip = '127.0.0.1'
    server_port = 65000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))
    print("Cliente conectado ao servidor.")

    def receber_mensagens():
        while True:
            data = client.recv(4096)
            protocolo = pickle.loads(data)
            
            if protocolo.msg.startswith('/msg'):
                mensagem = protocolo.msg.split(' ', 1)[1]
                print("Mensagem recebida:", mensagem)
                
            elif protocolo.msg.startswith('/enviararquivo'):
                nome_arquivo = protocolo.msg.split()[1]
                print(protocolo.arquivo_data)
                with open(nome_arquivo, 'wb') as file:
                    file.write(protocolo.arquivo_data)
                print(f"Arquivo '{nome_arquivo}' recebido e salvo.")
                
            elif protocolo.msg == "/sair":
                print("Desconectado do servidor.")
                client.close()
                break
            
    threading.Thread(target=receber_mensagens).start()
    
    print("Bem vindo Cliente!")
    print("Os comandos disponiveis são:")
    print("/msg {sua mensagem}") #envia mesagem para o servidor
    print("/enviararquivo {nome do arquivo} {path do arquivo}") #envia arquivo de texto para o servidor
    print("/sair") #fecha conexao com servidor
    print()

    while True:
        msg = input("")
        protocolo = Protocolo(msg=msg)
        
        if msg == '/sair':
            client.send(pickle.dumps(protocolo))
            break
        
        elif msg.startswith('/enviararquivo'):
            protocolo.arquivo = msg.split()[1]
            arquivo_path = msg.split()[2]
            print(arquivo_path)
            with open(arquivo_path, 'rb') as file:
                arquivo_data = file.read()
                protocolo.arquivo_data = arquivo_data
                client.send(pickle.dumps(protocolo))
        
        elif msg.startswith('/msg'):
            client.send(pickle.dumps(protocolo))
            
        else:
            print("Erro, comando fora do protocolo")

inicia_client()
