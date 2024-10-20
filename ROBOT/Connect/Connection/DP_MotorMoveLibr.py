import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

#import RPi.GPIO as GPIO
import DP_GPIO as gpio
from DP_teleplot import TelemetrySender

MoveData = TelemetrySender()

def MotorMove(M1SPEED, M2SPEED):
    
    if M1SPEED < -100:
        M1SPEED = -100
    if M2SPEED < -100:
        M2SPEED = -100
    if M2SPEED > 100:
        M2SPEED = 100
    if M1SPEED > 100:
        M1SPEED = 100
        
    #MoveData.send_telemetry("M1SPEED",M1SPEED)
    #MoveData.send_telemetry("M2SPEED",M2SPEED)
    # Управление первым мотором
    if M1SPEED < 0:  # Движение вперед
        gpio.digital_write(gpio.IN1, True)
        gpio.digital_write(gpio.IN2, False)
        gpio.ena_pwm(-M1SPEED)
    elif M1SPEED > 0:  # Движение назад
        gpio.digital_write(gpio.IN1, False)
        gpio.digital_write(gpio.IN2, True)
        gpio.ena_pwm(M1SPEED)
    elif M1SPEED == 0:  # Торможение мотора
        gpio.digital_write(gpio.IN1, True)
        gpio.digital_write(gpio.IN2, True)
        gpio.ena_pwm(0)

    # Управление вторым мотором
    if M2SPEED < 0:  # Движение вперед
        gpio.digital_write(gpio.IN3, True)
        gpio.digital_write(gpio.IN4, False)
        gpio.enb_pwm(-M2SPEED)
    elif M2SPEED > 0:  # Движение назад
        gpio.digital_write(gpio.IN3, False)
        gpio.digital_write(gpio.IN4, True)
        gpio.enb_pwm(M2SPEED)
    elif M2SPEED == 0:  # Торможение мотора
        gpio.digital_write(gpio.IN3, True)
        gpio.digital_write(gpio.IN4, True)
        gpio.enb_pwm(0)
