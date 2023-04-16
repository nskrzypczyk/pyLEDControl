#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from control.adapter.abstract_matrix import AbstractMatrix
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


class RealMatrix(RGBMatrix, AbstractMatrix):
    def __init__(self, options={}):
        super().__init__()
        self.graphics = graphics