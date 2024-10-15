import socket
import threading
import time

# Укажите IP-адрес и порт
UDP_IP = "192.168.1.100"  # IP-адрес ПК
UDP_PORT = 5005
LOCAL_UDP_PORT = 5006  # Порт для приема

# Создаем сокет для UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', LOCAL_UDP_PORT))

def receive_data():
    while True:
        data, addr = sock.recvfrom(1024)  # Буфер размером 1024 байта
        print(f"Получено от {addr}: {data.decode()}")

def send_data():
    while True:
        # Подготовка данных для отправки
        message = "Данные от Raspberry Pi"
        sock.sendto(message.encode(), (UDP_IP, UDP_PORT))
        print(f"Отправлено: {message}")
        time.sleep(2)  # Отправляем данные каждые 2 секунды

# Запускаем потоки для отправки и получения данных
threading.Thread(target=receive_data, daemon=True).start()
send_data()
