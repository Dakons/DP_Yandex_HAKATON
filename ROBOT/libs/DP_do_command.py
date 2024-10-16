import sys
import os

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

import libs.DP_MotorMoveLibr as Motor
def do_command_RASP(name, values):
    pass
def do_command_PC(name, values):
    if name == "motor":
        values = list(map(int, values))
        Motor.MotorMove(values[0], values[1])