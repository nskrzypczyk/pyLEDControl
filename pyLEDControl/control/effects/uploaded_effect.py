from dataclasses import dataclass
from typing import List
from misc.domain_data import MultiselectConstraint
import settings
from control.abstract_effect_options import AbstractEffectOptions
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log
from server.routes.effect_upload_routes import custom_effects_with_settings

# @dataclass
# class UploadedEffectDefinition():
    

class UploadedEffect(AbstractEffect):
    """
    Purpose: Uses yaml configurations which include the path to the media to be displayed.
    This path is used to load the media and display it
    """
    @dataclass
    class Options(AbstractEffectOptions):
        # TODO Frontend must check both, standard and custom routes or figure smt out
        
        custom = True
        active_effects: List[str]
        active_effects_constraint = MultiselectConstraint(
            display_name = "Active uploaded effects", 
            items = lambda: list(custom_effects_with_settings.keys()), 
            strict=True)
    @staticmethod
    def run(matrix_class, options, conn, *args, **kwargs):
        log = Log("UploadedEffect")
        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())
        canvas: AbstractMatrix = matrix.CreateFrameCanvas()