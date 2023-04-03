#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
import settings
from typing import Literal
from RGBMatrixEmulator import RGBMatrix
from control.effects.abstract_effect import AbstractEffect


class RainbowWave(AbstractEffect):
    @dataclass
    class EffectOptions():
        corner: Literal["lu", "ru", "lb", "rb"] = "lu"

    default_options: EffectOptions = EffectOptions("lu")

    @staticmethod
    def run(matrix: RGBMatrix, options: EffectOptions = default_options):
        starting_point: tuple[int, int]  # (x,y)
        if options.corner == "lu":
            starting_point = (0, 0)

        elif options.corner == "ru":
            starting_point = (settings.MATRIX_EMULATION.WIDTH.value, 0)
        elif options.corner == "rb":
            starting_point = (settings.MATRIX_EMULATION.WIDTH.value,
                              settings.MATRIX_EMULATION.HEIGHT.value)
        elif options.corner == "lb":
            starting_point = (0, settings.MATRIX_EMULATION.HEIGHT.value)
