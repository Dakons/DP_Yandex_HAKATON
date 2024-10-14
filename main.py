import DP_MotorMoveLibr as Motor
import time

i = 100
j = -100

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
        
    
    