# import socket
# import asyncio
#  # Подключаем библиотеку для обработки команд


# class TCPClient:
#     """Класс для TCP-клиента на ПК"""

#     def connect(self):
#         """Подключение к серверу на Raspberry Pi"""
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client_socket.connect(('192.168.2.110', 5000))  # Подключаемся к серверу на Pi
#         print("Подключено к Raspberry Pi на 192.168.2.65:5000")
#         return client_socket

#     async def handle_client(self, client_socket):
#         """
#         Асинхронная функция для отправки команд и получения ответов параллельно.
#         """
#         loop = asyncio.get_running_loop()
#         while True:
#             # Отправляем команду на сервер
#             try:
#                 command = input("Введите команду для отправки на Raspberry Pi: ")
#                 if command.lower() == "exit":
#                     print("Завершаем работу...")
#                     break
#                 client_socket.sendall(command.encode())  # Отправляем команду серверу
#                 print(f"Команда '{command}' отправлена на сервер.")

#             except Exception as e:
#                 print(f"Ошибка при отправке или получении данных: {e}")
#                 break

#     async def start_client(self):
#         """Запуск клиента и обработка команд"""
#         client_socket = self.connect()
#         await self.handle_client(client_socket)  # Запускаем асинхронный цикл отправки и приёма

# if __name__ == "__main__":
#     client = TCPClient()
#     asyncio.run(client.start_client())

import socket
import asyncio

class TCPClient:
    """Класс для TCP-клиента на ПК"""

    def connect(self):
        """Подключение к серверу на Raspberry Pi"""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('192.168.43.206', 5000))  # Подключаемся к серверу на Pi
        print("Подключено к Raspberry Pi на 192.168.2.65:5000")
        return client_socket

    async def handle_client(self, client_socket):
        """
        Асинхронная функция для отправки команд и получения ответов параллельно.
        """
        loop = asyncio.get_running_loop()
        while True:
            # Отправляем команду на сервер
            try:
                command = input("Введите команду для отправки на Raspberry Pi: ")
                if command.lower() == "exit":
                    print("Завершаем работу...")
                    break

                client_socket.sendall(command.encode())  # Отправляем команду серверу
                print(f"Команда '{command}' отправлена на сервер.")

                # Ожидание ответа от сервера
                print("Ожидаем ответ от сервера...")
                data = await loop.sock_recv(client_socket, 1024)  # Асинхронное ожидание ответа
                if not data:
                    print("Сервер закрыл соединение.")
                    break

                # Обработка полученной команды
                response = data.decode().strip()  
                print(f"Ответ от сервера: {response}")


            except Exception as e:
                print(f"Ошибка при отправке или получении данных: {e}")
                break

    async def start_client(self):
        """Запуск клиента и обработка команд"""
        client_socket = self.connect()
        await self.handle_client(client_socket)  # Запускаем асинхронный цикл отправки и приёма

if __name__ == "__main__":
    client = TCPClient()
    asyncio.run(client.start_client())
