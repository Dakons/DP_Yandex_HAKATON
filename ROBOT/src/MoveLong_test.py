import sys
import os
# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)
import time
import ROBOT.libs.DP_tasks as Task
import libs.DP_MotorMoveLibr as Motor
import libs.DP_MotorMovements as Movement



# Основная программа
Motor.MotorMove(0, 0)
time.sleep(2)
#Task.add_angle(90,0)
#time.sleep(2)
# Запускаем движение вдоль стены
Task.drive_along_wall(side="LEFT", distance=12, setpoint=30, kp=4, ki=-0.04, kd=0)#-0.16
Motor.MotorMove(0,0)
time.sleep(2)
Task.add_angle(180.0,0)
Motor.MotorMove(0,0)
time.sleep(2)
'''
Task.add_angle(180.0,0)
time.sleep(2)
Task.drive_along_wall(side="RIGHT", distance=10, setpoint=30, kp=0.2, ki=-0.01, kd=0)
time.sleep(2)
Motor.MotorMove(0,0)
time.sleep(2)
Task.add_angle(180.0,0)
Motor.MotorMove(0,0)
time.sleep(2)
'''
