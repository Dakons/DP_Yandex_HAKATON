import os
import time
from builtins import IOError, object, len
import smbus

class I2c(object):
    def __init__(self):
        # Устанавливаем адреса устройств
        self.mcu_address = 0x18
        # Создаем объект для работы с шиной I2C (используем /dev/i2c1)
        self.device = smbus.SMBus(1)

    def writedata(self, address, values):
        """
        # Запись данных по адресу I2C
        """
        try:
            # Пишем блок данных. Первый параметр: адрес устройства, второй параметр: адрес регистра для записи,
            # но у нашего MCU нет адреса регистра, поэтому пишем первый фрейм данных,
            # третий параметр: данные для записи
            self.device.write_i2c_block_data(address, values[0], values[1:len(values)])
            time.sleep(0.005)
        except Exception as e:  # Ошибка записи 
            pass
            # print('Ошибка записи i2c:', e)
            # os.system('sudo i2cdetect -y 1')

    def readdata(self, address, index):
        """
        # Чтение одного байта данных с I2C
        """
        try:
            # Читаем байт данных с указанного смещения index у устройства
            value = self.device.read_byte_data(address, index)
            time.sleep(0.005)
            return value  # Возвращаем прочитанные данные
        except Exception as e:  # Ошибка чтения
            pass
            # print('Ошибка чтения i2c:', e)
            # os.system('sudo i2cdetect -y 1')
