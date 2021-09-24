import socket
import pickle

class Network:
    def __init__(self, ip) -> None:
        self.host = ip
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 3000
        self.addr = (self.host, self.port)
        self.symbol = self.connect()

    def getSymbol(self):
        return int(self.symbol)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(1024).decode()
        except:
            raise ValueError('Unable to connect to the server. Is the server even on ?')

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(1024))
        except socket.error as e:
            print(e)

    def recvGame(self):
        try:
            self.client.send(str.encode("GET_GAME"))
            return pickle.loads(self.client.recv(1024))

        except socket.timeout as e:
            return None
        except:
            print("Unable to receive data :c")
            return None
