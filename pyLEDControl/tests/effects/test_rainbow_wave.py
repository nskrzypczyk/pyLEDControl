#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import unittest

from control.adapter.emulated_matrix import EmulatedMatrix
from control.effects.rainbow_wave import RainbowWave
from settings import rgb_options


class TestRainbowWave(unittest.TestCase):
    matrix = EmulatedMatrix(options=rgb_options)
    RainbowWave.run(matrix)


if __name__ == "__main__":
    try:
        unittest.main()
    except KeyboardInterrupt:
        sys.exit(0)
