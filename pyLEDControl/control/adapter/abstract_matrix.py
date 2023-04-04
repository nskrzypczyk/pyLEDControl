#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import abc


class AbstractMatrix(abc.ABC):
    """
    Method names are derived from the Canvas class of the RGBMatrixEmulator module
    """

    @abc.abstractmethod
    def Clear(self):
        pass

    @abc.abstractmethod
    def Fill(self, r: int, g: int, b: int):
        pass

    @abc.abstractmethod
    def SetPixel(self, x: int, y: int, r: int, g: int, b: int):
        pass

    @abc.abstractmethod
    def SetImage(self, image, offset_x=0, offset_y=0, *other):
        pass

    @abc.abstractmethod
    def SwapOnVSync(self, canvas):
        pass

    @abc.abstractmethod
    def CreateFrameCanvas(self):
        pass
