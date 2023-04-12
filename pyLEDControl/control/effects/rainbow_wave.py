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

# FIXME: Implement options

log = Log("RainbowWave")
max_width = settings.MATRIX_EMULATION.WIDTH.value-1
max_height = settings.MATRIX_EMULATION.HEIGHT.value-1


class RainbowWave(AbstractEffect):
    rainbow = []
    for i in range(128):
        hue = 0 + i*(1/128)
        r, g, b = [int(255 * c)
                   for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
        rainbow.append((r, g, b))

    @dataclass
    class EffectOptions():

        mode: Literal["left to right",
                      "top left to bottom right"] = "top left to bottom right"

    default_options: EffectOptions = EffectOptions()

    @staticmethod
    def left_to_right(matrix: AbstractMatrix):
        rainbow = RainbowWave.rainbow
        matrix.Clear()
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        base_offset = 1
        while 1:
            for x in range(max_width+1):
                [canvas.SetPixel(x, y, rainbow[x][0], rainbow[x][1],
                                 rainbow[x][2]) for y in range(max_height+1)]

            time.sleep(0.005)
            canvas = matrix.SwapOnVSync(canvas)
            rainbow = rotate(rainbow, base_offset)

    @staticmethod
    def top_left_to_bottom_right(matrix: AbstractMatrix):
        rainbow = RainbowWave.rainbow
        matrix.Clear()
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        base_offset = 1
        while 1:
            counter = 1
            for x in range(max_width+1):
                base_x = x
                base_y = 0
                while base_x > -1 and base_y <= max_height:
                    canvas.SetPixel(
                        base_x, base_y, rainbow[x][0], rainbow[x][1], rainbow[x][2])
                    base_x -= 1
                    base_y += 1

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

    @staticmethod
    def run(matrix: AbstractMatrix, options: EffectOptions = default_options):
        if options.mode == "left to right":
            RainbowWave.left_to_right(matrix)
        elif options.mode == "top left to bottom right":
            RainbowWave.top_left_to_bottom_right(matrix)
