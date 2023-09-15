#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
from enum import Enum
from typing import List, TypeVar

from control.abstract_effect_options import AbstractEffectOptions


def rotate(input_list: list, index: int) -> list:
    output_list = deque(input_list)
    output_list.rotate(index)
    return list(output_list)


def chunk_list(lst, size) -> List[List]:
    return [lst[i:i+size] for i in range(0, len(lst), size)]

class Generics(Enum): # TODO: Move to domain data
    T_EFFECT_OPTIONS = TypeVar("T",bound=AbstractEffectOptions)
