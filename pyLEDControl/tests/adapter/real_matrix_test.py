#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import unittest
import multiprocessing
from control.adapter.real_matrix import RealMatrix
from control.effects.rainbow_wave import RainbowWave
from settings import rgb_options


class TestRealMatrix(unittest.TestCase):
    def test_rgb_matrix(self):
        def child_process2():    
            matrix = RealMatrix(options=rgb_options())
            RainbowWave.run(matrix)
        def child_process1():
            p1 = multiprocessing.Process(target=child_process2)
            p1.start()
            p1.join()

        p = multiprocessing.Process(target=child_process1)
        p.start()
        p.join()


if __name__ == "__main__":
    try:
        unittest.main()
    except KeyboardInterrupt:
        sys.exit(0)
