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
    if color == "GREEN":
        sendbuf = [0xff, 0x02, 0x08, 0x04, 0xff]
    if color == "RED":
        sendbuf = [0xff, 0x02, 0x08, 0x01, 0xff]
    i2c.writedata(i2c.mcu_address, sendbuf)
    time.sleep(0.01)
    print("Color set:")
    print(color)
    

#set_all_leds("GREEN")
#time.sleep(5)

    
