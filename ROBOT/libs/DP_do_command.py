import libs.DP_MotorMoveLibr as Motor
def do_command_RASP(name, values):
    pass
def do_command_PC(name, values):
    if name == "motor":
        values = list(map(int, values))
        Motor.MotorMove(values[0], values[1])