import sys
import os

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)


import libs.DP_tasks as Task
import time
import libs.DP_MotorMoveLibr as Motor






Motor.MotorMove(0,0)
time.sleep(2)
Task.drive_along_wall(side="LEFT",distance=10,setpoint=50,Kp=0.01,Ki=0,Kd=0)
Motor.MotorMove(0,0)
Motor.MotorMove(0,0)