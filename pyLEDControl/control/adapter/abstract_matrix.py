#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
import abc
from io import BytesIO
from pathlib import Path
from typing import Union
from PIL import Image, ImageEnhance
import requests
import settings
from settings import MATRIX_DIMENSIONS


class AbstractFont(abc.ABC):
    @abc.abstractmethod
    def LoadFont(self, path: str):
        raise NotImplementedError(f"Method 'LoadFont' not implemented!")

    @abc.abstractmethod
    def CharacterWidth(self, char):
        raise NotImplementedError(f"Method 'CharacterWidth' not implemented!")


class AbstractColor(abc.ABC):
    Font: AbstractFont

    @abc.abstractmethod
    def __init__(self, r, g, b):
        raise NotImplementedError(f"Method '__init__' not implemented!")

    @abc.abstractmethod
    def to_tuple(self):
        raise NotImplementedError(f"Method 'to_tuple' not implemented!")

    @abc.abstractmethod
    def to_hex(self):
        raise NotImplementedError(f"Method 'to_hex' not implemented!")


class AbstractGraphics(abc.ABC):    
    class Color(AbstractColor):
        pass
    @abc.abstractmethod
    def DrawText(
        self,
        canvas: AbstractMatrix,
        font: AbstractFont,
        x: int,
        y: int,
        color: AbstractColor,
        text: str,
    ):
        raise NotImplementedError(f"Method 'DrawText' not implemented!")

    @abc.abstractmethod
    def DrawLine(
        self,
        canvas: AbstractMatrix,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: AbstractColor,
    ):
        raise NotImplementedError(f"Method 'DrawLine' not implemented!")

    @abc.abstractmethod
    def DrawCircle(
        self,
        canvas: AbstractMatrix,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: AbstractColor,
    ):
        raise NotImplementedError(f"Method 'DrawCircle' not implemented!")


class AbstractMatrix(abc.ABC):
    graphics: AbstractGraphics
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

    def SetImageFromURL(self, url: str, brightness: int):
        image_resp = requests.get(url)
        img = (
            Image.open(BytesIO(image_resp.content))
            .resize(
                (
                    settings.MATRIX_DIMENSIONS.WIDTH.value,
                    settings.MATRIX_DIMENSIONS.HEIGHT.value,
                ),
                Image.LANCZOS,
            )
            .convert("RGB")
        )
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)
        img.load()
        self.SetImage(img)

    def SetImageFromFile(self, path: Union[str, Path], x: int, y: int, brightness:int, resize = False):
        img = Image.open(path).convert("RGB")
        if resize:
            img = img.resize((MATRIX_DIMENSIONS.HEIGHT.value, MATRIX_DIMENSIONS.WIDTH.value), Image.LANCZOS)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)
        img.load()
        self.SetImage(img, x, y)
