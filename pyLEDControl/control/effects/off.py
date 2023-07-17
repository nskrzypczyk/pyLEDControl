import time
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from settings import rgb_options
import settings


class OFF(AbstractEffect):
    @staticmethod
    def run(matrix_class_name, _, conn):
        matrix: AbstractMatrix = matrix_class_name(options=settings.rgb_options())
        matrix.Clear()
        while OFF.is_terminated(conn):
            time.sleep(5)
