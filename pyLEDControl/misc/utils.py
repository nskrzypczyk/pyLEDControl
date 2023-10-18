#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from collections import deque
from dataclasses import Field
from typing import List, Union

from misc.domain_data import AbstractConstraint


def rotate(input_list: list, index: int) -> list:
    output_list = deque(input_list)
    output_list.rotate(index)
    return list(output_list)


def chunk_list(lst, size) -> List[List]:
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def __check_constraints(cls: type, att_name: str) -> Union[dict, None]:
    constraint_attriubute: AbstractConstraint = cls.__base__.__dict__.get(f"{att_name}_constraint")
    if constraint_attriubute is None:
        constraint_attriubute = cls.__dict__.get(f"{att_name}_constraint")
    if constraint_attriubute is None:
        return None
    return constraint_attriubute.get_definition()


def to_json_td(cls: type) -> dict:
    type_def = {}
    att_field: Field
    for att_name, att_field in cls.__dict__["__dataclass_fields__"].items():
        type_def[str(att_name)] = __att_to_json(att_field.type)
        constraint_def = __check_constraints(cls, att_name)
        if constraint_def is not None:
            type_def[str(att_name)]["constraint"] = constraint_def
    return type_def


def __python_type_to_json_type(t: str) -> str:
    if t in ["int", "float"]:
        return "number"
    elif t == "bool":
        return "boolean"
    elif t in ["str", "type"]:
        return "string"
    elif t == "None":
        return "null"
    elif t == "list":
        return "any[]"
    elif t.split("[")[0] == "List":
        return f"{__python_type_to_json_type(t.split('[')[1][:-1])}[]"
    else:
        return "any"


def __extract_class(field) -> str:
    as_string = str(field)
    if "'" not in as_string:
        return as_string
    return as_string.split("'")[1]


def __att_to_json(data: str) -> dict:
    return {"type": __python_type_to_json_type(__extract_class(data))}
