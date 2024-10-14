from builtins import hex, eval, int, object  # Стандартные функции для работы с числами и объектами
from xr_i2c import I2c  # Импорт класса для работы с I2C протоколом
import os  # Модуль для работы с операционной системой

i2c = I2c()  # Инициализация объекта I2C для управления устройствами
import xr_config as cfg  # Конфигурационный файл с параметрами
from xr_configparser import HandleConfig  # Импорт обработчика конфигурационных файлов

# Путь к файлу конфигурации данных
path_data = os.path.dirname(os.path.realpath(__file__)) + '/data.ini'
cfgparser = HandleConfig(path_data)  # Инициализация конфигурационного парсера


class Servo(object):
    """
    Класс для управления сервоприводом
    """
    def __init__(self):
        pass  # Конструктор, который ничего не делает на данном этапе

    def angle_limit(self, angle):
        """
        Ограничение угла сервопривода, чтобы предотвратить его блокировку или повреждение
        :param angle: угол, который нужно ограничить
        :return: корректированный угол в пределах допустимых значений
        """
        # Проверка и корректировка угла, если он выходит за допустимые пределы
        if angle > cfg.ANGLE_MAX:  # Если угол превышает максимальный предел
            angle = cfg.ANGLE_MAX
        elif angle < cfg.ANGLE_MIN:  # Если угол меньше минимального предела
            angle = cfg.ANGLE_MIN
        return angle  # Возвращаем скорректированное значение угла

    def set(self, servonum, servoangle):
        """
        Установка угла для сервопривода
        :param servonum: номер сервопривода
        :param servoangle: угол для установки
        :return: ничего не возвращает
        """
        angle = self.angle_limit(servoangle)  # Ограничиваем угол перед установкой
        # Подготовка команды для отправки по шине I2C
        buf = [0xff, 0x01, servonum, angle, 0xff]
        try:
            # Отправка данных на микроконтроллер через I2C
            i2c.writedata(i2c.mcu_address, buf)
        except Exception as e:
            # Обработка ошибок в случае неудачной отправки данных
            print('Ошибка записи в сервопривод:', e)

    def store(self):
        """
        Сохранение текущих углов сервоприводов в файл конфигурации
        :return: ничего не возвращает
        """
        # Сохраняем текущие значения углов сервоприводов в секции "servo" файла данных
        cfgparser.save_data("servo", "angle", cfg.ANGLE)

    def restore(self):
        """
        Восстановление углов сервоприводов из файла конфигурации
        :return: ничего не возвращает
        """
        # Получаем сохранённые значения углов сервоприводов из файла данных
        cfg.ANGLE = cfgparser.get_data("servo", "angle")
        # Восстанавливаем углы для каждого из сервоприводов
        for i in range(0, 8):  # Предполагается, что имеется 8 сервоприводов
            cfg.SERVO_NUM = i + 1  # Номер текущего сервопривода
            cfg.SERVO_ANGLE = cfg.ANGLE[i]  # Восстановленный угол для этого сервопривода
            self.set(i + 1, cfg.ANGLE[i])  # Устанавливаем угол для каждого сервопривода
