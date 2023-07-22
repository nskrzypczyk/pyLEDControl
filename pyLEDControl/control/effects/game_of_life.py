#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from control.effects.abstract_effect import AbstractEffect
import settings
from control.adapter.abstract_matrix import AbstractMatrix
import time
import random
import copy
from typing import List, NewType
from dataclasses import dataclass

REFRESH_RATE = 1 / 30


@dataclass
class Cell:
    is_alive: bool
    x: int
    y: int

    def __str__(self) -> str:
        return "0" if self.is_alive else "."


Field: NewType = NewType("Field", List[List[Cell]])


def __is_index_out_of_bounds(field: Field, x: int, y: int) -> bool:
    return (0 <= x) and (x < len(field)) and (0 <= y) and (y < len(field[0]))


def __print_field(
    field: Field, matrix: AbstractMatrix, canvas: AbstractMatrix, br: int
):
    for row in field:
        for cell in row:
            if cell.is_alive:
                canvas.SetPixel(
                    cell.x,
                    cell.y,
                    255 * br,
                    255 * br,
                    255 * br,
                )
            else:
                canvas.SetPixel(
                    cell.x,
                    cell.y,
                    0,
                    0,
                    0,
                )
    canvas = matrix.SwapOnVSync(canvas)


def _new_generation(field: Field, matrix: AbstractMatrix, canvas: AbstractMatrix, br):
    new_field: Field = copy.deepcopy(field, None, [])
    for ir, row in enumerate(field):
        for ic, cell in enumerate(row):
            active_neighbors = 0
            for ranges in [
                zip([cell.x - 1, cell.x, cell.x + 1], [cell.y - 1] * 3),
                zip([cell.x - 1, cell.x, cell.x + 1], [cell.y + 1] * 3),
                zip([cell.x - 1, cell.x + 1], [cell.y] * 2),
            ]:
                for xi, yi in ranges:
                    if __is_index_out_of_bounds(field, xi, yi):
                        if field[xi][yi].is_alive:
                            active_neighbors += 1
            if cell.is_alive and (active_neighbors < 2 or active_neighbors > 3):
                new_field[ir][ic].is_alive = False
            elif not cell.is_alive and (active_neighbors == 3):
                new_field[ir][ic].is_alive = True

    __print_field(new_field, matrix, canvas, br)
    return new_field


class GameOfLife(AbstractEffect):
    @staticmethod
    def run(matrix_class, msg, conn):
        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()

        field = Field([])
        for x in range(64):
            row = []
            for y in range(64):
                row.append(Cell(random.choice([True, False]), x, y))
            field.append(row)

        counter = 0
        br = msg.get_brightness()
        while not GameOfLife.is_terminated(conn):
            if counter == 20:
                br = msg.get_brightness()
            field = _new_generation(field, matrix, canvas, br)
            time.sleep(REFRESH_RATE)
