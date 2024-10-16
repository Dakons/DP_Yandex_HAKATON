import sys
import os
import time
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

import libs.DP_MotorMoveLibr as Motor

direction_inside = ""
def sweep (speed_normal, speed_boom, duration, direction: str):

    if (speed_boom < 0) and direction == "LEFT":
        print("sit_1")
        direction_inside = "LEFT"
        
    if (speed_boom > 0) and direction == "LEFT":
        print("sit_2")
        direction_inside = "RIGHT"

    if (speed_boom > 0) and direction == "RIGHT":
        print("sit_3")
        direction_inside = "LEFT"

    if (speed_boom < 0) and direction == "RIGHT":
        print("sit_4")
        direction_inside = "RIGHT"

    speed_boom=abs(speed_boom)
    if direction_inside == "RIGHT":
        speed_boomed = speed_normal+speed_boom
        Motor.MotorMove(speed_boomed, speed_normal)
        time.sleep(duration)
        Motor.MotorMove(speed_normal, speed_boomed)
        time.sleep(duration)
        Motor.MotorMove(speed_normal, speed_normal)
    elif direction_inside == "LEFT":
        speed_boomed = speed_normal+speed_boom
        Motor.MotorMove(speed_normal, speed_boomed)
        time.sleep(duration)
        Motor.MotorMove(speed_boomed, speed_normal)
        time.sleep(duration)
        Motor.MotorMove(speed_normal, speed_normal)



def turn (speed_normal, angle):
    if angle < 0:
        Motor.MotorMove(-speed_normal, speed_normal)
    elif angle > 0:
        Motor.MotorMove(speed_normal, -speed_normal)
    time.sleep(angle*0.8)
    Motor.MotorMove(0,0)