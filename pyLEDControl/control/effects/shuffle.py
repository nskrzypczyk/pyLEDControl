import time
from abc import abstractmethod
from dataclasses import dataclass
from multiprocessing import Pipe, Process
from typing import List

from control.abstract_effect_options import AbstractEffectOptions
from control.adapter.abstract_matrix import AbstractMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log


class Shuffle(AbstractEffect):
    @dataclass
    class Options(AbstractEffectOptions):
        active_effects: List[str]

    @abstractmethod
    def run(matrix: type, options: Options, conn_p):
        log = Log(__class__.__name__)
        from control.effects import effect_dict

        local_effect_dict = effect_dict
        for unwanted in ["Shuffle", "OFF", "AbstractEffect"]: # TODO: Add decorator / interface for unwanted effects
            if unwanted in local_effect_dict:
                local_effect_dict.pop(unwanted)
        max_count = len(local_effect_dict)
        counter = 0
        while not Shuffle.is_terminated(conn_p):
            if counter == max_count - 1:
                log.debug("Resetting counter")
                counter = 0
            _conn, conn_c = Pipe(True)
            tt = Process(
                target=list(local_effect_dict.values())[counter].run,
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
