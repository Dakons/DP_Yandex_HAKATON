import time
import sys
import os

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

from libs.DP_i2c import I2c

i2c = I2c()

colors = {"GREEN": 2, "RED": 1}


def set_all_leds(color):
    """
    Устанавливает один и тот же цвет для всех светодиодов в группе.
    
    :param group: группа светодиодов (1 для индикаторов заряда, 2 для фар)
    :param color: цвет светодиодов (1-8, предопределённые значения)
    """
    # Устанавливаем цвет для всех 8 светодиодов в указанной группе
    sendbuf = [0xff, 0x06, colors[color], 0x00, 0xff]
    i2c.writedata(i2c.mcu_address, sendbuf)
    time.sleep(0.01)
