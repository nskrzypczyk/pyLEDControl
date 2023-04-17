import os
import time
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
import settings
import datetime


class DigiClock(AbstractEffect):
    @staticmethod
    def run(matrix_class_name):
        matrix: AbstractMatrix = matrix_class_name(
            options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        font = matrix.graphics.Font()
        font.LoadFont(
            "../../rpi-rgb-led-matrix/fonts/7x13.bdf")
        while True:
            canvas.Clear()
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            matrix.graphics.DrawText(
                canvas, font, 4, 30, matrix.graphics.Color(255, 255, 255), current_time)
            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(0.9)
