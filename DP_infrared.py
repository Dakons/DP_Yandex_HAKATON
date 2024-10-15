import DP_GPIO as gpio


class Infrared(object):
    def __init__(self):
        pass
    def Get_IR_M(self):
        return(gpio.IR_M)
    def Get_IR_L(self):
        return(gpio.IR_L)
    def Get_IR_R(self):
        return(gpio.IR_R)