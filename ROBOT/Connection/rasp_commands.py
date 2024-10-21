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

async def set_servo(angle_1, angle_2, angle_3, angle_4):
    serv_1.set(angle_1)
    serv_2.set(angle_2)
    serv_3.set(angle_3)
    serv_4.set(angle_4)
    

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
            print("Motor")
        case "Servo_take_cube_floor":
            await set_servo(175, 25, 90, 35)
            time.sleep(0.5)
            await set_servo(65, 180, 90, 35)
            time.sleep(0.5)
            tasks.drive_line(20)
            time.sleep(0.5)
            await set_servo(65, 180, 90, 70)
            time.sleep(0.5)
            await set_servo(175, 25, 90, 70)
            print("Servo_take_cube_floor")
        case "Servo_take_ball_floor":
            await set_servo(175, 25, 90, 35)
            time.sleep(0.5)
            await set_servo(65, 180, 90, 35)
            time.sleep(0.5)
            tasks.drive_line(20)
            time.sleep(0.5)
            await set_servo(65, 180, 90, 80)
            time.sleep(0.5)
            await set_servo(175, 25, 90, 80)
            print("Servo_take_ball_floor")
        case "Servo_put_cube_to_basket":
            await set_servo(175, 25, 90, 70)
            time.sleep(0.5)
            await set_servo(175, 90, 90, 70)
            time.sleep(0.5)
            tasks.drive_line(10)
            await set_servo(175, 70, 90, 35)
            time.sleep(0.5)
            await set_servo(175, 90, 90, 35)
            time.sleep(0.5)
            tasks.drive_line(-10)
            await set_servo(175, 25, 90, 35)
            print("Servo_put_cube_to_basket")
        case "Servo_put_ball_to_basket":
            await set_servo(175, 25, 90, 80)
            time.sleep(0.5)
            await set_servo(175, 90, 90, 80)
            time.sleep(0.5)
            tasks.drive_line(10)
            await set_servo(175, 70, 90, 35)
            time.sleep(0.5)
            await set_servo(175, 90, 90, 35)
            time.sleep(0.5)
            tasks.drive_line(-10)
            await set_servo(175, 25, 90, 35)
            print("Servo_put_ball_to_basket")

        case "Camera":
            serv_7.set(int(values[0]))
            serv_8.set(int(values[1]))
        case "Servo_take_cube_from_basket":
            await set_servo(175, 25, 90, 45)
            time.sleep(0.5)
            await set_servo(175, 90, 90, 45)
            time.sleep(0.5)
            tasks.drive_line(13)
            await set_servo(175, 55, 90, 45)
            time.sleep(0.5)
            await set_servo(175, 55, 90, 70)
            time.sleep(0.5)
            await set_servo(175, 90, 90, 70)
            time.sleep(0.5)
            tasks.drive_line(-13)
            await set_servo(175, 25, 90, 70)
            print("Servo_take_cube_from_basket")
            
        case "Servo_take_ball_from_basket":
            await set_servo(175, 25, 90, 45)
            time.sleep(0.5)
            await set_servo(175, 90, 90, 45)
            time.sleep(0.5)
            tasks.drive_line(13)
            await set_servo(175, 55, 90, 45)
            time.sleep(0.5)
            await set_servo(175, 55, 90, 80)
            time.sleep(0.5)
            await set_servo(175, 90, 90, 80)
            time.sleep(0.5)
            tasks.drive_line(-13)
            await set_servo(175, 25, 90, 80)
        case "Servo_push_button":
            await set_servo(175, 25, 90, 80)
            time.sleep(0.5)
            await set_servo(175,160, 0, 80)
            time.sleep(0.5)
            tasks.drive_line(13)
            await set_servo(175, 45, 0, 80)
            time.sleep(0.5)
            await set_servo(175, 90, 90, 80)
            time.sleep(0.5)
            tasks.drive_line(-13)
            await set_servo(175, 25, 90, 80)
            print("Servo_push_button")
            
        case "Go_Straight_Wall":
            side = values[0]
            Distantion = float(values[1])
            setpoint = float(values[2])
            tasks.drive_along_wall(side, Distantion, setpoint)
        case "Turn":
            added_angle = int(values[0])
            tasks.add_angle(added_angle)
        case "Go_Straight":
            Distantion = float(values[0])
            tasks.drive_line(Distantion)

