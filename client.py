import socket
import json

class Client:
    def __init__(self, host="127.0.0.1", port=9009, name="player"):
        self.host = host
        self.port = port
        self.name = name
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        print("[client] Connected to server")

        # Gửi lệnh join khi mới vào
        self.send_command({"type": "join", "name": self.name})

    def send_command(self, obj):
        msg = json.dumps(obj) + "\n"
        self.sock.sendall(msg.encode("utf-8"))

    def receive(self):
        data = self.sock.recv(2048).decode("utf-8")
        for line in data.strip().split("\n"):
            try:
                msg = json.loads(line)
                print("[server]", msg)
            except:
                print("[server raw]", line)

    def close(self):
        if self.sock:
            self.sock.close()
            print("[client] Disconnected")

if __name__ == "__main__":
    client = Client(name="player2")
    client.connect()
    client.send_command({"type": "input", "action": "move", "dir": "UP"})
    client.receive()
    client.close()