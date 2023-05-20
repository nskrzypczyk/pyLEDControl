import os
import time
import random
import settings
import datetime
from misc.logging import Log
from control.adapter.abstract_matrix import AbstractMatrix
from control.effect_message import EffectMessage
from control.effects.abstract_effect import AbstractEffect

log = Log("DigiClock")


class DigiClock(AbstractEffect):
    @staticmethod
    def run(matrix_class_name, msg: EffectMessage):
        matrix: AbstractMatrix = matrix_class_name(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        font = matrix.graphics.Font()
        font.LoadFont("../../rpi-rgb-led-matrix/fonts/7x13.bdf")
        refresh_rate = 1 / 24
        x = 5
        y = 10
        dx = 1
        dy = 1
        while True:
            br: int = msg.get_brightness()
            canvas.Clear()
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            text_width = sum([font.CharacterWidth(ord(char)) for char in current_time])
            text_height = font.height
            matrix.graphics.DrawText(
                canvas,
                font,
                x,
                y,
                matrix.graphics.Color(255 * br, 255 * br, 255 * br),
                current_time,
            )
            x += dx
            y += dy

            # Bounce off edges
            log.debug(f"text_height:{text_height}")
            log.debug(f"text_width:{text_width}")
            log.debug(f"y:{y}")
            log.debug(f"x:{x}")
            if (x <= 0) or (x + text_width >= 64):
                dx = -dx
            if (y <= 9) or (
                y + text_height >= 64 + text_height
            ):  # TODO: Remove magic numbers
                dy = -dy

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(refresh_rate)
