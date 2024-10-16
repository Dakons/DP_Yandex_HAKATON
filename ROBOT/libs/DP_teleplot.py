import socket
import time

ipadress = "192.168.233.217"

class TelemetrySender:
    def __init__(self, address=(ipadress, 47269)):
        self.teleplotAddr = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_telemetry(self, name, value):
        now = int(time.time() * 1000)  # Текущее время в миллисекундах
        msg = f"{name}:{now}:{value}"
        self.sock.sendto(msg.encode(), self.teleplotAddr)

    def close(self):
        self.sock.close()
