#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import unittest

from control.adapter.emulated_matrix import EmulatedMatrix
from control.effects.weather import Weather
from control.abstract_effect_options import AbstractEffectOptions
from control.effects.effect_message_builder import EffectMessageBuilder
from control.effects.spotify import Spotify
from settings import rgb_options


class TestWeather(unittest.TestCase):
    Weather.run(EmulatedMatrix, EffectMessageBuilder().set_brightness(100).build())


if __name__ == "__main__":
    try:
        unittest.main()
    except KeyboardInterrupt:
        sys.exit(0)
