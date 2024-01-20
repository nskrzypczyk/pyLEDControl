import time
from dataclasses import dataclass
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from typing import List
from control.effects.uploaded_effect import UploadedEffect
import settings
from control.abstract_effect_options import AbstractEffectOptions
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.domain_data import MultiselectConstraint, SingleselectConstraint
from misc.logging import Log
from server.routes.effect_upload_routes import load_yaml_file_as_dict

log = Log("UploadedEffectSingle")

def load_effects(): # No eye candy really ._.
    from server.routes.effect_upload_routes import custom_effects_with_settings
    return list(custom_effects_with_settings.keys())

class UploadedEffectSingle(UploadedEffect, AbstractEffect):
    """
    Purpose: Uses yaml configurations which include the path to the media to be displayed.
    This path is used to load the media and display it
    """

    @dataclass
    class Options(AbstractEffectOptions):

        custom = True
        active_effect: str 
        active_effect_constraint = SingleselectConstraint(
            display_name="Active uploaded effects",
            items=load_effects,
        )

    @staticmethod
    def run(matrix_class: AbstractMatrix, options: Options, conn_p: Connection, *args, **kwargs):
        try:
            conf_file = load_yaml_file_as_dict(options.active_effect, read=True)
            
        except Exception:
            conf_file = None

        target = UploadedEffectSingle.run_gif if conf_file.get("source").endswith(".gif") else UploadedEffectSingle.run_jpeg_png
        target(matrix_class, options, conn_p, conf_file.get("source"))
