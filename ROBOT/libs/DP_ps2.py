import sys
import os
import time
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

from libs.DP_i2c import I2c

i2c = I2c()


while 1:
    ps2check = i2c.readdata(0x19, 0x01)
    read_key = i2c.readdata(0x19, 0x03)  # Чтение первого байта значений кнопок
    read_key1 = i2c.readdata(0x19, 0x04) # Чтение второго байта значений кнопок

    print(f"ps2check{ps2check}")
    print(f"read_key{read_key}")
    print(f"read_key1{read_key1}")
    time.sleep(0.1)