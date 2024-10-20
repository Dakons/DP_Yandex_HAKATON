import sys
import os

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

import DP_MotorMoveLibr as Motor  # Импортируем библиотеку для управления моторами
import DP_servo as Servo
import asyncio
import config as cfg
serv_1 = Servo.Servo(180, 0, 1)
serv_2 = Servo.Servo(180, 0, 2)
serv_3 = Servo.Servo(180, 0, 3)
serv_4 = Servo.Servo(180, 0, 4)
serv_7 = Servo.Servo(180, 0, 7)
serv_8 = Servo.Servo(180, 0, 8)

async def do_commands(command, conn):
    name, *values = command.split(" ")
    if name == "Motor":
        Motor.MotorMove(int(values[0]), int(values[1]))
    if name == "Servo":
        serv_1.set(int(values[0]))
        serv_2.set(int(values[1]))
        serv_3.set(int(values[2]))
        serv_4.set(int(values[3]))

    if name == "Camera":
        serv_7.set(int(values[1]))
        serv_8.set(int(values[2]))

    if name == "GIVE_IR_R":
        await asyncio.to_thread(conn.sendall, str(cfg.IR_R).encode())
    if name == "GIVE_IR_M":
        await asyncio.to_thread(conn.sendall, str(cfg.IR_M).encode())
    if name == "GIVE_IR_L":
        await asyncio.to_thread(conn.sendall, str(cfg.IR_L).encode())
    if name == "GIVE_sonar":
        await asyncio.to_thread(conn.sendall, str(cfg.sonar).encode())
