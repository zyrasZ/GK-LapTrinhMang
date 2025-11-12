# client_day1.py
import socket

class Client:
    def __init__(self, host="127.0.0.1", port=9009):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print("[client] Connected to server")

    def send(self, data: str):
        if self.sock:
            self.sock.sendall(data.encode("utf-8"))

    def receive(self):
            data = self.sock.recv(1024).decode("utf-8")
            print("[server]", data)

    def close(self):
        if self.sock:
            self.sock.close()
            print("[client] Disconnected")


if __name__ == "__main__":
    client = Client()
    client.connect()
    client.send("Hello server!")
    client.receive()
    client.close()
