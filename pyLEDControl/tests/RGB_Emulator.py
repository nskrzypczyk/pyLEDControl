import sys
import time
from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

class RGB_Emulator():
    def __init__(self) -> None:
        self.mode:callable = None

    def run(self):
        options = RGBMatrixOptions()
        options.pixel_size=16
        options.pixel_style="round"
        options.rows=64
        options.cols=128
        matrix= RGBMatrix(options=options)
        while 1:
            try:
                matrix.Clear()
                if self.mode != None: self.mode(matrix) 
                time.sleep(1)
            except KeyboardInterrupt:
                print("Exiting\n")
                sys.exit(0)

if __name__ == "__main__":
    matrix = RGB_Emulator()
    def pixel(matrix:RGBMatrix):
        matrix.SetPixel(1,1,10,20,30)
    matrix.mode=pixel
    matrix.run()