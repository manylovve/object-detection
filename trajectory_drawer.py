import numpy as np
import cv2
from Geometry import Geometry

class TrajectoryDrawer:
    def __init__(self, memory_size: int = 100, color_generator=lambda x: (0, 255, 0)):
        self.memory_size = memory_size
        self.history = {}  # {id: [...последние N позиций...]}
        self.frame_counter = {}
        self.color_generator = color_generator

    def draw(self, frame, figures):
        '''Рисует траектории фигур по их положениям в кадрах.'''

        for id, figure in figures:
            self.history.setdefault(id, np.array(Geometry.get_center(figure), ndmin=2))
            self.history[id] = np.append(self.history[id], [Geometry.get_center(figure)], axis=0)

        to_del = []
        for id in self.history:
            for i in range(len(self.history[id]) - 1):
                alpha = (i + 1) / len(self.history[id])  # коэффициент для плавности линии
                thickness = 2 + int(6 * alpha)  # сделаем линии значительно толще
                color = tuple([int(c * (1 - alpha)) for c in self.color_generator(id)])  # плавный переход цвета
                frame = cv2.line(frame,
                                 tuple(self.history[id][i]),
                                 tuple(self.history[id][i + 1]),
                                 color=color,
                                 thickness=thickness)
            self.frame_counter[id] = self.frame_counter.get(id, 0) + 1
            if self.frame_counter[id] >= self.memory_size:
                self.history[id] = self.history[id][1:]
                if not len(self.history[id]):
                    to_del.append(id)

        for id in to_del:
            del self.history[id]
            del self.frame_counter[id]

        return frame
