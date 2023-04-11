#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import colorsys
import time
from misc.utils import rotate
import settings
from typing import Literal
from dataclasses import dataclass
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log

log = Log("RainbowWave")


class RainbowWave(AbstractEffect):

    @dataclass
    class EffectOptions():

        corner: Literal["lt", "rt", "lb", "rb"] = "lt"

    default_options: EffectOptions = EffectOptions("lt")

    @staticmethod
    def run(matrix: AbstractMatrix, options: EffectOptions = default_options):
        max_width = settings.MATRIX_EMULATION.WIDTH.value-1
        max_height = settings.MATRIX_EMULATION.HEIGHT.value-1
        rainbow = []
        for i in range(128):
            hue = 0 + i*(1/128)
            r, g, b = [int(255 * c)
                       for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
            rainbow.append((r, g, b))

        log.debug(f"Color list length: {len(rainbow)}")
        starting_point: tuple[int, int]  # (x,y)

        # FIXME: Implement options
        if options.corner == "lt":
            starting_point = (0, 0)
        elif options.corner == "rt":
            starting_point = (max_width, 0)
        elif options.corner == "rb":
            starting_point = (max_width, max_height)
        elif options.corner == "lb":
            starting_point = (0, max_height)

        matrix.Clear()
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        base_offset = 1
        while 1:
            for x in range(max_width+1):
                base_x = x
                base_y = 0
                while base_x > -1 and base_y <= max_height:
                    canvas.SetPixel(
                        base_x, base_y, rainbow[x][0], rainbow[x][1], rainbow[x][2])
                    base_x -= 1
                    base_y += 1
            counter = 1
            for x in range(max_width+1):
                base_x = x
                base_y = max_height
                while base_x <= max_width and base_y > -1:
                    canvas.SetPixel(
                        base_x, base_y, rainbow[max_height+counter][0], rainbow[max_height+counter][1], rainbow[max_height+counter][2])
                    base_x += 1
                    base_y -= 1
                counter += 1
            time.sleep(0.005)
            canvas = matrix.SwapOnVSync(canvas)
            rainbow = rotate(rainbow, base_offset)
