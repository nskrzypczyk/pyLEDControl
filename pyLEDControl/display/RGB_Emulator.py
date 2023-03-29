import settings
import sys
import time
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
from misc.logging import Log
from control.led_service import LedService
from multiprocessing import Process


class RgbEmulator():
    def __init__(self) -> None:
        self.log: Log = Log("RgbEmulator")

    def loop(self, matrix, led_service: LedService):
        while 1:
            try:
                if led_service.effect != None:
                    led_service.effect.run(matrix)
                else:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.log.debug("Terminating")

    def run(self, led_service: LedService):
        options = RGBMatrixOptions()
        options.pixel_size = 16
        options.pixel_style = "round"
        options.rows = settings.MATRIX_EMULATION.HEIGHT.value
        options.cols = settings.MATRIX_EMULATION.WIDTH.value
        matrix = RGBMatrix(options=options)
        self.loop(led_service)


if __name__ == "__main__":
    matrix = RgbEmulator()

    def pixel(matrix: RGBMatrix):
        matrix.SetPixel(1, 1, 10, 20, 30)
    matrix.mode = pixel
    matrix.run()
