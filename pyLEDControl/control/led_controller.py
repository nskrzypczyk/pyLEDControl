import settings
from misc.domain_data import ExecutionMode
from display.RGB_Emulator import RgbEmulator
from multiprocessing import Process


class LedController():
    matrix: RgbEmulator

    def start_emulator(self) -> None:
        self.matrix = RgbEmulator()
        # TODO: make the rgb-emulator a "multiprocessing" process and use a shared variable

    def start_rgb_matrix(self) -> None:
        pass

    def __init__(self) -> None:
        if settings.ExecutionMode == ExecutionMode.EMULATED:
            self.start_emulator()
        else:
            self.start_rgb_matrix()
