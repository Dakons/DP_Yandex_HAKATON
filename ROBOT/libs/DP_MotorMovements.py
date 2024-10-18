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

def turn (speed_normal, direction):
    if direction == "CLOCKWISE":
        Motor.MotorMove(speed_normal, -speed_normal)
    elif direction == "COUNTERCLOCKWISE":
        Motor.MotorMove(-speed_normal, speed_normal)


def Smooth_turn_Start(speed_normal, step, direction):
    if direction == "CLOCKWISE":
        for i in range(0, speed_normal+1, 1):
            Motor.MotorMove(i,-i)
            time.sleep(step)
        Motor.MotorMove(speed_normal,-speed_normal)
    elif direction == "COUNTERCLOCKWISE":
        for i in range(0, speed_normal+1, 1):
            Motor.MotorMove(-i,i)
            time.sleep(step)
        Motor.MotorMove(-speed_normal, speed_normal)

def Smooth_turn_Stop(speed_normal, step, direction):
    if direction == "CLOCKWISE":
        for i in range(speed_normal, -1, -1):
            Motor.MotorMove(i,-i)
            time.sleep(step)
    elif direction == "COUNTERCLOCKWISE":
        for i in range(speed_normal, -1, -1):
            Motor.MotorMove(-i,i)
            time.sleep(step)
        Motor.MotorMove(-speed_normal, speed_normal)
    Motor.MotorMove(0,0)

def Smooth_line_Start(speed_normal, step):
    for i in range(0, speed_normal+1, 1):
        Motor.MotorMove(i,i)
        time.sleep(step)
    Motor.MotorMove(speed_normal,speed_normal)

def Smooth_line_Stop(speed_normal, step):
    for i in range(speed_normal, -1, -1):
        Motor.MotorMove(i,i)
        time.sleep(step)
    Motor.MotorMove(0,0)

