from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
import settings
import datetime

class DigiClock(AbstractEffect):
    @staticmethod
    def run(matrix_class_name):
        matrix = matrix_class_name(options=settings.rgb_options())
        canvas:AbstractMatrix = matrix.CreateFrameCanvas()
        font = matrix.graphics.Font()
        font.LoadFont("")
        while True:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            matrix.graphics.DrawText(canvas,font,0,0,matrix.graphics.Color(255,255,255), current_time)