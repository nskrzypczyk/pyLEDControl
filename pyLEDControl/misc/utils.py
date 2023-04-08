#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque


def rotate(input_list: list, index: int) -> list:
    output_list = deque(input_list)
    output_list.rotate(index)
    return list(output_list)
