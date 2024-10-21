import cv2
import config
from ultralytics import YOLO

def calibrate(camera):
    """
    Функция для калибровки камеры в режиме реального времени.
    Рисует рамки объектов и окружности для выбранного класса.
    """
    model = YOLO('yolov11n_trained.pt')  # Используем обученную модель

    while True:
        # Захват кадра с камеры
        ret, frame = camera.read()
        if not ret:
            print("Error: failed to capture image.")
            break

        # Выполнение детекции объектов на кадре
        results = model(frame)

        # Параметры окружности для выбранного класса
        circle_params = config.CIRCLE_PARAMS.get(config.selected_class)
        if circle_params:
            circle_center = (circle_params['center_x'], circle_params['center_y'])
            radius = circle_params['radius']
            
            # Рисуем окружность для выбранного класса
            cv2.circle(frame, circle_center, radius, (0, 255, 0), 2)
            cv2.putText(frame, f"Class: {config.selected_class}", (circle_center[0] - 20, circle_center[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Перебираем результаты детекции
        for result in results:
            for box in result.boxes:
                # Получаем координаты рамки объекта (x1, y1, x2, y2)
                coords = box.xyxy[0].tolist()
                x1, y1, x2, y2 = map(int, coords)

                # Рисуем рамку объекта на изображении
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # Получаем класс объекта
                class_id = int(box.cls)
                class_name = config.CLASSES[class_id]

                # Отображаем класс объекта и его центр на изображении
                x_center = (x1 + x2) // 2
                y_center = (y1 + y2) // 2
                cv2.putText(frame, f"{class_name}: {x_center},{y_center}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                            

                # Если это выбранный класс, рисуем точку в центре объекта и подписываем координаты
                if class_name == config.selected_class:
                    cv2.circle(frame, (x_center, y_center), 5, (0, 0, 255), -1)
                    cv2.putText(frame, f"Center: {x_center}, {y_center}", (x_center + 10, y_center),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        # Показ изображения в окне
        cv2.imshow('Calibration Mode', frame)

        # Для выхода нажмите 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождение ресурсов камеры и закрытие всех окон
    camera.release()
    cv2.destroyAllWindows()
