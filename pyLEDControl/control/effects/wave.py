#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from RGBMatrixEmulator import RGBMatrix
from control.effects.abstract_effect import AbstractEffect
import settings

# TODO: Abstract options so that they can be specified for each effect


class Wave(AbstractEffect):
    @staticmethod
    def default(matrix: RGBMatrix):
        width: int = settings.MATRIX_EMULATION.WIDTH.value
        height: int = settings.MATRIX_EMULATION.HEIGHT.value
        offset_canvas = matrix.CreateFrameCanvas()
        while 1:
            for col in range(width):
                for row in range(height):
                    offset_canvas.SetPixel(col, row, 255, 255, 255)
                if col > 0:
                    for row in range(height):
                        offset_canvas.SetPixel(col-1, row, 128, 128, 128)
                if col > 1:
                    for row in range(height):
                        offset_canvas.SetPixel(col-2, row, 50, 50, 50)
                if col > 2:
                    for row in range(height):
                        offset_canvas.SetPixel(col-3, row, 0, 0, 0)
                offset_canvas = matrix.SwapOnVSync(offset_canvas)
            matrix.Clear()

    @staticmethod
    def run(matrix: RGBMatrix, mode="default"):
        matrix.Clear()
        if mode == "default":
            Wave.default(matrix)
