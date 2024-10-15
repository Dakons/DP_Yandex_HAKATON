from collections import deque
import numpy as np

class Filter:
    def __init__(self, median_window_size, moving_average_alpha):
        """
        Инициализация фильтра с медианным фильтром и скользящим средним.
        
        :param median_window_size: размер окна для медианного фильтра
        :param moving_average_alpha: коэффициент сглаживания для экспоненциального скользящего среднего (0 < alpha <= 1)
        """
        self.median_window_size = median_window_size
        self.moving_average_alpha = moving_average_alpha
        self.median_data = deque(maxlen=median_window_size)
        self.moving_average_value = None

    def filter(self, new_value):
        """
        Фильтрация нового значения через медианный фильтр и экспоненциальное скользящее среднее.
        
        :param new_value: новое поступающее значение
        :return: значение, отфильтрованное через медианный фильтр и скользящее среднее
        """
        # Добавляем новое значение в медианный фильтр
        self.median_data.append(new_value)
        median_filtered = np.median(self.median_data)

        # Применяем экспоненциальное скользящее среднее
        if self.moving_average_value is None:
            # Инициализируем значение для скользящего среднего
            self.moving_average_value = median_filtered
        else:
            # Сглаживание
            self.moving_average_value = (
                self.moving_average_alpha * median_filtered +
                (1 - self.moving_average_alpha) * self.moving_average_value
            )
        
        return self.moving_average_value

