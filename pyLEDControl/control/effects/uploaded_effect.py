import time
from dataclasses import dataclass
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from typing import List
import settings
from control.abstract_effect_options import AbstractEffectOptions
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.domain_data import MultiselectConstraint
from misc.logging import Log
from server.routes.effect_upload_routes import load_yaml_file_as_dict

log = Log("UploadedEffect")

def load_effects(): # No eye candy really ._.
    from server.routes.effect_upload_routes import custom_effects_with_settings
    return list(custom_effects_with_settings.keys())

class UploadedEffect(AbstractEffect):
    """
    Purpose: Uses yaml configurations which include the path to the media to be displayed.
    This path is used to load the media and display it
    """

    @dataclass
    class Options(AbstractEffectOptions):

        custom = True
        active_effects: List[str]
        active_effects_constraint = MultiselectConstraint(
            display_name="Active uploaded effects",
            items=load_effects,
            strict=True,
        )

    @staticmethod
    def run_gif(matrix_class, options: Options, conn_p:Connection, image_path:str):
        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())
        print_gif: callable = matrix.SetFramesInLoop(image_path, options, 0.08)
        while not __class__.is_terminated(conn_p):
            print_gif()

    @staticmethod
    def run_jpeg_png(matrix_class, options: Options, conn_p:Connection, image_path:str):
        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())
        log.info("Running png/jpg "+image_path)
        matrix.SetImageFromFile(image_path, 0,0,options.get_brightness(), True)
        while not __class__.is_terminated(conn_p):
            pass
        matrix.Clear()


    @staticmethod
    def run(matrix_class: AbstractMatrix, options: Options, conn_p: Connection, *args, **kwargs):
        current_proc = None
        counter = 0
        while not __class__.is_terminated(conn_p):
            try:
                conf_files = [
                    load_yaml_file_as_dict(name, read=True) for name in options.active_effects
                ]
            except Exception:
                conf_files = []

            if counter >= len(options.active_effects):
                exit_sub_proc(current_proc, log, _conn)
                return UploadedEffect.run(matrix_class, options, conn_p)
            
            _conn, _conn_c = Pipe(True)

            current_proc = Process(
                target=UploadedEffect.run_gif if conf_files[counter].get("source").endswith(".gif") else UploadedEffect.run_jpeg_png,
                args=[matrix_class, options, _conn_c, conf_files[counter].get("source")]
            )

            counter += 1
            log.info("Stating custom effect")
            current_proc.start()

            log.info("Sleeping")
            time.sleep(7)
            exit_sub_proc(current_proc, log, _conn)
        exit_sub_proc(current_proc, log, _conn)



# TODO: Extract to helper / misc module
def exit_sub_proc(tt, log, conn):
    if tt is not None and tt.is_alive():
        log.debug("Killing child process")
        conn.send(True)
        tt.join()
