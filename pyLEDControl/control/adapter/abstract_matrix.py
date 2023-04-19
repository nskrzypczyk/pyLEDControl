#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import abc

class AbstractFont(abc.ABC):
    @abc.abstractmethod
    def LoadFont(self, path:str):
        raise NotImplementedError(f"Method 'LoadFont' not implemented!")

    @abc.abstractmethod
    def CharacterWidth(self, char):
        raise NotImplementedError(f"Method 'CharacterWidth' not implemented!")
    

class AbstractColor(abc.ABC):
    Color:AbstractColor
    Font:AbstractFont

    @abc.abstractmethod
    def __init__(self,r,g,b):
        raise NotImplementedError(f"Method '__init__' not implemented!")

    @abc.abstractmethod
    def adjust_brightness(self,alpha:float, to_int = False):
        raise NotImplementedError(f"Method 'adjust_brightness' not implemented!")

    @abc.abstractmethod
    def to_tuple(self):
        raise NotImplementedError(f"Method 'to_tuple' not implemented!")
    
    @abc.abstractmethod
    def to_hex(self):
        raise NotImplementedError(f"Method 'to_hex' not implemented!")
        

class AbstractGraphics(abc.ABC):
    @abc.abstractmethod
    def DrawText(canvas: AbstractMatrix, font: AbstractFont, x:int , y:int, text:str):
        raise NotImplementedError(f"Method 'DrawText' not implemented!")
    
    @abc.abstractmethod
    def DrawLine(canvas: AbstractMatrix, x1:int, y1: int, x2:int, y2:int, color:AbstractColor):
        raise NotImplementedError(f"Method 'DrawLine' not implemented!")

    @abc.abstractmethod
    def DrawCircle(canvas: AbstractMatrix, x1:int, y1: int, x2:int, y2:int, color: AbstractColor):
        raise NotImplementedError(f"Method 'DrawCircle' not implemented!")


class AbstractMatrix(abc.ABC):
    graphics:AbstractGraphics # TODO: Class definition
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
