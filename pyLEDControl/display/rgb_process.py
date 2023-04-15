import time
import settings
from control.effects.abstract_effect import AbstractEffect
from control.adapter.abstract_matrix import AbstractMatrix
from misc.logging import Log
from control.effect_message import EffectMessage
from multiprocessing import Process, Queue


class MatrixProcess():
    def __init__(self, matrix: AbstractMatrix) -> None:
        self.matrix = matrix
        self.log: Log = Log("RgbEmulator")

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
                        self.log.debug(
                            "Effect has changed. Restarting process")
                        if proc:
                            proc.terminate()
                        proc = Process(
                            target=message.effect.run, args=[matrix])
                        proc.start()
                        current_effect = message.effect
                time.sleep(1)
            except KeyboardInterrupt:
                self.log.debug("Terminating")

    def run(self, queue: Queue):
        matrix = self.matrix(options=settings.rgb_options())
        self.loop(matrix, queue)


if __name__ == "__main__":
    matrix = MatrixProcess()

    def pixel(matrix: AbstractMatrix):
        matrix.SetPixel(1, 1, 10, 20, 30)
    matrix.mode = pixel
    matrix.run()
