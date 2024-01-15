import time
from dataclasses import dataclass
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from typing import List

from control.abstract_effect_options import AbstractEffectOptions
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log
from misc.domain_data import MultiselectConstraint
from control.effects import get_effects, get_effect_list


class Shuffle(AbstractEffect):
    @dataclass
    class Options(AbstractEffectOptions):
        active_effects: List[str]

        active_effects_constraint = MultiselectConstraint(
            display_name="Active effects",
            items=list(set(get_effect_list()) - {"AbstractEffect", "Shuffle", "OFF"}),
            strict=True,
        )

    def run(matrix: type, options: Options, conn_p: Connection, *args, **kwargs):
        log = Log(__class__.__name__)
        tt = None
        counter = 0
        while not __class__.is_terminated(conn_p):
            if counter == len(options.active_effects):
                log.debug("Resetting counter")
                counter = 0
            _conn, conn_c = Pipe(True)

            # active_effects can run on the fly via pipes so we need to check.
            # introducing another variable for this matter is not necessary.
            if counter >= len(options.active_effects):
                exit_sub(tt, log, _conn)
                return Shuffle.run(matrix, options, conn_p)
            tt = Process(
                target=get_effects()[options.active_effects[counter]].run,
                args=[matrix, options, conn_c],
            )

            counter += 1
            log.debug("Starting thread")
            tt.start()

            log.debug("Sleeping")
            time.sleep(7)
            exit_sub(tt, log, _conn)
        exit_sub(tt, log, _conn)


def exit_sub(tt, log, conn):
    if tt is not None and tt.is_alive():
        log.debug("Killing child process")
        conn.send(True)
        tt.join()
