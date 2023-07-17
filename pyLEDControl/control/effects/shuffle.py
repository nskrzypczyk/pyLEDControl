from abc import abstractmethod
import os
import time
from control.effects.abstract_effect import AbstractEffect
from control.effect_message import EffectMessage
from control.adapter.abstract_matrix import AbstractMatrix
from misc.logging import Log
from threading import Thread
from multiprocessing import Process


class Shuffle(AbstractEffect):
    @abstractmethod
    def run(matrix: type, msg: EffectMessage, conn):
        log = Log(__class__.__name__)
        from control.effects import effect_dict

        local_effect_dict = effect_dict
        local_effect_dict.pop("OFF")
        max_count = len(local_effect_dict)
        counter = 0
        while not Shuffle.is_terminated(conn):
            if counter == max_count - 1:
                log.debug("Resetting counter")
                counter = 0

            tt = Process(
                target=list(local_effect_dict.values())[counter].run,
                args=[matrix, msg, conn],
            )
            counter += 1
            log.debug("Starting thread")
            tt.start()
            log.debug("Sleeping")
            time.sleep(7)
            exit_sub(tt, log)
        exit_sub(tt, log)


def exit_sub(tt, log):
    while tt.is_alive():
        log.debug("Killing child process")
        tt.terminate()
        tt.join()
