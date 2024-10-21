# config.py

# Список классов объектов, которые используются в модели YOLO
CLASSES = [
    'ball',     # Шар
    'basket',   # Корзина
    'buttons',  # Панель с кнопками
    'cube',     # Куб
    'robot'     # Робот
]

# Переменная для хранения выбранного класса
selected_class = None

# Параметры окружностей для каждого класса
CIRCLE_PARAMS = {
    'ball': {'center_x': 320, 'center_y': 240, 'radius': 50},
    'basket': {'center_x': 320, 'center_y': 240, 'radius': 70},
    'buttons': {'center_x': 320, 'center_y': 240, 'radius': 60},
    'cube': {'center_x': 320, 'center_y': 240, 'radius': 50},
}

