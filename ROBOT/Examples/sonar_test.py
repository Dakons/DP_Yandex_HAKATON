import time
from DP_sonar import Ultrasonic  # Импорт класса Ultrasonic из библиотеки

# Инициализация ультразвукового датчика
trig_pin = 23  # Задаём пин для TRIG (например, GPIO 23)
echo_pin = 24  # Задаём пин для ECHO (например, GPIO 24)
ultrasonic_sensor = Ultrasonic(trig_pin, echo_pin)  # Создаём объект датчика

# Основной цикл для получения и вывода расстояния
while True:
    distance = ultrasonic_sensor.get_distance()  # Получаем расстояние
    if distance != -1:
        print(f"Расстояние: {distance} см")  # Выводим результат
    else:
        print("Ошибка измерения или превышение расстояния.")
    
    time.sleep(1)  # Задержка между измерениями (1 секунда)
