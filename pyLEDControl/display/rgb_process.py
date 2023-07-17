import os
import time
import settings
from control.effects.abstract_effect import AbstractEffect
from control.adapter.abstract_matrix import AbstractMatrix
from control.adapter.real_matrix import RealMatrix
from misc.logging import Log
from control.effect_message import EffectMessage
from multiprocessing import Process, Queue, Pipe


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
                    message: EffectMessage = queue.get(block=False)
                    print(message)
                    if message.effect != current_effect:
                        self.log.debug("Effect has changed. Restarting process")

                        if proc:
                            conn_p.send(True)
                            proc.join()
                        conn_p, conn_c = Pipe(True)
                        proc = Process(
                            target=message.effect.run, args=[matrix, message, conn_c]
                        )
                        proc.start()
                        current_effect = message.effect
                time.sleep(1)
            except KeyboardInterrupt:
                self.log.debug("Terminating")

    def run(self, queue: Queue):
        self.log.debug("run method called.")
        self.loop(self.matrix, queue)
