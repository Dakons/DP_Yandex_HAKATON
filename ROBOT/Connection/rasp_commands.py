import sys
import os
import time
kp = 12
ki = -0.04
kd = 0
# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

import libs.DP_MotorMoveLibr as Motor  # Импортируем библиотеку для управления моторами
import libs.DP_servo as Servo
import libs.DP_tasks as tasks
import asyncio
serv_1 = Servo.Servo(180, 0, 1)
serv_2 = Servo.Servo(180, 0, 2)
serv_3 = Servo.Servo(180, 0, 3)
serv_4 = Servo.Servo(180, 0, 4)
serv_7 = Servo.Servo(180, 0, 7)
serv_8 = Servo.Servo(180, 0, 8)

# async def do_commands(command, conn):
#     name, *values = command.split(" ")
#     if name == "Motor":
#         Motor.MotorMove(int(values[0]), int(values[1]))
#     if name == "Servo_take_cube":
#         set_servo(175, 25, 90, 35)
#         set_servo(65, 180, 90, 35)
#         set_servo(65, 180, 90, 70)
#         set_servo(175, 25, 90, 70)
#     if name == "Servo_take_ball":
#         set_servo(175, 25, 90, 35)
#         set_servo(65, 180, 90, 35)
#         set_servo(65, 180, 90, 80)
#         set_servo(175, 25, 90, 80)

#     if name == "Camera":
#         serv_7.set(int(values[1]))
#         serv_8.set(int(values[2]))

#     if name == "Go_Straight":
#         side = values[0]
#         Duration = float(values[1])
#         setpoint = float(values[3])
#         tasks.drive_along_wall(side, Duration, setpoint)

async def do_commands(command, conn):
    name, *values = command.split(" ")
    match name:
        case "Motor":
            Motor.MotorMove(int(values[0]), int(values[1]))
        case "Servo_take_cube_floor":
            set_servo(175, 25, 90, 35)
            time.sleep(0.5)
            set_servo(65, 180, 90, 35)
            time.sleep(0.5)
            set_servo(65, 180, 90, 70)
            time.sleep(0.5)
            set_servo(175, 25, 90, 70)
        case "Servo_take_ball_floor":
            set_servo(175, 25, 90, 35)
            time.sleep(0.5)
            set_servo(65, 180, 90, 35)
            time.sleep(0.5)
            set_servo(65, 180, 90, 80)
            time.sleep(0.5)
            set_servo(175, 25, 90, 80)
        case "Servo_put_cube_to_basket":
            set_servo(175, 25, 90, 70)
            time.sleep(0.5)
            set_servo(175, 90, 90, 70)
            time.sleep(0.5)
            set_servo(175, 70, 90, 70)
            time.sleep(0.5)
            set_servo(175, 90, 90, 70)
            time.sleep(0.5)
            set_servo(175, 70, 90, 70)
            time.sleep(0.5)
            set_servo(175, 25, 90, 35)
        case "Servo_put_ball_to_basket":
            set_servo(175, 25, 90, 80)
            time.sleep(0.5)
            set_servo(175, 90, 90, 80)
            time.sleep(0.5)
            set_servo(175, 70, 90, 80)
            time.sleep(0.5)
            set_servo(175, 90, 90, 80)
            time.sleep(0.5)
            set_servo(175, 70, 90, 80)
            time.sleep(0.5)
            set_servo(175, 25, 90, 35)

        case "Camera":
            serv_7.set(int(values[0]))
            serv_8.set(int(values[1]))

        case "Go_Straight":
            side = values[0]
            Duration = float(values[1])
            setpoint = float(values[2])
            tasks.drive_along_wall(side, Duration, setpoint, ki, kp, kd)
        case "Turn":
            added_angle = float(values[0])
            tasks.add_angle(added_angle)

async def set_servo(angle_1, angle_2, angle_3, angle_4):
    serv_1.set(angle_1)
    serv_2.set(angle_2)
    serv_3.set(angle_3)
    serv_4.set(angle_4)