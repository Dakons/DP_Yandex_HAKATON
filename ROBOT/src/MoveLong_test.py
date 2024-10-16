import sys
import os
import threading
import time
import libs.DP_tasks as Task
import libs.DP_MotorMoveLibr as Motor
import libs.DP_MotorMovements as Movement

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

# Флаг для управления завершением работы потока
sweep_running = True

def sweep_thread():
    global sweep_running
    while sweep_running:
        # Выполняем движение sweep в отдельном потоке
        Movement.sweep(5, 100, 0.1, "RIGHT")
        time.sleep(0.1)  # Это для того, чтобы предотвратить чрезмерно быструю итерацию цикла

# Основная программа
Motor.MotorMove(0, 0)
time.sleep(2)

# Запускаем поток для sweep
sweep_thread_instance = threading.Thread(target=sweep_thread)
sweep_thread_instance.start()

# Запускаем движение вдоль стены
Task.drive_along_wall(side="RIGHT", distance=30, setpoint=100, Kp=1, Ki=0, Kd=0)

# По окончании движения выключаем поток sweep
sweep_running = False

# Ждём завершения потока перед завершением программы
sweep_thread_instance.join()

# Остановка моторов
Motor.MotorMove(0, 0)
