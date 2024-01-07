import socket
import json
from ..communikate.communication import Communication
from urllib.parse import urlparse
from ..message import Request, Response
class Fetch:
    def split_endpoint(endpoint: str):
        url_parts = urlparse(endpoint)
        host = url_parts.hostname
        port = url_parts.port
        path = url_parts.path
        if(host == None or port == None): 
            raise Exception('Endpoint inválido')
        return host, int(port), path
    
    def post(endpoint: str, data: dict):
        host, port, path = Fetch.split_endpoint(endpoint) 

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        request = Request(method="post", path=path, data=data)
        Communication.send(client, request.__dict__())
        response: Response = Response.__from__(Communication.receive(client))
        client.close()
        return response.data
    
    def put(endpoint: str, data: dict):
        host, port, path = Fetch.split_endpoint(endpoint) 
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        request = Request(method="put", path=path, data=data)
        Communication.send(client, request.__dict__())
        response: Response = Response.__from__(Communication.receive(client))
        client.close()
        return response.data
    
    def get(endpoint: str):
        host, port, path = Fetch.split_endpoint(endpoint) 
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        request = Request(method="get", path=path)
        Communication.send(client, request.__dict__())
        response: Response = Response.__from__(Communication.receive(client))
        client.close()
        return response.data
    
    def delete(endpoint: str, data: dict):
        host, port, path = Fetch.split_endpoint(endpoint) 
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        request = Request(method="delete", path=path, data=data)
        Communication.send(client, request.__dict__())
        response: Response = Response.__from__(Communication.receive(client))
        client.close()
        return response.data

if __name__ == '__main__':
    print(Fetch.split_endpoint('http://localhost:3000'))