# -*- coding=utf-8 -*-

import time
from bindings.spotify_binding import SpotifyBinding
import settings
from misc.logging import Log
from control.effects.abstract_effect import AbstractEffect
from control.adapter.abstract_matrix import AbstractMatrix

log = Log("Spotify")


class Spotify(AbstractEffect):
    @staticmethod
    def run(matrix_class):
        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        font = matrix.graphics.Font()
        font.LoadFont("../../rpi-rgb-led-matrix/fonts/7x13.bdf")
        refresh_rate = 5
        counter = 0

        spotify = SpotifyBinding()

        while 1:
            log.debug("Hello")
            matrix.graphics.DrawText(
                canvas, font, 0, 10, matrix.graphics.Color(
                    255, 255, 255), "Test"
            )
            try:
                data = spotify.get()
            except:
                pass

            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(refresh_rate)
            counter += 1
