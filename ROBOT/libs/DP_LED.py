import time
from DP_i2c import I2c

i2c = I2c()

class CarLight:
    def __init__(self):
        pass

    def set_all_leds(self, group, color):
        """
        Устанавливает один и тот же цвет для всех светодиодов в группе.
        
        :param group: группа светодиодов (1 для индикаторов заряда, 2 для фар)
        :param color: цвет светодиодов (1-8, предопределённые значения)
        """
        if 0 < group < 3 and 0 < color < 9:
            # Устанавливаем цвет для всех 8 светодиодов в указанной группе
            sendbuf = [0xff, group + 1, 8, color, 0xff]
            i2c.writedata(i2c.mcu_address, sendbuf)
            time.sleep(0.01)

# Пример использования:
car_light = CarLight()
car_light.set_all_leds(1, 3)  # Устанавливаем цвет 3 для всех светодиодов группы 1 (например, красный)
