# -*- coding=utf-8 -*-

import textwrap
import time
from bindings.spotify_binding import SpotifyBinding
import settings
from misc.logging import Log
from control.effects.abstract_effect import AbstractEffect
from control.adapter.abstract_matrix import AbstractMatrix
from control.effect_message import EffectMessage
from PIL import Image
from io import BytesIO
import requests

log = Log("Spotify")
height = settings.MATRIX_DIMENSIONS.HEIGHT.value
width = settings.MATRIX_DIMENSIONS.WIDTH.value


class Spotify(AbstractEffect):
    @staticmethod
    def run(matrix_class, msg: EffectMessage):
        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        font = matrix.graphics.Font()
        font.LoadFont("../../rpi-rgb-led-matrix/fonts/6x9.bdf")
        refresh_rate = 5
        counter = 0

        spotify = SpotifyBinding()

        while 1:
            br = msg.get_brightness()
            color_text = 255 * br
            try:
                data = spotify.get()
                if counter < 5:
                    matrix.SetImageFromURL(data.album_art_url, br)
                    log.debug("Image set")

                elif counter < 9:
                    canvas.Clear()
                    lines = textwrap.wrap(
                        f"{data.artist}\n-\n{data.track_name}", width=int(64 / 6)
                    )
                    y = 10
                    for line in lines:
                        matrix.graphics.DrawText(
                            canvas,
                            font,
                            0,
                            y,
                            matrix.graphics.Color(
                                color_text, 255 * br, 255 * br),
                            line,
                        )
                        y += 10
                    canvas = matrix.SwapOnVSync(canvas)
                else:
                    counter = 0
            except Exception as e:
                log.error(e)
            time.sleep(refresh_rate)
            counter += 1
