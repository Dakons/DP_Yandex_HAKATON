import socket
import time

class TelemetrySender:
    def __init__(self, address=("127.0.0.1", 47269)):
        self.teleplotAddr = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_telemetry(self, name, value):
        now = int(time.time() * 1000)  # Текущее время в миллисекундах
        msg = f"{name}:{now}:{value}"
        self.sock.sendto(msg.encode(), self.teleplotAddr)

    def close(self):
        self.sock.close()
