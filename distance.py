import cv2 as cv
import os

# мой логгер
from log_client import *


# модуль, который получает капчу и отправляет расстояние, на которое нужно передвинуть пазлу

# Получение расстояния
def get_distance(captcha_bytes):

    # создаем файл
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img.png")
    with open(path, "wb") as file:
        file.write(captcha_bytes)
    file.close()

    # читаем файл
    captcha = cv.imread(path, flags=-5)

    # удаляем файл
    os.remove(path)

    # Раземры для детальки [1]
    width_puzzle, height_puzzle = 60, 192
    x_puzzle, y_puzzle = 0, 0

    # Размеры для фона [1]
    width_area, height_area = 310, 192
    x_area, y_area = 60, 0

    # Кадрирование детальки [2]
    puzzle = captcha[y_puzzle: y_puzzle + height_puzzle,
                     x_puzzle: x_puzzle + width_puzzle]

    # Кадрирование фона [2]
    area = captcha[y_area: y_area + height_area, x_area: x_area + width_area]

    # Определение контура детальки
    puzzle_gr = cv.cvtColor(puzzle, cv.COLOR_BGR2GRAY)
    puzzle_bl = cv.medianBlur(puzzle_gr, 1)
    puzzle_canny = cv.Canny(puzzle_bl, 800, 450) # [3]

    # Определение контура фона
    area_gr = cv.cvtColor(area, cv.COLOR_BGR2GRAY)
    area_bl = cv.medianBlur(area_gr, 1)
    area_canny = cv.Canny(area_bl, 200, 500) # [3]

    # Получение размеров детальки и фона
    img = area_canny
    template = puzzle_canny

    # Выбираем метод [3]
    method = cv.TM_CCOEFF

    # Применяем метод нахождение одинаковых объектов
    res = cv.matchTemplate(img, template, method)
    _, _, _, max_loc = cv.minMaxLoc(res)

    # max_loc[0] - это расстояние в пикселях по оси Х
    distance = str(max_loc[0])
    logger_cli(level=0, message='обработка капчи завершена. Расстояние: ' + distance, on=0)
    return distance
