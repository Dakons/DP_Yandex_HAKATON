import libs.DP_servo as Servo
serv_1 = Servo(180, 0, 1)
serv_2 = Servo(180, 0, 2)
serv_3 = Servo(180, 0, 3)
serv_4 = Servo(180, 0, 4)
def set_robohand_position(s_1_angle, s_2_angle, s_3_angle, s_4_angle):
    serv_1.set(s_1_angle)
    serv_2.set(s_2_angle)
    serv_3.set(s_3_angle)
    serv_4.set(s_4_angle)