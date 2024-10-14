import time
from DP_LED import CarLight  # Импорт класса CarLight из библиотеки DP_LED

# Инициализация объекта для управления светодиодами
car_light = CarLight()

# Определяем цвета
GREEN = 4  # Зелёный
RED = 1    # Красный

# Бесконечный цикл для смены цветов каждые 2 секунды
while True:
    # Устанавливаем все светодиоды на зелёный цвет
    car_light.set_all_leds(2, GREEN)  # 2 означает группу фар
    time.sleep(2)  # Ждём 2 секунды
    
    # Устанавливаем все светодиоды на красный цвет
    car_light.set_all_leds(2, RED)
    time.sleep(2)  # Ждём 2 секунды
