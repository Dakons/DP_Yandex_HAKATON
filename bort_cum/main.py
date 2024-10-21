import config  # Подключаем файл с конфигурацией
import bort_cam  # Импортируем библиотеку bort_cam для дальнейшей работы
import cv2  # Для работы с камерой

camera = None  # Глобальная переменная для хранения объекта камеры

def initialize_camera():
    """
    Инициализируем бортовую камеру 
    """
    global camera
    if camera is None:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            message_command("Error: failed to open the camera.")
            camera = None
        else:
            message_command("Camera initialized.")

def message_command(message):
    """
    Функция для вывода сообщения в терминал.
    """
    print(message)

def process_command():
    """
    Функция для обработки команд, введённых в терминале.
    """
    while True:
        # Считывание команды с терминала и деление на части по пробелам
        parts = input("Enter the command: ").split()

        # Проверяем команду bort_cam и её параметры
        if len(parts) > 0 and parts[0] == "bort_cam":
            object_class = parts[1] if len(parts) > 1 else None

            # Проверяем, передан ли класс и есть ли он в списке допустимых классов
            if object_class in config.CLASSES:
                config.selected_class = object_class
                message_command(f"Class '{object_class}' selected.")
                bort_cam.capture_image(camera)  # Передаём объект камеры в функцию захвата изображения
            else:
                message_command(f"Error: Invalid or missing class '{object_class}'.")
        else:
            message_command(f"Unknown command: {parts[0]}")

def main():
    """
    Основная функция программы для обработки команд.
    """
    initialize_camera()  # Инициализируем камеру при старте программы
    process_command()  # Запуск обработки команд

# Запуск программы
if __name__ == "__main__":
    main()
