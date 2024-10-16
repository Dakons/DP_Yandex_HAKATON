import sys
import os
import time

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
sonServo = Servo(ANGLE_MAX = 180, ANGLE_MIN = 0, servonum=7)
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
    VectorRegulator = PIDRegulator(Kp=Kp, Ki=Ki, Kd=Kd,output_min=-2,output_max=2)

    # Засекаем время начала
    start_time = time.time()
    sweep_permission = "YES"
    sweep_timemarker = 0.0
    while True:

        # Логика скорости с учетом положения стены
        if side == 'LEFT':
            sonServo.set(180)
            # Если стена слева
            #Left_Speed = BAZASPEED - Vector
            #Right_Speed = BAZASPEED + Vector
        elif side == 'RIGHT':
            sonServo.set(0)
            # Если стена справа
           # Left_Speed = BAZASPEED + Vector
            #Right_Speed = BAZASPEED - Vector
        else:
            raise ValueError("Неверное значение для 'side'. Ожидается 'left' или 'right'.")
        # Получаем расстояние от датчика
        distance = Ultrasonic.get_distance()
        distance_filtered = round(Filter_sonar.filter(distance))
        MoveData.send_telemetry("Distance", distance_filtered)
        print(distance_filtered)
        
        
        # ПИД регуляция расстояния до стены
        Vector = VectorRegulator.regulate(distance_filtered, setpoint)
        
        
        if (time.time() - sweep_timemarker) > Vector:
            sweep_permission == "YES"
        # Передаем скорости на моторы
        
        if sweep_permission == "YES" and Vector !=0:
            sweep_permission == "NO"
            sweep_timemarker = time.time()
            Movement.sweep(BAZASPEED, 100, 0.1, side)#Нужно намутить контроль по времени, чтобы не делалось больше чем надо
            
        Motor.MotorMove(BAZASPEED, BAZASPEED)  

        # Отправка телеметрии
        
        #MoveData.send_telemetry("P", VectorRegulator.P)
        #MoveData.send_telemetry("I", VectorRegulator.I)
        #MoveData.send_telemetry("D", VectorRegulator.D)
        #MoveData.send_telemetry("Error", VectorRegulator.regulate_error)
        #MoveData.send_telemetry("Vector", Vector)
        
        # Проверяем время, чтобы завершить выполнение через заданное время
        current_time = time.time()
        if (current_time - start_time) > drive_time:
            break

    # Остановка моторов после завершения движения
    Motor.MotorMove(0, 0)

