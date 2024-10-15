import time  # Импортируем модуль для работы со временем
import libs.DP_infrared as infrared
while True:
    if (infrared.Get_IR_M()):
        print("Спереди")
    if (infrared.Get_IR_L()):
        print("Слева")
    if (infrared.Get_IR_R()):
        print("Справа")
    time.sleep(1)



