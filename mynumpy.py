def mean(arrays, axis=0):
    """
    Вычисление среднего значения по заданной оси.
    """
    if axis == 0:
        height = len(arrays[0])
        width = len(arrays[0][0])

        # Создание массива для хранения среднего значения
        avg_frame = [[0.0] * width for _ in range(height)]

        # Суммирование значений
        for y in range(height):
            for x in range(width):
                total = sum(float(arr[y][x]) for arr in arrays)
                avg_frame[y][x] = total / len(arrays)

        # Приведение результата к целочисленному типу и ограничение диапазона значений
        return [[max(0, min(255, int(round(pixel)))) for pixel in row] for row in avg_frame]
    else:
        raise ValueError("Поддерживается только axis=0")


def abs_diff(arr1, arr2):
    """
    Вычисление абсолютной разности между двумя массивами.
    """
    height = len(arr1)
    width = len(arr1[0])
    diff = [[0] * width for _ in range(height)]

    for y in range(height):
        for x in range(width):
            diff[y][x] = abs(arr1[y][x] - arr2[y][x])

    return diff


def astype(arr, dtype):
    """
    Приведение массива к другому типу.
    """
    if dtype == int:
        return [[int(pixel) for pixel in row] for row in arr]
    elif dtype == 'uint8':
        return [[max(0, min(255, int(pixel))) for pixel in row] for row in arr]
    else:
        raise ValueError("Неизвестный тип данных")
