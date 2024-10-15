import sys
import os
import time

BAZASPEED = 80
# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

# Импортируем модуль и используем псевдоним
from libs.DP_Regulator import PIDRegulator
from libs.DP_Filter import Filter 
import libs.DP_sonar as Ultrasonic
import libs.DP_MotorMoveLibr as Motor
from libs.DP_teleplot import TelemetrySender
from libs.DP_Filter import Filter
from libs.DP_servo import Servo

Filter_sonar = Filter(5,0.3)

MoveData = TelemetrySender()

sonServo = Servo()

sonServo.set(7, 0)

def constrain(value, min_value, max_value):
    return max(min(value, max_value), min_value)


VectorRegulator = PIDRegulator()

Last_time = time.time()
while True:
    distance = Ultrasonic.get_distance()  # Получаем расстояние
    distance_filtered = round(Filter_sonar.filter(distance))
    VectorRegulator.PIDRegulator(Kp=1, Ki=0, Kd=0)
    
    Vector = VectorRegulator.regulate(distance_filtered, 50.0)
    
    Left_Speed = BAZASPEED + Vector
    Right_Speed = BAZASPEED - Vector

    Left_Speed = constrain(Left_Speed, -100, 100)
    Right_Speed = constrain(Right_Speed, -100, 100)

    Motor.MotorMove(Left_Speed, Right_Speed)
    MoveData.send_telemetry("Distantion", distance_filtered)
    Now_time = time.time()
    if (Now_time - Last_time) > 10:
        break

Motor.MotorMove(0,0)




