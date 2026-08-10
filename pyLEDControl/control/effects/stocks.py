
import settings
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
import numpy as np

class Stocks(AbstractEffect):
    @staticmethod
    def run(matrix_cls: type, options, conn, *args, **kwargs):
        matrix, canvas, font, field, rows, cols = AbstractEffect.create_context(matrix_cls)

    