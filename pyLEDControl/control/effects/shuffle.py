import time
from dataclasses import dataclass
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from typing import List

from control.abstract_effect_options import AbstractEffectOptions
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects import get_effect_list, get_effects
from control.effects.abstract_effect import AbstractEffect
from control.effects.uploaded_effect_single import (UploadedEffectSingle,
                                                    load_effects)
from misc.domain_data import MultiselectConstraint
from misc.logging import Log
from server.routes.effect_upload_routes import load_existing_file_paths

uploaded_effects_list = []
base_effects_list = list(set(get_effect_list()) - {"AbstractEffect", "Shuffle", "OFF", "UploadedEffect", "UploadedEffectSingle"})
def load_uploaded_effects():
    uploaded_effects_list = load_effects()
    return uploaded_effects_list


class Shuffle(AbstractEffect):
    @dataclass
    class Options(AbstractEffectOptions):
        global base_effects_list, uploaded_effects_list
        active_effects: List[str]
        active_effects_constraint = MultiselectConstraint(
            display_name="Active effects",
            items=lambda: base_effects_list + load_uploaded_effects(),
            strict=True,
        )

    def run(matrix_class: type, options: Options, conn_p: Connection, *args, **kwargs):
        global base_effects_list, uploaded_effects_list
        log = Log(__class__.__name__)
        tt = None
        counter = 0
        while not __class__.is_terminated(conn_p):
            uploaded_effects_list = list(load_existing_file_paths().keys())
            if counter == len(options.active_effects):
                log.debug("Resetting counter")
                counter = 0
            _conn, conn_c = Pipe(True)

            # active_effects can run on the fly via pipes so we need to check.
            # introducing another variable for this matter is not necessary.
            if counter >= len(options.active_effects):
                exit_sub_proc(tt, log, _conn)
                return Shuffle.run(matrix_class, options, conn_p)
            active_effect = options.active_effects[counter]
            counter += 1
            if active_effect in base_effects_list:
                tt = Process(
                    target=get_effects()[active_effect].run,
                    args=[matrix_class, options, conn_c],
                )
                tt.start()
            elif active_effect in load_effects():
                options.active_effect = active_effect
                tt = Process(
                    target=UploadedEffectSingle.run,
                    args=[matrix_class, options, conn_c],
                )
                tt.start()
            else:
                continue
            log.debug("Sleeping")
            time.sleep(7)
            exit_sub_proc(tt, log, _conn)
        exit_sub_proc(tt, log, _conn)


def exit_sub_proc(tt, log, conn):
    if tt is not None and tt.is_alive():
        log.debug("Killing child process")
        conn.send(True)
        tt.join()
