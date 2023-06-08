#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
from typing import List


def rotate(input_list: list, index: int) -> list:
    output_list = deque(input_list)
    output_list.rotate(index)
    return list(output_list)


def chunk_list(lst, size) -> List[List]:
    return [lst[i:i+size] for i in range(0, len(lst), size)]
