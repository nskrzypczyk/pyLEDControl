from dataclasses import dataclass
from typing import List
from misc.domain_data import MultiselectConstraint
import settings
from control.abstract_effect_options import AbstractEffectOptions
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log

log = Log("UploadedEffect")
def get_uploaded_effects() -> list:
    return []

class UploadedEffect(AbstractEffect):
    @dataclass
    class Options(AbstractEffectOptions):
        active_effects: List[str]
        active_effects_constraint = MultiselectConstraint("Active uploaded effects", get_uploaded_effects(), strict=True)
    @staticmethod
    def run(matrix_class, options, conn, *args, **kwargs):
        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()