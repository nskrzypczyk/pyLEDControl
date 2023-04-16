#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import abc


class AbstractMatrix(abc.ABC):
    graphics:any # TODO: Class definition
    """
    Method names are derived from the Canvas class of the RGBMatrixEmulator module
    """

    @abc.abstractmethod
    def Clear(self):
        raise NotImplementedError(f"Method 'Clear' not implemented!")

    @abc.abstractmethod
    def Fill(self, r: int, g: int, b: int):
        raise NotImplementedError(f"Method 'Fill' not implemented!")

    @abc.abstractmethod
    def SetPixel(self, x: int, y: int, r: int, g: int, b: int):
        raise NotImplementedError(f"Method 'SetPixel' not implemented!")

    @abc.abstractmethod
    def SetImage(self, image, offset_x=0, offset_y=0, *other):
        raise NotImplementedError(f"Method 'SetImage' not implemented!")

    @abc.abstractmethod
    def SwapOnVSync(self, canvas):
        raise NotImplementedError(f"Method 'SwapOnVSync' not implemented!")

    @abc.abstractmethod
    def CreateFrameCanvas(self):
        raise NotImplementedError(
            f"Method 'CreateFrameCanvas' not implemented!")
