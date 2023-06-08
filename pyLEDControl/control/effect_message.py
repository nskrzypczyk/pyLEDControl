#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Union


class EffectMessage:
    br_file_path = "brightness.txt"
    effect: type
    brightness: int
    options: dict

    def set_brightness(self, br: int) -> None:
        with open(self.br_file_path, "w") as f:
            f.write(str(br))

    def get_brightness(self) -> int:
        self.brightness = int(open(self.br_file_path, "r").read())
        return self.brightness / 100
