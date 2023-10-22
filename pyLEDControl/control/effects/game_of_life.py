#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pickle
from dataclasses import dataclass

import numpy as np
import settings
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect


@dataclass
class Cell:
    is_alive: bool
    x: int
    y: int

    def __str__(self) -> str:
        return "0" if self.is_alive else "."


def __is_index_out_of_bounds(field: np.ndarray, x: int, y: int) -> bool:
    return (0 <= x) and (x < field.shape[0]) and (0 <= y) and (y < field.shape[1])


def __print_field(
    field: np.ndarray, matrix: AbstractMatrix, canvas: AbstractMatrix, br: int
):
    for x in range(field.shape[0]):
        for y in range(field.shape[1]):
            if field[x, y].is_alive:
                canvas.SetPixel(
                    x,
                    y,
                    255 * br,
                    255 * br,
                    255 * br,
                )
            else:
                canvas.SetPixel(
                    x,
                    y,
                    0,
                    0,
                    0,
                )
    canvas = matrix.SwapOnVSync(canvas)

def _calc_row(field, new_field, ir):
    for ic in range(field.shape[1]):
        cell = field[ir, ic]
        active_neighbors = 0
        for ranges in [
            # one row "above" the cell
            zip([cell.x - 1, cell.x, cell.x + 1], [cell.y - 1] * 3),
            # one row "below" the cell
            zip([cell.x - 1, cell.x, cell.x + 1], [cell.y + 1] * 3),
            # left and right to the cell
            zip([cell.x - 1, cell.x + 1], [cell.y] * 2),
        ]:
            for xi, yi in ranges:
                if __is_index_out_of_bounds(field, xi, yi):
                    if field[xi, yi].is_alive:
                        active_neighbors += 1
        if cell.is_alive and (active_neighbors < 2 or active_neighbors > 3):
            new_field[ir, ic].is_alive = False
        elif not cell.is_alive and (active_neighbors == 3):
            new_field[ir, ic].is_alive = True

def _new_generation(
    field: np.ndarray, matrix: AbstractMatrix, canvas: AbstractMatrix, br
):
    new_field: np.ndarray = pickle.loads(pickle.dumps(field))
    for ir in range(field.shape[0]):
        for ic in range(field.shape[1]):
            cell = field[ir, ic]
            active_neighbors = 0
            for ranges in [
                # one row "above" the cell
                zip([cell.x - 1, cell.x, cell.x + 1], [cell.y - 1] * 3),
                # one row "below" the cell
                zip([cell.x - 1, cell.x, cell.x + 1], [cell.y + 1] * 3),
                # left and right to the cell
                zip([cell.x - 1, cell.x + 1], [cell.y] * 2),
            ]:
                for xi, yi in ranges:
                    if __is_index_out_of_bounds(field, xi, yi):
                        if field[xi, yi].is_alive:
                            active_neighbors += 1
            if cell.is_alive and (active_neighbors < 2 or active_neighbors > 3):
                new_field[ir, ic].is_alive = False
            elif not cell.is_alive and (active_neighbors == 3):
                new_field[ir, ic].is_alive = True

    __print_field(new_field, matrix, canvas, br)
    return new_field


class GameOfLife(AbstractEffect):
    @staticmethod
    def run(matrix_class, options, conn, *args, **kwargs):
        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()

        field = np.empty((64, 64), dtype=Cell)
        for x in range(field.shape[0]):
            for y in range(field.shape[0]):
                field[x, y] = Cell(
                    np.random.choice([True, False], p=[1 / 6, 5 / 6]), x, y
                )

        counter = 0
        br = options.get_brightness()
        while not GameOfLife.is_terminated(conn):
            if counter == 10:
                br = options.get_brightness()
            field = _new_generation(field, matrix, canvas, br)
