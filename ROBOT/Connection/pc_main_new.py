import socket

class TCPClient:
    """Класс для TCP-клиента на ПК"""
    def __init__(self, ip_adress):
        self.ip_adress = ip_adress

    def connect(self):
        """Подключение к серверу на Raspberry Pi"""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.ip_adress, 5000))  # Подключаемся к серверу на Pi
        print(f"Подключено к Raspberry Pi на {self.ip_adress}")
        return client_socket
    
    def send_command(self, command):
        client_socket = self.connect()
        client_socket.sendall(command.encode())  # Отправляем команду серверу
        print(f"Команда '{command}' отправлена на сервер.")
        
        # Ожидание ответа от сервера
        print("Ожидаем ответ от сервера...")
        data = client_socket.recv(1024)  # Синхронное ожидание ответа
        if not data:
            print("Сервер закрыл соединение.")
        else:
            # Обработка полученной команды
            response = data.decode().strip()  
            print(f"Ответ от сервера: {response}")


raspberry = TCPClient("192.168.185.206")

raspberry.send_command("Turn 360")


