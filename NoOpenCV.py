import cv2
import mynumpy  as np

# Параметры
Ny, Nx = 10, 10  # Шаги сетки по вертикали и горизонтали
My, Mx = 3, 3  # Шаги поиска в ширину и высоту
N = 5  # Количество кадров для усреднения
threshold = 50  # Порог для обнаружения движения
min_area = 100  # Минимальная площадь для детекции движения

# Загрузка видео
path = '100.mp4'
cap = cv2.VideoCapture(path)

frame_buffer = []

# Чтение первых N кадров
for _ in range(N):
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_buffer.append(frame)

resize_width = 800
resize_height = 600

def merge_rectangles(rectangles, threshold=30):
    """ Объединение близко расположенных прямоугольников в один большой """
    if not rectangles:
        return []

    rectangles = sorted(rectangles, key=lambda r: (r[0], r[1]))
    merged = []
    current_rect = rectangles[0]

    for rect in rectangles[1:]:
        if (rect[0] <= current_rect[2] + threshold and
                rect[1] <= current_rect[3] + threshold and
                rect[2] >= current_rect[0] - threshold and
                rect[3] >= current_rect[1] - threshold):
            current_rect = (min(current_rect[0], rect[0]),
                            min(current_rect[1], rect[1]),
                            max(current_rect[2], rect[2]),
                            max(current_rect[3], rect[3]))
        else:
            merged.append(current_rect)
            current_rect = rect

    merged.append(current_rect)
    return merged

def process_frame(current_gray):
    avg_frame = np.mean(frame_buffer, axis=0)
    avg_frame = np.astype(avg_frame, 'uint8')
    diff = np.abs_diff(np.astype(current_gray, int), np.astype(avg_frame, int))
    return diff

while cap.isOpened():
    ret, current_frame = cap.read()
    if not ret:
        break

    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

    # Обработка текущего кадра
    diff = process_frame(current_gray)

    rectangles = []
    height, width = len(diff), len(diff[0])

    for y in range(0, height, Ny):
        for x in range(0, width, Nx):
            if diff[y][x] > threshold:
                min_x, max_x = x, x
                min_y, max_y = y, y

                for i in range(y, min(y + My * Ny, height), My):
                    for j in range(x, min(x + Mx * Nx, width), Mx):
                        if diff[i][j] > threshold:
                            min_x = min(min_x, j)
                            max_x = max(max_x, j)
                            min_y = min(min_y, i)
                            max_y = max(max_y, i)

                if (max_x - min_x) * (max_y - min_y) >= min_area:
                    rectangles.append((min_x, min_y, max_x, max_y))

    merged_rectangles = merge_rectangles(rectangles, threshold=30)

    for (x1, y1, x2, y2) in merged_rectangles:
        cv2.rectangle(current_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    resized_frame = cv2.resize(current_frame, (resize_width, resize_height))
    cv2.imshow('Video', resized_frame)

    frame_buffer.pop(0)
    frame_buffer.append(current_gray)

    if cv2.waitKey(40) == 27:
        break

cap.release()
cv2.destroyAllWindows()
