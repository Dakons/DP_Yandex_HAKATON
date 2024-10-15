import sys
import os

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

import time
import libs.DP_sonar as Ultrasonic # Импорт класса Ultrasonic из библиотеки

from libs.DP_servo import Servo
from libs.DP_teleplot import TelemetrySender

SonarData = TelemetrySender()
sonServo = Servo()

sonServo.set(7, 0)
# Инициализация ультразвукового датчика
trig_pin = 23  # Задаём пин для TRIG (например, GPIO 23)
echo_pin = 24  # Задаём пин для ECHO (например, GPIO 24)


# Основной цикл для получения и вывода расстояния
while True:
    distance = Ultrasonic.get_distance()  # Получаем расстояние
    if distance != -1:
        print(f"Расстояние: {distance} см")  # Выводим результат
        SonarData.send_telemetry("Dirty",distance)
    else:
        print("Ошибка измерения или превышение расстояния.")
        SonarData.send_telemetry("Dirty",distance)
    time.sleep(1)  # Задержка между измерениями (1 секунда)
