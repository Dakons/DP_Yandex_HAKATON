# command_handler.py
import bort_cam  # Импортируем наш модуль для работы с камерой и вывода сообщений
import cv2  # Для работы с камерой

def read_command(camera):
    """
    Функция для чтения команды из терминала и проверки условий.
    """
    # Чтение команды от пользователя
    command = input("Введите команду: ").strip()

    # Разделяем команду по пробелу, получаем первую часть (bort_cam) и вторую (класс объекта)
    parts = command.split()

    # Проверка, если есть хотя бы 2 части в команде
    if len(parts) > 0 and parts[0] == "bort_cam":
        if len(parts) > 1:
            # Вторая часть команды — это класс (например, ball, cube)
            object_class = parts[1]
            bort_cam.process_command(object_class, camera)  # Передаем камеру
        else:
            bort_cam.message_command("Ошибка: необходимо указать класс после 'bort_cam'.")
    else:
        bort_cam.message_command(f"Неизвестная команда: {command}")

def main():
    """
    Основной цикл программы для чтения команд.
    """
    # Инициализация камеры
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        bort_cam.message_command("Ошибка: не удалось открыть камеру.")
        return

    try:
        while True:
            read_command(camera)
    finally:
        camera.release()

if __name__ == "__main__":
    main()
