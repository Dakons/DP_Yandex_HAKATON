# button_color.py

import cv2
import numpy as np

def detect_button_color(frame, button_coords):
    """
    Определение цвета кнопки в пределах рамки кнопки.
    frame: кадр изображения
    button_coords: координаты рамки, в которой находится кнопка (x1, y1, x2, y2)
    """
    # Извлекаем область кнопки
    x1, y1, x2, y2 = button_coords
    button_region = frame[int(y1):int(y2), int(x1):int(x2)]

    # Преобразуем область кнопки в цветовое пространство HSV
    hsv_button = cv2.cvtColor(button_region, cv2.COLOR_BGR2HSV)

    # Определяем пороговые значения для каждого цвета
    lower_green = np.array([35, 50, 50])
    upper_green = np.array([85, 255, 255])

    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])

    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    lower_purple = np.array([140, 50, 50])
    upper_purple = np.array([160, 255, 255])

    # Определяем маски для каждого цвета
    green_mask = cv2.inRange(hsv_button, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv_button, lower_blue, upper_blue)
    red_mask1 = cv2.inRange(hsv_button, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv_button, lower_red2, upper_red2)
    red_mask = red_mask1 | red_mask2  # Объединяем два диапазона для красного
    purple_mask = cv2.inRange(hsv_button, lower_purple, upper_purple)

    # Считаем количество пикселей каждого цвета
    green_pixels = cv2.countNonZero(green_mask)
    blue_pixels = cv2.countNonZero(blue_mask)
    red_pixels = cv2.countNonZero(red_mask)
    purple_pixels = cv2.countNonZero(purple_mask)

    # Определяем преобладающий цвет
    if green_pixels > max(blue_pixels, red_pixels, purple_pixels):
        return "green"
    elif blue_pixels > max(green_pixels, red_pixels, purple_pixels):
        return "blue"
    elif red_pixels > max(green_pixels, blue_pixels, purple_pixels):
        return "red"
    elif purple_pixels > max(green_pixels, blue_pixels, red_pixels):
        return "purple"
    else:
        return "undefined"
