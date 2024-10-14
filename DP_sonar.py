

import time
import DP_GPIO as gpio  # Импортируем модуль для работы с GPIO

class Ultrasonic(object):
    def __init__(self, trig_pin, echo_pin):
        """
        Инициализация ультразвукового датчика.

        :param trig_pin: Номер GPIO пина для сигнала TRIG.
        :param echo_pin: Номер GPIO пина для сигнала ECHO.
        """
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        
        gpio.setup(self.trig_pin, gpio.OUTPUT)  # Настраиваем TRIG как выход
        gpio.setup(self.echo_pin, gpio.INPUT)  # Настраиваем ECHO как вход

    def get_distance(self):
        """
        Функция для получения расстояния с помощью ультразвукового датчика.
        Возвращает расстояние в сантиметрах.
        """
        time_count = 0
        time.sleep(0.01)  # Задержка для стабилизации

        # Отправляем ультразвуковой сигнал
        gpio.digital_write(self.trig_pin, True)  # Устанавливаем высокий уровень на TRIG
        time.sleep(0.000015)  # Длительность сигнала
        gpio.digital_write(self.trig_pin, False)  # Устанавливаем низкий уровень на TRIG
        
        # Ждем, пока ECHO не станет высоким
        while not gpio.digital_read(self.echo_pin):  
            pass
        t1 = time.time()  # Запоминаем время начала

        # Ждем, пока ECHO не станет низким
        while gpio.digital_read(self.echo_pin):  
            if time_count < 2000:  # Тайм-аут для предотвращения бесконечного цикла
                time_count += 1
                time.sleep(0.000001)  # Маленькая задержка
            else:
                print("Нет сигнала ECHO! Пожалуйста, проверьте соединение.")
                return -1  # Возвращаем -1 в случае ошибки
        t2 = time.time()  # Запоминаем время окончания

        # Вычисляем расстояние: время * скорость звука / 2
        distance = (t2 - t1) * 340 / 2 * 100  # Приводим к сантиметрам
        if distance < 500:  # Проверяем, что расстояние в пределах 5 метров
            return round(distance, 2)  # Округляем до двух знаков
        else:
            return -1  # Если превышает 5 метров, возвращаем -1

# Пример использования:
if __name__ == "__main__":
    # Замените 17 и 27 на номера пинов вашего датчика
    ultrasonic_sensor = Ultrasonic(trig_pin=17, echo_pin=27)  
    while True:
        distance = ultrasonic_sensor.get_distance()  # Получаем расстояние
        if distance != -1:
            print(f"Расстояние: {distance} см")  # Выводим расстояние
        else:
            print("Ошибка получения расстояния.")  # Сообщение об ошибке
        time.sleep(1)  # Задержка между измерениями
