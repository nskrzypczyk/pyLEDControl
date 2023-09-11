#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import abc
from dataclasses import Field, dataclass

@dataclass
class AbstractEffectOptions(abc.ABC):
    br_file_path = "brightness.txt"
    effect: type
    brightness: int

    def set_brightness(self, br: int) -> None:
        with open(self.br_file_path, "w") as f:
            f.write(str(br))

    def get_brightness(self) -> int:
        self.brightness = int(open(self.br_file_path, "r").read())
        return self.brightness / 100


def get_attribute_types(obj:type):
    dc_fields = obj.__dict__["__dataclass_fields__"]
    attributes = dict()
    v:Field
    for k,v in dc_fields.items():
        attributes[k]=str(v.type)
    print(attributes)
    return attributes
