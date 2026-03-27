#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes
import os
import settings
import numpy as np
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from PIL import Image

'''
This effect simulates the "digital rain" from the Matrix movies. 
The main logic is implemented in C for performance reasons, while the Python code handles the integration with the LED matrix and effect management.
This was primarily implemented as a demonstration of how to integrate C code for performance-critical effects.
'''

def _print_field(field, matrix: AbstractMatrix, canvas: AbstractMatrix, br: int):
    img = Image.fromarray(field, 'RGB')
    canvas.SetImage(img)
    canvas = matrix.SwapOnVSync(canvas)


class DigitalRain(AbstractEffect):

    @staticmethod
    def run(matrix_class, options, conn, *args, **kwargs):
        rows = settings.rgb_options().rows
        cols = settings.rgb_options().cols

        clib = ctypes.CDLL(
            f"c_libs/{str(os.path.basename(__file__)).replace('.py', '.so')}")

        clib.step.argtypes = [ctypes.POINTER(ctypes.c_uint8)]

        # State array (for C library)
        field = np.zeros((rows, cols, 3), dtype=np.uint8)

        # Pointer on the state (for C library)
        field_ptr = field.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))

        clib.init()

        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()

        counter = 0
        br = options.get_brightness()
        while not DigitalRain.is_terminated(conn):
            if counter == 10:
                br = options.get_brightness()
                counter = 0
            clib.step(field_ptr)
            _print_field(field, matrix, canvas, br)
            counter += 1
