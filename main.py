import cv2
import numpy as np
from Geometry import Geometry
from trajectory_drawer import TrajectoryDrawer

# Загрузка видео
path = '100.mp4'  # Путь к видеофайлу
cap = cv2.VideoCapture(path)

if not cap.isOpened():
    print("Не удалось открыть видео.")
    exit()

# Чтение первого кадра
ret, frame1 = cap.read()
if not ret:
    print("Не удалось прочитать первый кадр.")
    cap.release()
    exit()

# Преобразование в оттенки серого
prev_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

# Размер для изменения (ширина, высота)
resize_width = 800
resize_height = 600

min_area = 300  # Порог минимальной площади детекции
trajectory_drawer = TrajectoryDrawer()  # Создаем экземпляр класса TrajectoryDrawer
object_id = 0  # Идентификатор для объектов

while cap.isOpened():
    ret, frame2 = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Вычисление разницы между двумя кадрами
    diff = cv2.absdiff(prev_gray, gray)

    # Применение размытия для снижения шума
    blur = cv2.GaussianBlur(diff, (7, 7), 0)

    # Применение порогового преобразования для выделения движущихся объектов
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

    # Расширение (dilation) для заполнения пробелов в движущихся объектах
    dilated = cv2.dilate(thresh, None, iterations=3)

    # Поиск контуров движущихся объектов
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    rectangles = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) >= min_area:
            rectangles.append((x, y, x + w, y + h))

    # Объединение близко расположенных прямоугольников
    merged_rectangles = Geometry.merge_rectangles(rectangles, threshold=30)

    # Подготовка списка фигур для отрисовки траекторий
    figures = []
    for rect in merged_rectangles:
        figures.append((object_id, rect))
        object_id += 1

    # Рисуем траектории объектов на текущем кадре
    frame_with_traj = trajectory_drawer.draw(frame2.copy(), figures)

    # Рисуем объединенные прямоугольники
    for (x1, y1, x2, y2) in merged_rectangles:
        cv2.rectangle(frame_with_traj, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Изменение размера кадра
    resized_frame = cv2.resize(frame_with_traj, (resize_width, resize_height))

    # Отображение измененного кадра
    cv2.imshow('Video with Trajectories', resized_frame)

    # Обновление предыдущего кадра
    prev_gray = gray.copy()

    # Переход к следующему кадру
    frame1 = frame2

    # Прерывание цикла при нажатии клавиши 'Esc'
    if cv2.waitKey(40) == 27:
        break

cap.release()
cv2.destroyAllWindows()
