import socket
import threading

# Настройки для UDP и TCP
UDP_IP = "0.0.0.0"   # Слушать на всех интерфейсах
UDP_PORT = 5005
TCP_IP = "0.0.0.0"   # Слушать на всех интерфейсах
TCP_PORT = 5006

# Функция для обработки UDP-пакетов (команды)
def udp_server():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Создание UDP-сокета
    udp_sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = udp_sock.recvfrom(1024)  # Получение данных
        print(f"Получена команда по UDP: {data.decode()} от {addr}")

# Функция для обработки TCP-пакетов (например, видео)
def tcp_server():
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создание TCP-сокета
    tcp_sock.bind((TCP_IP, TCP_PORT))
    tcp_sock.listen(1)

    conn, addr = tcp_sock.accept()  # Ожидание подключения клиента
    print(f"TCP подключение с {addr}")

    while True:
        data = conn.recv(1024)  # Получение данных
        if not data:
            break
        print(f"Получены данные по TCP (видео): {len(data)} байт")

    conn.close()

# Создаем и запускаем два потока для UDP и TCP серверов
udp_thread = threading.Thread(target=udp_server)
tcp_thread = threading.Thread(target=tcp_server)

udp_thread.start()
tcp_thread.start()

udp_thread.join()
tcp_thread.join()