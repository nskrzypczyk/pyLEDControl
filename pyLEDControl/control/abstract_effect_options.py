#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import abc
from dataclasses import Field, dataclass, field
from typing import Callable, Literal, TypeVar, Union
import typing
from misc.domain_data import IntervalConstraint

# TODO: REFACTORING AFTER IMPLEMENTING OPTION CLASS ABSTRACTION!


@dataclass
class AbstractEffectOptions(abc.ABC):
    br_file_path = "brightness.txt"
    effect: type
    brightness: int

    brightness_constraints = IntervalConstraint(0, True, 100, True)

    def set_brightness(self, br: int) -> None:
        with open(self.br_file_path, "w") as f:
            f.write(str(br))

    def get_brightness(self) -> float:
        self.brightness = int(open(self.br_file_path, "r").read())
        return self.brightness / 100


def to_json_td(cls: type):
    type_def = {}
    v: Field
    for k, v in cls.__dict__["__dataclass_fields__"].items():
        type_def[str(k)] = __att_to_json(v.type)
        # Hier weiter machen! JTD schema einführen
    return type_def


def __python_type_to_json_type(t: type) -> str:
    if t in [int, float]:
        return "number"
    elif t == bool:
        return "boolean"
    elif t == str:
        return "string"
    elif t == None:
        return "null"
    elif t == list:
        return "any[]"
    else:
        return "any"


def __GenericAllias_to_json_string_converter(ga: typing._GenericAlias) -> str:
    """ Example for _Genericalias: 
        >>>  {'_inst': False, '_name': 'List', '__origin__': <class 'list'>, '__slots__': None, '__args__': (<class 'str'>,), '__parameters__': (), '_paramspec_tvars': False}  
    """
    if ga.__dict__["__origin__"] == list:
        return f"{__att_to_json(ga.__dict__['__args__'][0],True)}[]"


def __att_to_json(data: type, is_class = False):
    cls = data.__class__ if not is_class else data
    if (cls is None) or (cls in [bool, int, float, str, object, list]):
        return __python_type_to_json_type(cls)

    elif cls is typing._GenericAlias:
        if data.__dict__["__origin__"] == list:
            return __GenericAllias_to_json_string_converter(data)
        else:
            return __python_type_to_json_type(None)
    return to_json_td(cls.__class__)


def get_attribute_types(obj: type):
    """Note: Input type/instance must be a @dataclass

    Args:
        obj (type): _description_

    Returns:
        attributes: A dict[Field,str] where the values are the names of the fields.
    """
    dc_fields = obj.__dict__["__dataclass_fields__"]
    attributes = dict()
    v: Field
    for k, v in dc_fields.items():
        attributes[k] = str(v.type)
    return attributes
