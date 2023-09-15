import random
import time

import settings
from control.effects.abstract_effect import AbstractEffect
from misc.utils import Generics
from RGBMatrixEmulator import RGBMatrix


class RandomDot(AbstractEffect):

    @staticmethod
    def run(matrix_class_name: RGBMatrix, options: Generics.T_EFFECT_OPTIONS, conn):
        matrix = matrix_class_name(options=settings.rgb_options())
        while not RandomDot.is_terminated(conn):
            br = options.get_brightness()
            matrix.SetPixel(
                random.randint(0, 63),
                random.randint(0, 63),
                int(random.randint(0, 128) * br),
                int(random.randint(0, 128) * br),
                int(random.randint(0, 128) * br),
            )
            time.sleep(0.0001)
