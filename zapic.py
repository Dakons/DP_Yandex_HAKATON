import cv2
import time

def start_video_stream(camera=None):
    """
    Функция для запуска видеопотока с камеры. По нажатию клавиши 'r' начинается запись видео.
    """
    if camera is None:
        # Инициализация камеры (если не передана)
        camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open the camera.")
        return

    # Переменная для отслеживания состояния записи
    recording = False
    video_writer = None

    while True:
        # Захват изображения с камеры
        ret, frame = camera.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Отображение кадра
        cv2.imshow("Video Stream", frame)

        # Ожидание нажатия клавиши
        key = cv2.waitKey(1) & 0xFF

        # Нажатие 'r' запускает запись видео
        if key == ord('r') and not recording:
            recording = True
            # Создаем имя файла на основе текущего времени
            filename = time.strftime("%Y-%m-%d_%H-%M-%S") + ".avi"
            # Инициализация VideoWriter для записи видео
            video_writer = cv2.VideoWriter(
                filename, 
                cv2.VideoWriter_fourcc(*"XVID"),  # Используем кодек XVID для записи
                20.0,  # FPS
                (int(camera.get(3)), int(camera.get(4)))  # Размер кадра
            )
            print(f"Recording started: {filename}")

        # Нажатие 's' останавливает запись видео
        elif key == ord('s') and recording:
            recording = False
            video_writer.release()  # Останавливаем запись
            print(f"Recording stopped.")
        
        # Если запись активна, записываем кадры в файл
        if recording:
            video_writer.write(frame)

        # Нажатие 'q' для выхода
        if key == ord('q'):
            break

    # Освобождаем ресурсы
    if recording:
        video_writer.release()
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_video_stream()
