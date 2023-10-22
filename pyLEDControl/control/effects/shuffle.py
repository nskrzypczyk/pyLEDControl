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
from control.effects import get_effects


class Shuffle(AbstractEffect):
    @dataclass
    class Options(AbstractEffectOptions):
        active_effects: List[str]

        active_effects_constraint = MultiselectConstraint("Active effects",
                                                          list(
                                                              set(get_effects().keys()) - {"AbstractEffect", "Shuffle", "OFF"}),
                                                          True)

    def run(matrix: type, options: Options, conn_p: Connection, conn_p_options: Connection, *args, **kwargs):
        log = Log(__class__.__name__)

        counter = 0
        while not __class__.is_terminated(conn_p):
            new_options = __class__.get_new_options(conn_p_options)
            # TODO: Extract this to somewhere else
            if new_options is not None and new_options.active_effects != options.active_effects: # if active effect list has been changed
                options = new_options
                counter = 0
            elif counter == len(options.active_effects):
                log.debug("Resetting counter")
                counter = 0
            _conn, conn_c = Pipe(True)
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
    if tt.is_alive():
        log.debug("Killing child process")
        conn.send(True)
        tt.join()
