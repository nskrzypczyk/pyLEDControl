#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import unittest

from control.adapter.emulated_matrix import EmulatedMatrix
from control.effects.rainbow_wave import RainbowWave
from control.effect_message import EffectMessage
from control.effects.effect_message_builder import EffectMessageBuilder
from settings import rgb_options


class TestRainbowWave(unittest.TestCase):
    RainbowWave.run(
        EmulatedMatrix, EffectMessageBuilder().set_brightness(100).build())


if __name__ == "__main__":
    try:
        unittest.main()
    except KeyboardInterrupt:
        sys.exit(0)
