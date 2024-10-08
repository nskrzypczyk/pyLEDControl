# -*- coding=utf-8 -*-

import textwrap
import time

import settings
from bindings.spotify_binding import SpotifyBinding
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log
from PIL import Image

log = Log("Spotify")
height = settings.MATRIX_DIMENSIONS.HEIGHT.value
width = settings.MATRIX_DIMENSIONS.WIDTH.value


class Spotify(AbstractEffect):

    @staticmethod
    def run(matrix_class, options, conn, *args, **kwargs):
        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        font = matrix.graphics.Font()
        font.LoadFont("../../rpi-rgb-led-matrix/fonts/6x9.bdf")
        refresh_rate = 5
        counter = 0

        spotify = SpotifyBinding()

        while not Spotify.is_terminated(conn):
            br = options.get_brightness()
            color = 255 * br
            color_text = matrix.graphics.Color(color, color, color)
            try:
                data = spotify.get()
                if counter < 5:
                    if hasattr(data, "album_art_url"):
                        matrix.SetImageFromURL(data.album_art_url, br)
                    else:
                        canvas.Clear()
                        matrix.graphics.DrawText(
                            canvas, font, 0, 10, color_text, "No playback"
                        )
                        canvas = matrix.SwapOnVSync(canvas)
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
                            color_text,
                            line,
                        )
                        y += 10
                    canvas = matrix.SwapOnVSync(canvas)
                else:
                    counter = 0
            except Exception as e:
                log.error(e, exc_info=e)
            time.sleep(refresh_rate)
            counter += 1
