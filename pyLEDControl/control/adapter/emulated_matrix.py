#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from RGBMatrixEmulator import RGBMatrix, graphics
from control.adapter.abstract_matrix import AbstractMatrix


class EmulatedMatrix(RGBMatrix, AbstractMatrix):
    def __init__(self, options={}):
        super().__init__(options)
        self.graphics = graphics
