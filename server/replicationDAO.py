
class ReplicationDAO:
    def __init__(self):
        # Simulando um banco de dados que armazena endereços e portas
        self.hosts = [
            {"endereco": "192.168.1.1", "porta": 5000},
            {"endereco": "192.168.1.2", "porta": 5000},
            # Adicione mais hosts conforme necessário
        ]

    def get_hosts(self):
        # Retorna a lista de hosts
        return self.hosts
