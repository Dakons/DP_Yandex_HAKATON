import sys
import os

import time
import libs.DP_tasks as Task
import libs.DP_MotorMoveLibr as Motor
import libs.DP_MotorMovements as Movement

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)



# Основная программа
Motor.MotorMove(0, 0)
time.sleep(2)

# Запускаем движение вдоль стены
Task.drive_along_wall(side="RIGHT", distance=30, setpoint=100, Kp=1, Ki=0, Kd=0)


Motor.MotorMove(0,0)
Motor.MotorMove(0,0)

