import cv2
import os
import config
from ultralytics import YOLO

camera = None  # Глобальная переменная для хранения объекта камеры

def capture_image(camera):
    """
    Захватывает изображение с камеры, сохраняет его в папку 'images/' с постоянным именем,
    а затем автоматически обрабатывает его через YOLO.
    """
    if camera is None or not camera.isOpened():
        print("Error: camera is not initialized or already closed.")
        return None
    
    image_filename = os.path.join('images', 'current_frame.jpg')
    
    # Захват изображения
    ret, frame = camera.read()
    if not ret:
        print("Error: failed to capture image.")
        return None
    
    # Сохранение изображения с постоянным именем
    cv2.imwrite(image_filename, frame)
    print(f"Изображение сохранено как {image_filename}")
    
    # Автоматически вызываем обработку изображения через YOLO после его сохранения
    return process_image(image_filename, frame, camera)

def process_image(image_filename, frame, camera):
    """
    Обрабатывает изображение с помощью модели YOLO и возвращает координаты нужного объекта.
    Далее вызывается функция регулирования.
    """
    model = YOLO('yolov11n_trained.pt')  # Загружаем обученную модель

    # Выполняем детекцию на изображении
    results = model(image_filename)

    # Переменные для хранения координат центра нужного объекта
    target_center = None

    # Перебираем все объекты, которые нашла YOLO
    for result in results:
        for box in result.boxes:
            # Получаем класс объекта
            class_id = int(box.cls)
            class_name = config.CLASSES[class_id]

            # Получаем координаты рамки (x1, y1, x2, y2)
            coords = box.xyxy[0].tolist()
            x1, y1, x2, y2 = map(int, coords)

            # Если это нужный объект, вычисляем и возвращаем его центр
            if class_name == config.selected_class:
                x_center = (x1 + x2) // 2  # Центр по X
                y_center = (y1 + y2) // 2  # Центр по Y
                target_center = (x_center, y_center)

    # Вызываем функцию для регулирования на основе смещения
    regulate_position(target_center, camera)

    return target_center

def regulate_position(target_center, camera):
    """
    Регулирование позиции объекта на основе смещения относительно центра окружности.
    """
    if config.selected_class is None:
        print("Error: no class selected.")
        return

    # Получаем параметры окружности для выбранного класса
    circle_params = config.CIRCLE_PARAMS.get(config.selected_class)
    if not circle_params:
        print(f"Error: No circle parameters found for class {config.selected_class}.")
        return

    circle_center_x = circle_params['center_x']
    circle_center_y = circle_params['center_y']
    radius = circle_params['radius']

    # Получаем координаты центра объекта
    if target_center is None:
        print("Error: object center not found.")
        return

    object_x, object_y = target_center

    # Вычисляем расстояние от центра объекта до центра окружности
    distance_x = object_x - circle_center_x
    distance_y = object_y - circle_center_y

    # Вычисляем расстояние от центра объекта до центра окружности по гипотенузе
    distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

    # Проверяем, находится ли объект в пределах окружности
    if distance <= radius:
        # Объект в пределах окружности, переходим к выполнению действия с объектом
        perform_action(target_center)
    else:
        # Объект за пределами окружности, отправляем параметры смещения в функцию регулирования
        apply_control(distance_x, distance_y, camera)

def apply_control(error_x, error_y, camera, Kpx=0.3125, Kpy=0.4167):
    """
    Функция для применения управляющего воздействия на основе смещения (ошибки) по осям X и Y.
    Ограничивает управляющие воздействия в пределах [-100, 100] и отбрасывает дробную часть.
    """
    # Вычисление управляющих воздействий для двигателей
    FP = error_x * Kpx
    TP = error_y * Kpy

    # Ограничиваем значения в диапазоне [-100, 100] и отбрасываем дробную часть
    left_motor = int(max(-100, min(100, FP + TP)))  # Ограничиваем значение и отбрасываем дробную часть
    right_motor = int(max(-100, min(100, FP - TP)))  # Ограничиваем значение и отбрасываем дробную часть

    # Печать для отладки (позже заменим на реальное управление двигателями)
    print(f"Motor.MotorMove(left_motor, right_motor): left_motor={left_motor}, right_motor={right_motor}")
    
    # Возвращаемся к следующему циклу захвата изображения
    capture_image(camera)


def perform_action(target_center):
    """
    Выполнение действия с объектом, когда он находится в целевой зоне.
    """
    x_center, y_center = target_center
    print(f"Объект находится в целевой зоне. Выполнение действия... Центр объекта: X={x_center}, Y={y_center}")
