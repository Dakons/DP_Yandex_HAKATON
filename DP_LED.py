from builtins import int, range

import time
from DP_i2c import I2c

COLOR = {'black': 0, 'red': 1, 'orange': 2, 'yellow': 3, 'green': 4, 'Cyan': 5, 'blue': 6, 'violet': 7, 'white': 8}

CAR_LIGHT = 2

i2c = I2c()

class Car_light(object):
    def __init__(self):
        pass

    def set_led(self, group, num, color):
        """
        Установить состояние RGB-светодиода
        :param group: Группа светодиодов, 1 для индикатора заряда, 2 для автомобильных фар
        :param num: Индекс светодиода
        :param color: Установить цвет, в config можно выбрать соответствующий цвет из COLOR, можно установить только предопределенные цвета
        :return:
        """
        if 0 < num < 9 and 0 < group < 3 and color < 9:
            sendbuf = [0xff, group + 3, num, color, 0xff]
            i2c.writedata(i2c.mcu_address, sendbuf)

    def open_light(self):
        """
        Включить все фары :return:
        """
        # print("Все фары включены")
        self.set_ledgroup(CAR_LIGHT, 8, COLOR['red'])

    def close_light(self):
        """
        Выключить все фары :return:
        """
        # print("Все фары выключены")
        self.set_ledgroup(CAR_LIGHT, 8, COLOR['black'])