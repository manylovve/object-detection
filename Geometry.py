class Geometry:
    @staticmethod
    def get_center(rect):
        x1, y1, x2, y2 = rect
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    @staticmethod
    def merge_rectangles(rectangles, threshold):
        """ Объединение близко расположенных прямоугольников """
        if len(rectangles) == 0:
            return []

        # Сортируем прямоугольники по координатам
        rectangles = sorted(rectangles, key=lambda r: r[0])

        merged_rectangles = []
        current_rect = rectangles[0]

        for rect in rectangles[1:]:
            # Проверяем, пересекаются ли прямоугольники или находятся близко друг к другу
            if (rect[0] <= current_rect[2] + threshold and
                    rect[1] <= current_rect[3] + threshold and
                    rect[2] >= current_rect[0] - threshold and
                    rect[3] >= current_rect[1] - threshold):
                # Объединяем прямоугольники
                current_rect = (min(current_rect[0], rect[0]),
                                min(current_rect[1], rect[1]),
                                max(current_rect[2], rect[2]),
                                max(current_rect[3], rect[3]))
            else:
                merged_rectangles.append(current_rect)
                current_rect = rect

        merged_rectangles.append(current_rect)
        return merged_rectangles
