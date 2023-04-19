#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from control.effects.abstract_effect import AbstractEffect
from control.adapter.abstract_matrix import AbstractColor, AbstractMatrix
from misc.utils import rotate
import settings

# TODO: Abstract options so that they can be specified for each effect

width: int = settings.MATRIX_DIMENSIONS.WIDTH.value
height: int = settings.MATRIX_DIMENSIONS.HEIGHT.value

def _data():
    data = []
    for col in range(width+1):
        if col == 0:
            data.append((25,25,25))
        if col == 1:
            data.append((50,50,50))
        if col == 2:
            data.append((128,128,128))
        if col == 3:
            data.append((255,255,255))
        else:
            data.append((0,0,0))
    print(len(data))
    return data

class Wave(AbstractEffect):
    @staticmethod
    def default(matrix: AbstractMatrix):
        base_offset = 1
        data = _data()
        matrix.Clear()
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        while 1:
            for xx,colors in enumerate(data):
                matrix.graphics.DrawLine(canvas, xx,0,xx,height,matrix.graphics.Color(colors[0],colors[1],colors[2]))
            canvas = matrix.SwapOnVSync(canvas)
            data = rotate(data,base_offset)
            time.sleep(0.001)


    @staticmethod
    def run(matrix_class_name: AbstractMatrix, mode="default"):
        matrix = matrix_class_name(options=settings.rgb_options())
        if mode == "default":
            Wave.default(matrix)
