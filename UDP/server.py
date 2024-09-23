import socket
import pickle

class Protocolo:
    def __init__(self, msg=None, arquivo=None, arquivo_data=None):
        self.msg = msg
        self.arquivo = arquivo
        self.arquivo_data = arquivo_data
        
# Dicionário para armazenar endereços e nomes de usuários
usuarios = {}

def inicia_server():
    host = '127.0.0.1'
    port = 65000

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((host, port))

    print("Servidor UDP iniciado")

    while True:
        data, endereco = server.recvfrom(4096)
        
        protocolo = pickle.loads(data)
        comando = protocolo.msg.split()[0]  # Extrai o comando
        
        print("Comando recebido:", comando)
        
        if comando == '/msg':
            mensagem = protocolo.msg.split(' ', 1)[1]
            # Se o endereço não estiver registrado, mostra o IP e a porta do cliente
            nome_usuario = usuarios.get(endereco, f"{endereco[0]}:{endereco[1]}")  
            print(f"Mensagem de {nome_usuario}: {mensagem}")
            for endereco_lista in usuarios:
                if endereco_lista != endereco:
                    server.sendto(pickle.dumps(protocolo), endereco_lista)

        elif comando == '/enviararquivo':
            print("Nome do arquivo recebido:", protocolo.arquivo)
            print("Texto do arquivo recebido:", protocolo.arquivo_data)
            for endereco_lista in usuarios:
                if endereco_lista != endereco:
                    server.sendto(pickle.dumps(protocolo), endereco_lista)
                    
        elif comando == '/reg':
            # Registra o cliente com seu nome
            nome_usuario = protocolo.msg.split(' ', 1)[1]  # Obtém o nome do usuário
            usuarios[endereco] = nome_usuario
            print(f"Novo cliente registrado: {nome_usuario} ({endereco[0]}:{endereco[1]})")
                    
        elif comando == '/sair':
            nome_usuario = usuarios.pop(endereco, f"{endereco[0]}:{endereco[1]}")  # Remove o usuário pelo endereço
            server.sendto(pickle.dumps(protocolo), endereco)
            print(f"Cliente {nome_usuario} ({endereco[0]}:{endereco[1]}) desconectado.")
        
        else:
            print("Erro, comando fora do protocolo")

inicia_server()
