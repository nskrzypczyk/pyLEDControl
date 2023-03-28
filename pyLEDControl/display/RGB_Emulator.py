import settings
import sys
import time
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from misc.logging import Log
from control.effects.abstract_effect import AbstractEffect


class RgbEmulator():
    def __init__(self) -> None:
        self.effect: AbstractEffect = None
        self.log: Log = Log("RgbEmulator")

    def run(self):
        options = RGBMatrixOptions()
        options.pixel_size = 16
        options.pixel_style = "round"
        options.rows = settings.MATRIX_EMULATION.HEIGHT
        options.cols = settings.MATRIX_EMULATION.WIDTH
        matrix = RGBMatrix(options=options)
        while 1:
            try:
                matrix.Clear()
                if self.effect != None:
                    self.effect.run(matrix)
                else:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.log.debug("Terminating")


if __name__ == "__main__":
    matrix = RgbEmulator()

    def pixel(matrix: RGBMatrix):
        matrix.SetPixel(1, 1, 10, 20, 30)
    matrix.mode = pixel
    matrix.run()
