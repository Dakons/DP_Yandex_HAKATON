import sys
import os

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

import time
import libs.DP_GPIO as gpio  # Импортируем вашу библиотеку

# Пины ультразвукового датчика для измерения расстояния
ECHO = 4    # Пин для получения сигнала от датчика (эхо-сигнал)
TRIG = 17   # Пин для отправки сигнала триггера (активация датчика)

# Инициализация пинов ультразвукового датчика
gpio.digital_write(TRIG, 0)  # Устанавливаем TRIG в низкий уровень (LOW)

def get_distance():
    # Функция для получения расстояния в сантиметрах
    gpio.digital_write(TRIG, 1)  # Устанавливаем TRIG в высокий уровень
    time.sleep(0.00001)  # Удерживаем HIGH в течение 10 мкс
    gpio.digital_write(TRIG, 0)  # Устанавливаем TRIG в низкий уровень

    
    start_time = time.time()  # Время начала
    stop_time = time.time()  # Время остановки
    init_time = start_time
    # Ждем, пока ECHO не станет высоким
    while gpio.digital_read(ECHO) == 0:
        start_time = time.time()
        if (time.time() - init_time > 0.1):
            print("NO IMPULSE")
            SOS_FLAG  = 1
            break

    # Ждем, пока ECHO не станет низким
    while gpio.digital_read(ECHO) == 1:
        stop_time = time.time()

    # Вычисляем расстояние в сантиметрах
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Скорость звука ~34300 см/с
    if SOS_FLAG ==1:
        SOS_FLAG =0
        distance = -1
    return distance


