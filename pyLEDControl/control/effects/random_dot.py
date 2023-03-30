from RGBMatrixEmulator import RGBMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log
import random
import time


class RandomDot(AbstractEffect):
    def build(self) -> AbstractEffect:
        self.log = Log(__class__.__name__)
        self.log.debug("Building the effect")
        return self

    def run(self, matrix: RGBMatrix):
        self.log.debug("Updating matrix")
        matrix.SetPixel(random.randint(0, 63), random.randint(
            0, 63), random.randint(0, 128), random.randint(0, 128), random.randint(0, 128))
        time.sleep(1)
