import sys
import os

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)


from builtins import hex, eval, int, object  # Стандартные функции для работы с числами и объектами
from libs.DP_i2c import I2c  # Импорт класса для работы с I2C протоколом
import os  # Модуль для работы с операционной системой

ANGLE_MAX = 160
ANGLE_MIN = 15

i2c = I2c()  # Инициализация объекта I2C для управления устройствами

class Servo(object):
    """
    Класс для управления сервоприводом
    """
    def __init__(self, ANGLE_MAX, ANGLE_MIN, servonum):
        self.ANGLE_MAX = ANGLE_MAX
        self.ANGLE_MIN = ANGLE_MIN
        self.servonum = servonum
    def angle_limit(self, angle):
        """
        Ограничение угла сервопривода, чтобы предотвратить его блокировку или повреждение
        :param angle: угол, который нужно ограничить
        :return: корректированный угол в пределах допустимых значений
        """
        # Проверка и корректировка угла, если он выходит за допустимые пределы
        if angle > self.ANGLE_MAX:  # Если угол превышает максимальный предел
            angle = self.ANGLE_MAX
        elif angle < self.ANGLE_MIN:  # Если угол меньше минимального предела
            angle = self.ANGLE_MIN
        return angle  # Возвращаем скорректированное значение угла

    def set(self, servoangle):
        """
        Установка угла для сервопривода
        :param servonum: номер сервопривода
        :param servoangle: угол для установки
        :return: ничего не возвращает
        """
        angle = self.angle_limit(servoangle)  # Ограничиваем угол перед установкой
        # Подготовка команды для отправки по шине I2C
        buf = [0xff, 0x01, self.servonum, angle, 0xff]
        try:
            # Отправка данных на микроконтроллер через I2C
            i2c.writedata(i2c.mcu_address, buf)
        except Exception as e:
            # Обработка ошибок в случае неудачной отправки данных
            print('Ошибка записи в сервопривод:', e)

