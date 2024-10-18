import sys
import os
import time
import threading

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from libs.DP_Regulator import PIDRegulator
from libs.DP_Filter import Filter
import libs.DP_sonar as Ultrasonic
import libs.DP_MotorMoveLibr as Motor
from libs.DP_teleplot import TelemetrySender
from libs.DP_servo import Servo
import libs.DP_MotorMovements as Movement

# Константы
BAZASPEED = 75
SONAR_OFFSET = -4  # Поправка в сантиметрах для датчика, установленного сбоку

# Инициализация компонентов
MoveData = TelemetrySender()
sonServo = Servo(ANGLE_MAX=180, ANGLE_MIN=0, servonum=7)
sonServo.set(90)
Filter_sonar = Filter(5, 0.3)
pid_output = 0.0
pid_output_semaphore = threading.Semaphore(1)  # Создаем семафор для pid_output


def telemetry_and_regulator(VectorRegulator, setpoint, telemetry_active, side):
    """Мониторинг, вычисление воздействия PID и отправка данных телеметрии."""
    global pid_output  # Объявляем переменную как глобальную
    while telemetry_active.is_set():
        distance = Ultrasonic.get_distance()
        
        # Применяем фильтр к данным с датчика
        distance_filtered = round(Filter_sonar.filter(distance))
        
        # Корректируем расстояние в зависимости от стороны установки датчика
        if side == 'LEFT':
            distance_filtered += SONAR_OFFSET  # Если слева, отнимаем поправку
        elif side == 'RIGHT':
            distance_filtered -= SONAR_OFFSET  # Если справа, прибавляем поправку

        # Вычисляем воздействие PID
        pid_output_value = VectorRegulator.regulate(distance_filtered, setpoint)
        
        # Используем контекстный менеджер для безопасного доступа к pid_output
        with pid_output_semaphore:
            pid_output = pid_output_value  # Записываем значение в pid_output

        # Отправляем данные телеметрии
        MoveData.send_telemetry("Distance", distance_filtered)
        MoveData.send_telemetry("Error", VectorRegulator.regulate_error)
        MoveData.send_telemetry("Vector", pid_output)
        MoveData.send_telemetry("I", VectorRegulator.I)
        MoveData.send_telemetry("P", VectorRegulator.P)
        
        time.sleep(0.01)


def drive_along_wall(side, distance, setpoint, kp, ki, kd):
    telemetry_active = threading.Event()
    telemetry_active.set()
    
    VectorRegulator = PIDRegulator(Kp=kp, Ki=ki, Kd=kd, output_min=-20, output_max=20, i_buffer_size=200)
    
    if side == 'LEFT':
        sonServo.set(180)
    elif side == 'RIGHT':
        sonServo.set(0)
    
    # Запускаем поток для телеметрии и PID регулирования
    telemetry_thread = threading.Thread(target=telemetry_and_regulator, args=(VectorRegulator, setpoint, telemetry_active, side))
    telemetry_thread.start()

    start_time = time.time()
    drive_time = distance * 1  # Простое время для примера
    Movement.Smooth_line_Start(BAZASPEED, 0.01)

    while (time.time() - start_time) < drive_time:
        # Используем контекстный менеджер для безопасного чтения pid_output
        with pid_output_semaphore:
            current_pid_output = pid_output
        
        # Движение моторов на основе текущего pid_output
        if side == 'RIGHT':
            Motor.MotorMove(BAZASPEED - current_pid_output, BAZASPEED + current_pid_output)
        elif side == 'LEFT':
            Motor.MotorMove(BAZASPEED + current_pid_output, BAZASPEED - current_pid_output)

        time.sleep(0.01)  # Не блокируем поток слишком плотно

    Movement.Smooth_line_Stop(BAZASPEED, 0.01)
    telemetry_active.clear()
    telemetry_thread.join()
    Motor.MotorMove(0, 0)


def add_angle(added_angle: float, angleMove):
    if added_angle > 0:
        Motor.MotorMove(BAZASPEED, -BAZASPEED)
        added_angle = added_angle * 0.003
        added_angle = added_angle * 3.8
        print(added_angle)
        time.sleep(added_angle)
    else:
        Motor.MotorMove(-BAZASPEED, BAZASPEED)
        added_angle = -added_angle
        added_angle = added_angle * 0.003
        added_angle = added_angle * 3.8
        print(added_angle)
        time.sleep(added_angle)
    Motor.MotorMove(0, 0)