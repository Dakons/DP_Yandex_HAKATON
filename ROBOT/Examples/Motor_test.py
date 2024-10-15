import sys
import os

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

import libs.DP_MotorMoveLibr as Motor  # Импортируем библиотеку для управления моторами
import time  # Импортируем модуль для работы со временем


speed_left = -100
speed_right = 100


Motor.MotorMove(0, 0)
time.sleep(3)
#to ride back need ride more up duration 10%
#1.5 sec to do 360 degrees
Motor.MotorMove(speed_left, speed_right)
time.sleep(1.5)
Motor.MotorMove(speed_right, speed_right)
time.sleep(1)



