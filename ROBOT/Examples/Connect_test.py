import sys
import os

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

import time
import libs.DP_send_message as Command

Command.send_tcp_command_PC("motor", [12, 24])
Command.get_tcp_command_RASP()
time.sleep(5)
Command.send_tcp_command_PC("motor", [0, 0])
Command.get_tcp_command_RASP()

