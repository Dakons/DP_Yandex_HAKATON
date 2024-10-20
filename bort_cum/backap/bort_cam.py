import cv2
import config
from ultralytics import YOLO
import button_color  # Импортируем библиотеку для работы с цветами кнопок

def message_command(message):
    """
    Функция для вывода сообщения в консоль.
    """
    print(message)

def capture_frame(camera):
    """
    Функция для захвата и сохранения кадра с камеры.
    """
    ret, frame = camera.read()
    if not ret:
        message_command("Ошибка: не удалось захватить кадр.")
        return None
    
    # Оставляем изображение в формате BGR (по умолчанию для OpenCV)
    
    # Проверка и создание директории для сохранения кадра
    import os
    if not os.path.exists('saved_images'):
        os.makedirs('saved_images')

    # Сохраняем кадр в формате BGR в папку 'saved_images'
    cv2.imwrite('saved_images/captured_frame.jpg', frame)
    message_command("Кадр сохранен как 'saved_images/captured_frame.jpg'.")
    return frame

def process_yolo_detection(image_path):
    """
    Обработка изображения с помощью YOLO для детекции объектов.
    Возвращает координаты обнаруженных объектов.
    """
    model = YOLO('yolov11n_trained.pt')  # Используем твою модель

    # Выполняем предсказание на изображении
    results = model(image_path)

    # Обрабатываем результаты предсказания
    object_info = []
    for result in results:
        for box in result.boxes:
            # Получаем координаты рамки (x1, y1, x2, y2)
            coords = box.xyxy[0].tolist()

            # Рассчитываем центр рамки
            x_center = (coords[0] + coords[2]) / 2  # (x1 + x2) / 2
            y_center = (coords[1] + coords[3]) / 2  # (y1 + y2) / 2

            class_id = int(box.cls)  # Класс объекта
            confidence = float(box.conf)  # Уверенность модели в предсказании

            # Добавляем информацию об объекте в список
            object_info.append({
                'class_id': class_id,
                'coords': coords,  # Координаты рамки
                'center': (x_center, y_center),  # Центр объекта
                'confidence': confidence
            })
    
    return object_info

def get_rect_params_for_class(object_class):
    """
    Возвращает параметры рамки (координаты и размеры) для выбранного класса.
    """
    if object_class in config.RECT_PARAMS:
        return (
            config.RECT_PARAMS[object_class]['x'], 
            config.RECT_PARAMS[object_class]['y'], 
            config.RECT_PARAMS[object_class]['width'], 
            config.RECT_PARAMS[object_class]['height']
        )
    else:
        return None  # Если класс не поддерживается

def check_object_position(object_center, rect_coords):
    """
    Проверяет положение объекта относительно рамки и выдаёт команды для передвижения.
    Сначала проверяется координата Y, затем X.
    """
    rect_x, rect_y, rect_w, rect_h = rect_coords

    x_center, y_center = object_center

    # Проверка координаты Y
    if y_center < rect_y:
        return "Объект выше рамки. Ехать вперед."  # Если объект выше, едем вперёд
    elif y_center > (rect_y + rect_h):
        return "Объект ниже рамки. Ехать назад."  # Если объект ниже, едем назад
    
    # Если Y в пределах рамки, проверяем X
    if x_center < rect_x:
        return "Объект левее рамки. Повернуть налево."
    elif x_center > (rect_x + rect_w):
        return "Объект правее рамки. Повернуть направо."
    
    # Если обе координаты в пределах рамки
    return "внутри рамки"

def process_command(command, camera):
    """
    Обработка команды для выбора класса и исключения класса 'robot'.
    Сразу же выполняется захват и сохранение кадра с камеры, а затем обработка через YOLO.
    """
    # Захват и сохранение кадра с камеры
    frame = capture_frame(camera)
    if frame is None:
        return
    
    # Если команда - это один из допустимых классов (кроме 'robot')
    if command in config.RECT_PARAMS and command != config.IGNORE_CLASS:
        message_command(f"Отслеживаем класс: {command}")

        # Получаем параметры рамки для выбранного класса
        rect_coords = get_rect_params_for_class(command)
        if rect_coords is None:
            message_command(f"Ошибка: Не найдены параметры рамки для класса '{command}'.")
            return

        # Загружаем изображение и выполняем YOLO-детекцию
        image_path = 'saved_images/captured_frame.jpg'
        object_info = process_yolo_detection(image_path)

        # Проверяем, есть ли объекты на изображении
        if object_info:
            for obj in object_info:
                class_id = obj['class_id']
                center = obj['center']

                # Преобразуем идентификатор класса в название
                class_name = config.CLASSES[class_id]

                # Проверяем, соответствует ли класс команде
                if class_name == command:
                    # Обработка для кнопок
                    # Обработка для кнопок
                    if class_name == 'buttons':
                        # Сначала проверяем, находится ли центр панели с кнопками в пределах рамки
                        position_message = check_object_position(center, rect_coords)

                        if position_message == "внутри рамки":
                            # Панель с кнопками в рамке, теперь проверяем цвет кнопок
                            while True:
                                button_color_value = button_color.detect_button_color(frame, obj['coords'])

                                if button_color_value in ['green', 'blue']:
                                    message_command(f"Нажать на кнопку {button_color_value}") 
                                    break  # Выходим из цикла, как только нужная кнопка оказалась в рамке
                                else:
                                    message_command(f"Игнорировать кнопку {button_color_value}")
                                    break  # Если кнопка не нужного цвета, цикл завершится

                        elif position_message == "Объект левее рамки. Повернуть налево.":
                            message_command("Панель кнопок слева. Повернуть налево.")
                            # Здесь можно добавить команду для поворота налево

                        elif position_message == "Объект правее рамки. Повернуть направо.":
                            message_command("Панель кнопок справа. Повернуть направо.")
                            # Здесь можно добавить команду для поворота направо

                        elif position_message == "Объект выше рамки. Ехать вперед.":
                            message_command("Панель кнопок выше рамки. Ехать вперёд.")
                            # Здесь можно добавить команду для движения вперёд

                        elif position_message == "Объект ниже рамки. Ехать назад.":
                            message_command("Панель кнопок ниже рамки. Ехать назад.")
                            # Здесь можно добавить команду для движения назад



                    # Обработка для класса "ball" (Шар)
                    elif class_name == 'ball':
                        position_message = check_object_position(center, rect_coords)
                        if position_message == "внутри рамки":
                            message_command("Поднять шар")
                        else:
                            message_command(f"Объект '{class_name}' найден! Центр: {center}. {position_message}")

                    # Обработка для класса "cube" (Куб)
                    elif class_name == 'cube':
                        position_message = check_object_position(center, rect_coords)
                        if position_message == "внутри рамки":
                            message_command("Поднять куб")
                        else:
                            message_command(f"Объект '{class_name}' найден! Центр: {center}. {position_message}")

                    # Обработка для класса "basket" (Корзина)
                    elif class_name == 'basket':
                        position_message = check_object_position(center, rect_coords)
                        if position_message == "внутри рамки":
                            message_command("Опустить объект в корзину")
                        else:
                            message_command(f"Объект '{class_name}' найден! Центр: {center}. {position_message}")

                else:
                    message_command(f"Объект '{class_name}' не соответствует команде '{command}'.")
        else:
            message_command("Объекты не найдены.")
    elif command == config.IGNORE_CLASS:
        message_command(f"Класс '{config.IGNORE_CLASS}' игнорируется.")
    else:
        message_command(f"Неизвестный класс: {command}")
