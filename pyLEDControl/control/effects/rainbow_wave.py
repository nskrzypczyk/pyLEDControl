#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import settings
from typing import Literal
from dataclasses import dataclass
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect


class RainbowWave(AbstractEffect):

    @dataclass
    class EffectOptions():

        corner: Literal["lt", "rt", "lb", "rb"] = "lt"

    default_options: EffectOptions = EffectOptions("lt")

    @staticmethod
    def run(matrix: AbstractMatrix, options: EffectOptions = default_options):
        max_width = settings.MATRIX_EMULATION.WIDTH.value-1
        max_height = settings.MATRIX_EMULATION.HEIGHT.value-1
        rainbow = [(255, 0, 0), (255, 127, 0), (255, 255, 0),
                   (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]

        starting_point: tuple[int, int]  # (x,y)

        if options.corner == "lt":
            starting_point = (0, 0)
        elif options.corner == "rt":
            starting_point = (max_width, 0)
        elif options.corner == "rb":
            starting_point = (max_width, max_height)
        elif options.corner == "lb":
            starting_point = (0, max_height)

        matrix.Clear()
        offset_canvas = matrix.CreateFrameCanvas()
        while 1:
            pass
