import sys
import os
import time
import threading

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
distance = Ultrasonic.get_distance()
distance_filtered = round(Filter_sonar.filter(distance))

# Телеметрия
MoveData = TelemetrySender()

# Моторное движение и серво
sonServo = Servo(ANGLE_MAX=180, ANGLE_MIN=0, servonum=7)
sonServo.set(90)

# Флаг для завершения потока телеметрии
telemetry_active = True
pid_output = 0.0  # Глобальная переменная для хранения воздействия PID

# Инициализация переменных для управления механизмом
sweep_timemarker = time.time()  # Инициализация переменной
sweep_permission = "NO"  # Инициализация разрешения

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
    global telemetry_active  # Используем глобальный флаг
    global sweep_timemarker
    global sweep_permission  # Добавляем sweep_permission как глобальную переменную
    drive_time = distance * 1

    # Инициализация регулятора
    VectorRegulator = PIDRegulator(Kp=Kp, Ki=Ki, Kd=Kd, output_min=-100, output_max=100)

    # Засекаем время начала
    start_time = time.time()
    
    # Запуск потока для мониторинга данных
    telemetry_thread = threading.Thread(target=Telemetry, args=(VectorRegulator, setpoint))
    telemetry_thread.start()

    while True:  # Воздействия
        # Логика скорости с учетом положения стены
        if side == 'LEFT':
            sonServo.set(180)
        elif side == 'RIGHT':
            sonServo.set(0)
        else:
            raise ValueError("Неверное значение для 'side'. Ожидается 'left' или 'right'.")

        if (time.time() - sweep_timemarker) > pid_output:
            sweep_permission = "YES"

        # Передаем скорости на моторы
        if sweep_permission == "YES" and pid_output != 0:
            sweep_permission = "NO"
            Movement.sweep(BAZASPEED, 100, 0.1, side)
            sweep_timemarker = time.time()

        Motor.MotorMove(BAZASPEED, BAZASPEED)

        # Проверяем время, чтобы завершить выполнение через заданное время
        current_time = time.time()
        if (current_time - start_time) > drive_time:
            break
    
    # Останавливаем поток телеметрии
    telemetry_active = False
    telemetry_thread.join()

def Telemetry(VectorRegulator, setpoint):
    """Мониторинг, вычисление воздействия PID и отправка данных телеметрии."""
    global telemetry_active
    global pid_output
    
    while telemetry_active:  # Мониторинг, пока флаг True
        distance = Ultrasonic.get_distance()
        distance_filtered = round(Filter_sonar.filter(distance))
        
        # Расчет воздействия от PID-регулятора
        pid_output = VectorRegulator.regulate(distance_filtered, setpoint) * 0.1
        
        # Отправляем данные телеметрии
        MoveData.send_telemetry("Distance", distance_filtered)
        MoveData.send_telemetry("Error", VectorRegulator.regulate_error)
        MoveData.send_telemetry("Vector", pid_output)
        
        time.sleep(0.1)  # Добавляем небольшую паузу, чтобы не перегружать ЦП
