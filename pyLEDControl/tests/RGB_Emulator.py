import settings
import sys
import time
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from misc.logging import Log


class RgbEmulator():
    def __init__(self) -> None:
        self.mode: callable = None
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
                if self.mode != None:
                    self.mode(matrix)
                time.sleep(1)
            except KeyboardInterrupt:
                self.log.debug("Terminating")


if __name__ == "__main__":
    matrix = RgbEmulator()

    def pixel(matrix: RGBMatrix):
        matrix.SetPixel(1, 1, 10, 20, 30)
    matrix.mode = pixel
    matrix.run()
