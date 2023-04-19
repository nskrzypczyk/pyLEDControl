import os
import time
import random
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
        x = 5
        y=10
        dx = 1
        dy = 1
        while True:
            canvas.Clear()
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            text_width = sum([font.CharacterWidth(ord(char)) for char in current_time])
            text_height = font.height
            matrix.graphics.DrawText(
                canvas, font, x, y, matrix.graphics.Color(255, 255, 255), current_time)
            x += dx
            y += dy

            # Bounce off edges
            if x <= 0 or x + text_width >= 64:
                dx = -dx
            if y <= 0 or y + text_height >= 64+text_height:
                dy = -dy

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(0.9)
