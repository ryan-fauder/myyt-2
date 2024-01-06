import struct
from message.interface import Mensagem
class ProtocolSocket:
    @staticmethod
    def criaMensagem(tipo, dado: bytes, tipo_dado: str, tamanho_dado: int) -> Mensagem:
        return Mensagem(tipo, dado, tipo_dado, tamanho_dado)

    @staticmethod
    def marshalMensagem(mensagem: Mensagem) -> bytes:
        # Empacotar os dados usando struct.pack
        mensagem_format = f'!I{len(mensagem.dado)}s{len(mensagem.tipo_dado)}sI'
        return struct.pack(mensagem_format, mensagem.tipo, mensagem.dado, mensagem.tipo_dado.encode('utf-8'), mensagem.tamanho_dado)

    @staticmethod
    def unmarshalMensagem(dados: bytes) -> Mensagem:
        # Desempacotar os dados usando struct.unpack
        unpacked_data = struct.unpack('!I', dados[:4])
        tipo = unpacked_data[0]

        unpacked_data = struct.unpack(f'!{len(dados) - 9}s', dados[4:-5])
        dado = unpacked_data[0]

        unpacked_data = struct.unpack(f'!{len(dados) - 13}s', dados[-5:-1])
        tipo_dado = unpacked_data[0].decode('utf-8')

        tamanho_dado = struct.unpack('!I', dados[-1:])[0]

        return Mensagem(tipo, dado, tipo_dado, tamanho_dado)