#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

from collections import deque
from dataclasses import Field
from typing import List, Union

from misc.domain_data import AbstractDataComponent


def rotate(input_list: list, index: int) -> list:
    output_list = deque(input_list)
    output_list.rotate(index)
    return list(output_list)


def chunk_list(lst, size) -> List[List]:
    return [lst[i:i + size] for i in range(0, len(lst), size)]

# Safely gets the data component attribute definition.
def __check_data_component_attributes(cls: type, att_name: str) -> Union[dict, None]:
    attribute_name = f"{att_name}_dc"
    component_attribute: AbstractDataComponent = cls.__base__.__dict__.get(attribute_name)
    if component_attribute is None:
        component_attribute = cls.__dict__.get(attribute_name)
    if component_attribute is None:
        return None
    return component_attribute.get_definition()


def to_json_td(cls: type) -> dict:
    type_def = {}
    att_field: Field
    for att_name, att_field in cls.__dict__["__dataclass_fields__"].items():
        type_def[str(att_name)] = __att_to_json(att_field.type)
        data_component_def = __check_data_component_attributes(cls, att_name)
        if data_component_def is not None:
            type_def[str(att_name)]["dataComponent"] = data_component_def
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
