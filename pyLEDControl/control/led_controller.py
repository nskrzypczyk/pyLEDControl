from misc.logging import Log
from control.adapter.real_matrix import RealMatrix
from control.adapter.emulated_matrix import EmulatedMatrix
import settings
from misc.domain_data import ExecutionMode
from display.rgb_process import MatrixProcess
from multiprocessing import Process, Queue
from control.effects.random_dot import RandomDot
from control.effect_message import EffectMessage


class LedController():

    def start(self) -> Process:
        if settings.MODE == ExecutionMode.EMULATED:
            self.log.debug(f"Starting the Emulator")
            matrix = EmulatedMatrix
        else:
            self.log.debug(f"Starting the Matrix")
            matrix = RealMatrix

        matrix_process = MatrixProcess(matrix)
        proc = Process(target=matrix_process.run, args=[self.queue])
        proc.start()
        return proc

    def __init__(self, queue: Queue) -> Process:
        self.log = Log(__class__.__name__)
        self.log.debug(f"Initializing {__class__.__name__}")
        self.queue = queue
