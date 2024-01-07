import socket
from .protocol import Protocol

class  ReceivedErrorMessageException(Exception):
    def __init__(self, message):
        super().__init__(message)
    
class Communication:
    def __init__(self, socket: socket.socket) -> None:
        self.socket = socket

    def send(connection: socket.socket, data: any):
        message = Protocol.marshalMessage(data)
        connection.sendall(message)

    def send_error(connection: socket.socket, error: str):
        message = Protocol.marshalMessage(error, status="Error")
        connection.sendall(message)


    def receive(connection: socket.socket) -> any:
        try:
            message: bytes = connection.recv(1024)
            message_size = Protocol.get_size(message)
            for _ in range(1024, message_size, 1024):
                data: bytes = connection.recv(1024)
                if not data:
                    break
                message += data
            header, body = Protocol.unmarshalMessage(message)
            
            if (header['status'] == 'Error'):
                raise ReceivedErrorMessageException(body)
            
            return body
        except ReceivedErrorMessageException as error:
            raise Exception(error)
        except Exception:
            error = 'Connection error: Server cannot receive message'
            raise Exception(error)