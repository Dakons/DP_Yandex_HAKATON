import sys
import os

# Получаем путь к директории ROBOT
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Добавляем libs в sys.path
sys.path.append(parent_dir)

# Импортируем модуль и используем псевдоним
import libs.DP_Regulator as Regulator

def main():
    # Создание экземпляра регулятора
    move_val = Regulator.PIDRegulator(Kp=1, Ki=0, Kd=0)
    print("Регулятор создан с Kp:", move_val.Kp)

if __name__ == '__main__':
    main()
