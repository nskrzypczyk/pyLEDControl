from misc.logging import Log
import settings
from misc.domain_data import ExecutionMode
from display.RGB_Emulator import RgbEmulator
from multiprocessing import Process
from control.effects.random_dot import RandomDot
from control.led_service import LedService


class LedController():
    matrix: RgbEmulator

    def start_emulator(self) -> Process:
        self.log.debug("Starting the Emulator")
        self.matrix = RgbEmulator()
        proc = Process(target=self.matrix.run, args=[self.led_service])
        proc.start()
        return proc

    def start_rgb_matrix(self) -> Process:
        # FIXME: Implement when parts arrive!
        raise NotImplementedError("Method is yet to be implemented")

    def start(self) -> Process:
        if settings.MODE == ExecutionMode.EMULATED:
            return self.start_emulator()
        else:
            return self.start_rgb_matrix()

    def __init__(self, service: LedService) -> Process:
        self.log = Log(__class__.__name__)
        self.log.debug(f"Initializing {__class__.__name__}")
        self.led_service = service
