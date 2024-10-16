import sys
import os
import time
import threading  # Добавляем поддержку многопоточности

# Константы
BAZASPEED = 5

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

# Импортируем необходимые модули
from libs.DP_Regulator import PIDRegulator
from libs.DP_Filter import Filter
import libs.DP_sonar as Ultrasonic
import libs.DP_MotorMoveLibr as Motor
from libs.DP_teleplot import TelemetrySender
from libs.DP_Filter import Filter
from libs.DP_servo import Servo
import libs.DP_MotorMovements as Movement

# Фильтр для сенсора
Filter_sonar = Filter(5, 0.3)

# Телеметрия
MoveData = TelemetrySender()

# Моторное движение и серво
sonServo = Servo(ANGLE_MAX=180, ANGLE_MIN=0, servonum=7)
sonServo.set(90)

def constrain(value, min_value, max_value):
    """Ограничивает значение в заданных пределах."""
    return max(min(value, max_value), min_value)

def drive_along_wall(side: str, distance, setpoint, Kp, Ki, Kd):
    """
    Управляет роботом для движения вдоль стены заданное время.
    
    Параметры:
        side (str): 'left' или 'right', указывает, с какой стороны находится стена.
        distance (float): Расстояние
        setpoint (float): Установочное значение (желаемое расстояние до стены).
        Kp (float): Пропорциональный коэффициент ПИД регулятора.
        Ki (float): Интегральный коэффициент ПИД регулятора.
        Kd (float): Дифференциальный коэффициент ПИД регулятора.
    """
    drive_time = distance * 1

    # Инициализация регулятора
    VectorRegulator = PIDRegulator(Kp=Kp, Ki=Ki, Kd=Kd, output_min=-100, output_max=100)

    # Засекаем время начала
    start_time = time.time()
    sweep_permission = True
    sweep_timemarker = 0.0
    sweep_thread = None  # Инициализируем переменную потока
    sweep_stop_flag = threading.Event()  # Создаем флаг для остановки потока

    while True:

        # Логика скорости с учетом положения стены
        if side == 'LEFT':
            sonServo.set(180)
        elif side == 'RIGHT':
            sonServo.set(0)
        else:
            raise ValueError("Неверное значение для 'side'. Ожидается 'left' или 'right'.")

        # Получаем расстояние от датчика
        distance = Ultrasonic.get_distance()
        distance_filtered = round(Filter_sonar.filter(distance))
        MoveData.send_telemetry("Distance", distance_filtered)
        print(distance_filtered)

        # ПИД регуляция расстояния до стены
        Vector = VectorRegulator.regulate(distance_filtered, setpoint)

        if (time.time() - sweep_timemarker) > 1:
            sweep_permission = True

        # Запускаем sweep в отдельном потоке, чтобы не блокировать основной код
        if sweep_permission and Vector != 0:
            sweep_permission = False
            sweep_timemarker = time.time()
            # Создаем и запускаем поток
            sweep_thread = threading.Thread(target=Movement.sweep, args=(BAZASPEED, Vector, 1, side, sweep_stop_flag))
            sweep_thread.start()

        Motor.MotorMove(BAZASPEED, BAZASPEED)

        # Проверяем время, чтобы завершить выполнение через заданное время
        current_time = time.time()
        if (current_time - start_time) > drive_time:
            if sweep_thread is not None and sweep_thread.is_alive():
                sweep_stop_flag.set()  # Устанавливаем флаг остановки
                sweep_thread.join()  # Ожидаем завершения потока
            break

    # Остановка моторов после завершения движения
    Motor.MotorMove(0, 0)

# В функции sweep вам нужно будет добавить логику для проверки флага остановки
# Например:
# def sweep(speed, vector, duration, side, stop_flag):
#     while not stop_flag.is_set():
#         # Ваш код для выполнения трюков
#         time.sleep(0.1)  # Задержка для снижения нагрузки на CPU
