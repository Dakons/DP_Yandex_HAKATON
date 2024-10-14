import DP_MotorMoveLibr as Motor
import DP_LED as LED
import time

i = 100
j = -100

LED.open_light()

while 1:
    Motor.MotorMove(100,-100)
    time.sleep(5)
    Motor.MotorMove(-100, 100)
    time.sleep(5)
    while i > -99:
        i-=1
        j+=1
        Motor.MotorMove(i, j)
        time.sleep(0.05)

LED.close_light()    
    
    