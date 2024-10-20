import sys
import os

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

import socket
import asyncio
import rasp_commands as commands




class TCPServer:
    """Класс для TCP-сервера на Raspberry Pi"""

    async def handle_connection(self, conn, addr):
        """
        Асинхронная обработка подключения и ожидание команд от клиента (ПК).
        """
        print(f"Подключен клиент с адресом: {addr}")
        loop = asyncio.get_running_loop()
        while True:
            try:
                print("Ожидаем данные от клиента...")
                data = await loop.sock_recv(conn, 1024)  # Асинхронное ожидание данных от клиента
                if not data:
                    print("Клиент закрыл соединение.")
                    break

                command = data.decode().strip()  # Декодируем и убираем пробелы/переводы строк
                await commands.do_commands(command, conn)

                # Асинхронно передаём команду и соединение в библиотеку команд

            except ConnectionResetError:
                print(f"Соединение с клиентом {addr} потеряно.")
                break

        print(f"Отключение клиента: {addr}")
        conn.close()
        print("Соединение закрыто.")

    async def start_server(self):
        """
        Запуск TCP-сервера для приема подключений.
        """
        loop = asyncio.get_running_loop()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('0.0.0.0', 5000))  # Привязываем сервер к порту 5000
            server_socket.listen()
            server_socket.setblocking(False)  # Переключаем сокет в неблокирующий режим
            print("Сервер запущен на порту 5000, ожидаем подключения...")

            while True:
                conn, addr = await loop.sock_accept(server_socket)  # Асинхронное ожидание подключений
                asyncio.create_task(self.handle_connection(conn, addr))  # Обрабатываем подключение асинхронно

if __name__ == "__main__":
    asyncio.run(TCPServer().start_server())
