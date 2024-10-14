import DP_MotorMoveLibr as Motor  # Импортируем библиотеку для управления моторами
import time  # Импортируем модуль для работы со временем
import DP_servo as servo  # Импортируем библиотеку для управления сервоприводами

speed_left = -100
speed_right = 100


Motor.MotorMove(0, 0)
time.sleep(3)
#to ride back need ride more up duration 10%
#1.5 sec to do 360 degrees
Motor.MotorMove(speed_left, speed_right)
time.sleep(1.5)
Motor.MotorMove(speed_right, speed_right)
time.sleep(1)


#
#servo_controller = servo.Servo()  # Создаем объект управления сервоприводами

#servo_controller.set(servonum=2, servoangle=70)  # Устанавливаем угол в 90 градусов


