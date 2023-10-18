import os
import time
from multiprocessing import Pipe, Process, Queue

from control.abstract_effect_options import AbstractEffectOptions
from control.adapter.abstract_matrix import AbstractMatrix
from control.adapter.real_matrix import RealMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log


class MatrixProcess:
    def __init__(self, matrix: AbstractMatrix) -> None:
        self.matrix = matrix
        self.log: Log = Log("MatrixProcesss")

    def loop(self, matrix, queue: Queue):
        proc: Process = None
        current_effect: AbstractEffect = None
        while 1:
            try:
                if queue.empty():
                    self.log.debug("Queue is empty")
                else:
                    queue_data = queue.get(block=False)
                    effect_class: AbstractEffect = queue_data[0]
                    options: AbstractEffectOptions = queue_data[1]
                    if options.effect != current_effect:
                        self.log.debug(
                            "Effect has changed. Restarting process")

                        if proc:
                            conn_p.send(True)
                            proc.join()
                        conn_p, conn_c = Pipe(True)
                        proc = Process(
                            target=effect_class.run, args=[
                                matrix, options, conn_c
                            ]
                        )
                        proc.start()
                        current_effect = options.effect
                time.sleep(1)
            except KeyboardInterrupt:
                self.log.debug("Terminating")

    def run(self, queue: Queue):
        self.log.debug("run method called.")
        self.loop(self.matrix, queue)
