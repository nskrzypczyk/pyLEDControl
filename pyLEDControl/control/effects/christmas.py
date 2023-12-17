from dataclasses import dataclass
import random
import time
from settings import MATRIX_DIMENSIONS as MD

import settings
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log


MAX_WIDTH = MD.WIDTH.value
MAX_HEIGHT = MD.HEIGHT.value

@dataclass
class Color():
    r:int
    g:int
    b:int

    def white(matrix:AbstractMatrix, brightness):
        return Color(255*brightness,255*brightness,255*brightness)

log = Log("Christmas")
class Christmas(AbstractEffect):

    @staticmethod
    def run(matrix_class_name, options, conn, *args, **kwargs):
        matrix: AbstractMatrix = matrix_class_name(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        font = matrix.graphics.Font()
        font.LoadFont("../../rpi-rgb-led-matrix/fonts/7x13.bdf")
        refresh_rate = 0.8 # seconds
        while not Christmas.is_terminated(conn):
            matrix.SetImageFromFile("display/christmas-tree.png",0,0,options.get_brightness())
            color: Color = Color.white(matrix, options.get_brightness())
            for i in range(12):
                x,y = MAX_WIDTH, MAX_HEIGHT
                while(x>MAX_WIDTH-1 or y>MAX_HEIGHT-1):
                    x,y = (random.randrange(64) for _ in range(2))
                matrix.SetPixel(x,y,color.r, color.g, color.b)
                matrix.SetPixel(x+1,y+1,color.r, color.g, color.b)
                matrix.SetPixel(x+1,y,color.r, color.g, color.b)
                matrix.SetPixel(x,y+1,color.r, color.g, color.b)
                
            time.sleep(refresh_rate)