import sys
import os
import time
#import threading
BAZASPEED = 75
SONAR_OFFSET = -4  # Поправка в сантиметрах для датчика, установленного сбоку
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


DataTeleplot = TelemetrySender()
SonarFilter = Filter(5, 0.3)

sonarServo = Servo(ANGLE_MAX=180, ANGLE_MIN=0, servonum=7)
sonarServo.set(90)
LineRegulator = PIDRegulator(Kp=12, Ki=-0.04, Kd=0, output_min=-20, output_max=20, i_buffer_size=200)
time.sleep(3)

def drive_along_wall(side, Duration, setpoint, kp, ki, kd):
    
    if side == 'LEFT':
        sonarServo.set(180)
    elif side == 'RIGHT':
        sonarServo.set(0)
    
    current_pid_output = 0
    FirstTime = time.time()
    Movement.Smooth_line_Start(BAZASPEED, 0.01) 

    while True:
        Dist = Ultrasonic.get_distance()

        
        Dist_filtered = round(SonarFilter.filter(Dist))

        if side == 'LEFT':
            Dist_filtered += SONAR_OFFSET  # Если слева, отнимаем поправку
        elif side == 'RIGHT':
            Dist_filtered -= SONAR_OFFSET  # Если справа, прибавляем поправку

        current_pid_output = LineRegulator.regulate(Dist_filtered, setpoint)
        
        if side == "RIGHT":
                
                Motor.MotorMove(BAZASPEED - current_pid_output, BAZASPEED + current_pid_output)
                print("RIGHT")
        elif side == "LEFT":
                
                Motor.MotorMove(BAZASPEED + current_pid_output, BAZASPEED - current_pid_output)
                print("LEFT")

        print("Start send data")
        DataTeleplot.send_telemetry("DISTANTION", Dist_filtered)
        DataTeleplot.send_telemetry("Error", LineRegulator.regulate_error)
        DataTeleplot.send_telemetry("PID", current_pid_output)
        DataTeleplot.send_telemetry("I", LineRegulator.I)
        DataTeleplot.send_telemetry("P", LineRegulator.P)
        print("End send data")
        if time.time() - FirstTime > Duration:
             print("Task Completed. timer is off")
             break
        #time.sleep(0.01)
    print("Smooth Stop started")
    Movement.Smooth_line_Stop(BAZASPEED, 0.01)
    Motor.MotorMove(0, 0)
    print("Motor Stopped")

def add_angle(added_angle: float):
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


def drive_line(Duration):
    print("START Smooth start")
    Movement.Smooth_line_Start(BAZASPEED, 0.01)
    print("END Smooth start")
    First_time = time.time()
    while True:
        Motor.MotorMove(BAZASPEED, BAZASPEED)
        if time.time() - First_time > (Duration - BAZASPEED * 0.02):
             break
    print("START Smooth stop")
    Movement.Smooth_line_Stop(BAZASPEED, 0.01)
    print("END Smooth stop")
    Motor.MotorMove(0, 0)

drive_along_wall(side ="LEFT", Duration = 5, setpoint = 50, kp = 12, ki = -0.04, kd = 0)
Motor.MotorMove(0, 0)
time.sleep(1)

add_angle(180)
Motor.MotorMove(0, 0)
time.sleep(1)

drive_along_wall(side ="RIGHT", Duration = 5, setpoint = 50, kp = 12, ki = -0.04, kd = 0)
Motor.MotorMove(0, 0)
time.sleep(1)

add_angle(180)
time.sleep(1)
Motor.MotorMove(0, 0)
    
