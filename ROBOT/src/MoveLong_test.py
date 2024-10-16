import sys
import os

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)


import libs.DP_tasks as Task
import time
import libs.DP_MotorMoveLibr as Motor







time.sleep(1)
Task.drive_along_wall("RIGHT",10,75,0.5,0,0)
Motor.MotorMove(0,0)