#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
import os
import settings
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect


def _print_field(
        field: list, matrix: AbstractMatrix, canvas: AbstractMatrix, br: int
):
    for x in range(settings.MATRIX_DIMENSIONS.HEIGHT.value):
        for y in range(settings.MATRIX_DIMENSIONS.HEIGHT.value):
            if field[x][y] == 1:
                canvas.SetPixel(
                    x,
                    y,
                    255 * br,
                    255 * br,
                    255 * br,
                )
            else:
                canvas.SetPixel(
                    x,
                    y,
                    0,
                    0,
                    0,
                )
    canvas = matrix.SwapOnVSync(canvas)


class GameOfLife(AbstractEffect):
    @staticmethod
    def run(matrix_class, options, conn, *args, **kwargs):
        c_lib = ctypes.CDLL(f"c_libs/{str(os.path.basename(__file__)).replace('.py', '.so')}")
        c_lib.create_grid.argtypes = [ctypes.c_int, ctypes.c_int]
        c_lib.create_grid.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

        c_lib.free_grid.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.c_int]

        c_lib.update_grid.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.c_int, ctypes.c_int]
        c_lib.update_grid.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()

        rows = settings.rgb_options().rows
        cols = settings.rgb_options().cols

        current_grid = c_lib.create_grid(rows, cols)

        counter = 0
        br = options.get_brightness()
        while not GameOfLife.is_terminated(conn):
            if counter == 10:
                br = options.get_brightness()
                counter = 0
            new_grid = c_lib.update_grid(current_grid, rows, cols)
            c_lib.free_grid(current_grid, rows)
            current_grid = new_grid

            _print_field(current_grid, matrix, canvas, br)

            counter += 1
