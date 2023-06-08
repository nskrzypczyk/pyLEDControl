from abc import abstractmethod
from control.effects.abstract_effect import AbstractEffect
from control.effect_message import EffectMessage
from control.adapter.abstract_matrix import AbstractMatrix
import settings


class Shuffle(AbstractEffect):
    @abstractmethod
    def run(matrix: type, msg: EffectMessage):
        matrix: AbstractMatrix = matrix(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()
        font = matrix.graphics.Font()
        font.LoadFont("../../rpi-rgb-led-matrix/fonts/6x9.bdf")
        refresh_rate = 5
