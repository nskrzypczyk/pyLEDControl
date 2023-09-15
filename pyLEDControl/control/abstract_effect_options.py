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
    

def to_json_td(cls: type):
    type_def = {}
    v:Field
    for k, v in cls.__dict__["__dataclass_fields__"].items():
        type_def[str(k)] = __att_to_json(v.type)
        # Hier weiter machen! JTD schema einführen
    return type_def


def __att_to_json(data):
    print(data)
    if data is None or data in [bool, int, float, str, object]:
        return data
    elif data is list:
        return [__att_to_json(d) for d in data]
    elif data is dict:
        return {k: __att_to_json(v) for k, v in data.items()}
    return to_json_td(data.__class__)


def get_attribute_types(obj:type):
    dc_fields = obj.__dict__["__dataclass_fields__"]
    attributes = dict()
    v:Field
    for k,v in dc_fields.items():
        attributes[k]=str(v.type)
    print(attributes)
    return attributes
