from RGBMatrixEmulator import RGBMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log
import random
import time

import settings


class RandomDot(AbstractEffect):
    @staticmethod
    def run(matrix_class_name: RGBMatrix):
        matrix = matrix_class_name(options=settings.rgb_options())
        while True:
            matrix.SetPixel(random.randint(0, 63), random.randint(
                0, 63), random.randint(0, 128), random.randint(0, 128), random.randint(0, 128))
            time.sleep(0.0001)
