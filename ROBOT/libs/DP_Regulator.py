class PIDRegulator:
    def __init__(self, Kp: float, Ki: float, Kd: float, output_min: float = -100.0, output_max: float = 100.0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.regulate_error = 0.0
        self.integral = 0.0
        self.last_error = 0.0
        self.output_min = output_min  # Минимальное значение выходного сигнала
        self.output_max = output_max  # Максимальное значение выходного сигнала

    def regulate(self, data: float, state: float) -> float:
        # Вычисляем текущую ошибку
        self.regulate_error = state - data
        
        # Пропорциональная составляющая
        P = self.Kp * self.regulate_error
        
        # Интегральная составляющая
        self.integral += self.Ki * self.regulate_error
        
        # Дифференциальная составляющая
        D = self.Kd * (self.regulate_error - self.last_error)
        self.last_error = self.regulate_error  # Обновляем последнюю ошибку
        
        # PID-выход
        PID_output = P + self.integral + D
        
        # Линейная интерполяция для ограничения выходного сигнала
        PID_output = self.linear_interpolate(PID_output)
        
        return PID_output

    def linear_interpolate(self, value: float) -> float:
        """Ограничивает значение в заданных пределах."""
        if value < self.output_min:
            return self.output_min
        elif value > self.output_max:
            return self.output_max
        else:
            return value
