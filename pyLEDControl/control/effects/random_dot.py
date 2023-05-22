from RGBMatrixEmulator import RGBMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log
import random
import time
import settings
from control.effect_message import EffectMessage


class RandomDot(AbstractEffect):
    @staticmethod
    def run(matrix_class_name: RGBMatrix, msg: EffectMessage):
        matrix = matrix_class_name(options=settings.rgb_options())
        while True:
            br = msg.get_brightness()
            matrix.SetPixel(random.randint(0, 63), random.randint(
                0, 63), int(random.randint(0, 128)*br), int(random.randint(0, 128)*br), int(random.randint(0, 128)*br))
            time.sleep(0.0001)
