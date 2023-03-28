from misc.logging import Log
import settings
from misc.domain_data import ExecutionMode
from display.RGB_Emulator import RgbEmulator
from multiprocessing import Process
from control.effects.random_dot import RandomDot


class LedController():
    matrix: RgbEmulator

    def start_emulator(self) -> None:
        self.log.debug("Starting the Emulator")
        self.matrix = RgbEmulator()
        self.matrix.effect = RandomDot().build()
        self.matrix.run()

    def start_rgb_matrix(self) -> None:
        pass

    def __init__(self) -> None:
        self.log = Log(__class__.__name__)
        self.log.debug(f"Initializing {__class__.__name__}")
        if settings.ExecutionMode == ExecutionMode.EMULATED:
            self.start_emulator()
        else:
            self.start_rgb_matrix()
