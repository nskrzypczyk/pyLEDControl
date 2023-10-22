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
        current_options: AbstractEffectOptions = None
        while 1:
            try:
                if queue.empty():
                    self.log.debug("Queue is empty")
                else:
                    queue_data = queue.get(block=False) # get effect and corresponding options from queue
                    effect_class: AbstractEffect = queue_data[0]
                    options: AbstractEffectOptions = queue_data[1]
                    if current_options is None or (options.effect != current_options.effect): # if the effect changes
                        self.log.debug(
                            "Effect has changed. Restarting process")

                        if proc:
                            conn_p.send(True) # send kill signal to current effect
                            proc.join() # wait for termination of current effect

                        # create new pipes
                        conn_p, conn_c = Pipe(True)
                        conn_p_options, conn_c_options = Pipe(True)

                        # create and start new effect process
                        proc = Process(
                            target=effect_class.run, args=[
                                matrix, options, conn_c, conn_c_options
                            ]
                        )
                        proc.start()

                        current_options = options
                    elif options != current_options: # if just the options changed
                        conn_p_options.send(options) # send new options via pipe to current effect
                        current_options = options
                time.sleep(1)
            except KeyboardInterrupt:
                self.log.debug("Terminating")

    def run(self, queue: Queue):
        self.log.debug("run method called.")
        self.loop(self.matrix, queue)
