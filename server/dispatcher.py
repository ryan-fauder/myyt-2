import socket
import threading
import struct
from servidor import Servidor
class Dispatcher:
    def __init__(self, host, porta):
        self.host = host
        self.porta = porta
        self.servidor = Servidor()

    def start(self):
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_socket.bind((self.host, self.porta))
        servidor_socket.listen(5)

        print(f"O Dispatcher está ouvindo em {self.host}:{self.porta}")

        while True:
            cliente_socket, endereco_cliente = servidor_socket.accept()
            print(f"Conexão recebida de {endereco_cliente}")

            # Cria uma nova thread para lidar com a conexão
            thread = threading.Thread(target=self.listen, args=(cliente_socket,))
            thread.start()

    def listen(self, cliente_socket):
        # Lê os dados da mensagem do cliente
        dados = cliente_socket.recv(1024)
        
        # Desempacota os dados usando struct.unpack
        unpacked_data = struct.unpack('!I', dados[:4])
        tipo = unpacked_data[0]

        unpacked_data = struct.unpack(f'!{len(dados) - 9}s', dados[4:-5])
        dado = unpacked_data[0]

        unpacked_data = struct.unpack(f'!{len(dados) - 13}s', dados[-5:-1])
        tipo_dado = unpacked_data[0].decode('utf-8')

        tamanho_dado = struct.unpack('!I', dados[-1:])[0]

        # Cria uma instância da classe Mensagem
        request = Mensagem(tipo, dado, tipo_dado, tamanho_dado)

        # Chama o método handle do servidor para processar a requisição
        response = self.servidor.handle(request)

        # Envia a resposta de volta ao cliente
        cliente_socket.sendall(self.marshalMensagem(response))

        # Fecha o socket do cliente
        cliente_socket.close()

    def marshalMensagem(self, mensagem: Mensagem) -> bytes:
        # Empacotar os dados usando struct.pack
        mensagem_format = f'!I{len(mensagem.dado)}s{len(mensagem.tipo_dado)}sI'
        return struct.pack(mensagem_format, mensagem.tipo, mensagem.dado, mensagem.tipo_dado.encode('utf-8'), mensagem.tamanho_dado)

if __name__ == "__main__":
    # Exemplo de uso
    host_dispatcher = "localhost"
    porta_dispatcher = 8888

    dispatcher = Dispatcher(host_dispatcher, porta_dispatcher)
    dispatcher.start()
