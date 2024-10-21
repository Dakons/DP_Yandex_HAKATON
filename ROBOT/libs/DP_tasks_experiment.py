import sys
import os
import time
#import threading
BAZASPEED = 75
SONAR_OFFSET = -4  # Поправка в сантиметрах для датчика, установленного сбоку
KP = 12
KI = -0.04
KD = 0
SPEEED = 38 #см в секунду
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
LineRegulator = PIDRegulator(Kp=KP, Ki=KI, Kd=KD, output_min=-20, output_max=20, i_buffer_size=240)
time.sleep(3)

def drive_along_wall(side, Distantion, setpoint):
    Duration = round(((Distantion - 40)/SPEEED),2)
    LineRegulator = PIDRegulator(Kp=KP, Ki=KI, Kd=KD, output_min=-20, output_max=20, i_buffer_size=240)  
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

        if Dist_filtered <= 10:
            LineRegulator.Ki = 0
        else:
            LineRegulator.Ki = KI
        
        current_pid_output = LineRegulator.regulate(Dist_filtered, setpoint)
        
        if side == "RIGHT":
                
                Motor.MotorMove(BAZASPEED - current_pid_output, BAZASPEED + current_pid_output)
                print(f"RIGHT{Dist_filtered},{LineRegulator.I}")
        elif side == "LEFT":
                
                Motor.MotorMove(BAZASPEED + current_pid_output, BAZASPEED - current_pid_output)
                print(f"LEFT{Dist_filtered},{LineRegulator.I}")
        """
        print("Start send data")
        DataTeleplot.send_telemetry("DISTANTION", Dist_filtered)
        DataTeleplot.send_telemetry("Error", LineRegulator.regulate_error)
        DataTeleplot.send_telemetry("PID", current_pid_output)
        DataTeleplot.send_telemetry("I", LineRegulator.I)
        DataTeleplot.send_telemetry("P", LineRegulator.P)
        print("End send data")
        """
        if time.time() - FirstTime > Duration:
             print("Task Completed. timer is off")
             break
        #time.sleep(0.01)
    print("Smooth Stop started")
    Movement.Smooth_line_Stop(BAZASPEED, 0.01)
    Motor.MotorMove(0, 0)
    print("Motor Stopped")

def add_angle(added_angle):
    if (added_angle < 0):
        direction = "CLOCKWISE"
        added_angle = abs(added_angle)
    elif added_angle > 0:
        direction = "COUNTERCLOCKWISE"
    steps = added_angle//5  
    Movement.Add_bit_angle(BAZASPEED,direction,0.060,steps)

def drive_line(Distantion):
    USESPEED = BAZASPEED
    if Distantion < 0:
        USESPEED = -USESPEED
    if abs(Distantion) < 50:
        Duration = round(abs(Distantion)/(SPEEED*0.5),2)
        First_time = time.time()
    else:
        Duration = round(((Distantion - 40)/SPEEED),2)
        print (Duration)
        print("START Smooth start")
        Movement.Smooth_line_Start(USESPEED, 0.01)
        print("END Smooth start")
        First_time = time.time()
    while True:
        if Distantion < 50:
            Motor.MotorMove(USESPEED/2, USESPEED/2)
        else:
            Motor.MotorMove(BAZASPEED, BAZASPEED)
        if (time.time()-First_time)  > (Duration):
            print(time.time()-First_time)
            #print(time.time())
            break
    if Distantion >= 50:
        print("START Smooth stop")
        Movement.Smooth_line_Stop(BAZASPEED, 0.01)
        print("END Smooth stop")
    Motor.MotorMove(0, 0)

#NA 1\4 proyeszhayet > 25 vmesto 20
#for i in range(1):
 #   drive_line(10)
  #  time.sleep(1)
#drive_line(-10)

#Movement.Smooth_line_Start(BAZASPEED,0.01)
#drive_line(200)
#drive_along_wall(side ="LEFT", Distantion = 150, setpoint = 30)
#add_angle(-180)
#drive_along_wall(side ="RIGHT", Distantion = 100, setpoint = 60)
#add_angle(180)