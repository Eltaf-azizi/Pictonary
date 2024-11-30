import socket
import json
import time as t

class Network:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5556
        self.addr = (self.server, self.port)
        self.name = name
        self.connected = False
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.sendall(self.name.encode())
            response = self.client.recv(2048).decode()
            self.connected = True
            return json.loads(response)
        except Exception as e:
            self.disconnect(e)

    def send(self, data):
        try:
            if not self.connected:
                raise socket.error("Not connected to the server.")
            
            self.client.send(json.dumps(data).encode())
            
            d = ""
            while True:
                last = self.client.recv(1024).decode()
                d += last
                try:
                    # Assuming data ends with a period (".")
                    if d.count(".") == 1:
                        break
                except:
                    pass

            if d.endswith("."):
                d = d[:-1]

            return json.loads(d)
        except Exception as e:
            self.disconnect(e)

    def disconnect(self, msg):
        print("[EXCEPTION] Disconnected from server:", msg)
        self.connected = False
        self.client.close()

# Example usage
n = Network("Tech With Tim")

print("send 1")
response = n.send({3: []})
print(response)

t.sleep(0.1)

print("send 2")
response = n.send({5: []})
print(response)
