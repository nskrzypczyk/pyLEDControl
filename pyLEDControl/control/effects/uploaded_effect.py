from dataclasses import dataclass
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
import time
from typing import List
from misc.domain_data import MultiselectConstraint
import settings
from control.abstract_effect_options import AbstractEffectOptions
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log
from server.routes.effect_upload_routes import (
    custom_effects_with_settings,
    open_conf_file,
)
import imageio
from control.effects.shuffle import exit_sub
from PIL import Image, ImageEnhance
from server.routes.effect_upload_routes import load_yaml_file_as_dict
from settings import MATRIX_DIMENSIONS


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
            items=lambda: list(custom_effects_with_settings.keys()),
            strict=True,
        )

    @staticmethod
    def run(matrix_class: AbstractMatrix, options: Options, conn_p: Connection, *args, **kwargs):
        def run_gif(matrix:AbstractMatrix, options: UploadedEffect.Options, conn_p:Connection, image_path:str):
            frames = convert_gif_to_frames(image_path)
            framerate = 1/30
            def print_gif():
                for frame in frames:
                    matrix.SetImage(ImageEnhance.Brightness(frame.convert("RGB")).enhance(options.get_brightness()))
                    time.sleep(framerate)
            while not __class__.is_terminated(conn_p):
                print_gif()
            matrix.Clear()

        def run_jpeg_png(matrix:AbstractMatrix, options: UploadedEffect.Options, conn_p:Connection, image_path:str):
            matrix.SetImageFromFile(image_path, 0,0,options.get_brightness(), True)
            while not __class__.is_terminated(conn_p):
                time.sleep(1)
            matrix.Clear()
    



        log = Log("UploadedEffect")
        matrix: AbstractMatrix = matrix_class(options=settings.rgb_options())

        conf_files = [
           load_yaml_file_as_dict(name, read=True) for name in options.active_effects
        ]
        current_proc = None
        counter = 0
        while not __class__.is_terminated(conn_p):
            if counter == len(options.active_effects):
                log.info("Resetting counter")
                counter = 0
            _conn, _conn_c = Pipe(True)

            if counter >= len(options.active_effects):
                exit_sub(current_proc, log, _conn)
                return UploadedEffect.run(matrix, options, conn_p)
            

            current_proc = Process(
                target=run_gif if conf_files[counter].get("source").endswith(".gif") else run_jpeg_png,
                args=[matrix, options, _conn_c, conf_files[counter].get("source")]
            )

            counter += 1
            log.info("Stating custom effect")
            current_proc.start()

            log.info("Sleeping")
            time.sleep(7)
            exit_sub(current_proc, log, _conn)
        exit_sub(current_proc, log, _conn)

def convert_gif_to_frames(gif_path):
    with imageio.get_reader(gif_path) as reader:
        return [Image.fromarray(frame).resize((settings.MATRIX_DIMENSIONS.HEIGHT.value, settings.MATRIX_DIMENSIONS.WIDTH.value), Image.ADAPTIVE) for frame in reader]

# TODO: Extract to helper / misc module
def exit_sub(tt, log, conn):
    if tt is not None and tt.is_alive():
        log.debug("Killing child process")
        conn.send(True)
        tt.join()
