import socket
import threading
import DP_do_command as DO

UDP_IP_RASP = "192.168.233.206"  # IP-адрес Raspberry Pi
UDP_PORT_RASP = 5005
TCP_IP_RASP = "192.168.233.206"  # IP-адрес Raspberry Pi
TCP_PORT_RASP = 5006

UDP_IP_PC = "0.0.0.0"   # Слушать на всех интерфейсах
UDP_PORT_PC = 5005
TCP_IP_PC = "0.0.0.0"   # Слушать на всех интерфейсах
TCP_PORT_PC = 5006

# Функция для отправки данных через UDP
def send_udp_command_RASP(name, values):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    command = " ".join([name] + list(map(str, values)))
    udp_sock.sendto(command.encode(), (UDP_IP_PC, UDP_PORT_PC))
    udp_sock.close()

def send_tcp_command_RASP(name, values):
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind((TCP_IP_PC, TCP_PORT_PC))
    tcp_sock.listen(1)
    command = " ".join([name] + list(map(str, values)))
    tcp_sock.sendall(command.encode(), (TCP_IP_PC, TCP_PORT_PC))

def send_udp_command_PC(name, values):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    command = " ".join([name] + list(map(str, values)))
    udp_sock.sendto(command.encode(), (UDP_IP_RASP, UDP_PORT_RASP))

def send_tcp_command_PC(name, values):
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создание TCP-сокета
    tcp_sock.connect((TCP_IP_RASP, TCP_PORT_RASP))  # Подключение к серверу
    command = " ".join([name] + list(map(str, values)))
    tcp_sock.sendall(command.encode(), (TCP_IP_RASP, TCP_PORT_RASP))

def get_tcp_command_PC():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind((TCP_IP_RASP, TCP_PORT_RASP))
    tcp_sock.listen(1)
    conn, addr = tcp_sock.accept()  # Ожидание подключения клиента

    command = conn.recv(1024)  # Получение данных
    name, *values = command.split(" ")
    DO.do_command_PC(name, values)
    conn.close()


def get_tcp_command_RASP():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создание TCP-сокета
    tcp_sock.bind((TCP_IP_PC, TCP_PORT_PC))
    tcp_sock.listen(1)
    conn, addr = tcp_sock.accept()  # Ожидание подключения клиента
    command = conn.recv(1024)  # Получение данных
    name, *values = command.split(" ")
    DO.do_command_Rasp(name, values)
    conn.close()

def get_udp_command_PC():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((UDP_IP_RASP, UDP_PORT_RASP))

    data, addr = udp_sock.recvfrom(1024)  # Получение данных
    name, *values = data.decode().split(" ")  # Получение данных
    DO.do_command_PC(name, values)

def get_udp_command_RASP():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Создание UDP-сокета
    udp_sock.bind((UDP_IP_PC, UDP_PORT_PC))
    data, addr = udp_sock.recvfrom(1024)  # Получение данных
    name, *values = data.decode().split(" ")  # Получение данных
    DO.do_command_Rasp(name, values)