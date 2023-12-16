from dataclasses import dataclass
import datetime
import time

import settings
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log


log = Log("Christmas")
class Christmas(AbstractEffect):

    @staticmethod
    def run(matrix_class_name, options, conn, *args, **kwargs):
        matrix: AbstractMatrix = matrix_class_name(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        font = matrix.graphics.Font()
        font.LoadFont("../../rpi-rgb-led-matrix/fonts/7x13.bdf")
        refresh_rate = 3 # seconds
        while not Christmas.is_terminated(conn):
            matrix.SetImageFromFile("display/christmas-tree.png",0,0,options.brightness)
            time.sleep(refresh_rate)