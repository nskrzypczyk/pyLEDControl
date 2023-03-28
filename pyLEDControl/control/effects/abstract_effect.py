from RGBMatrixEmulator import RGBMatrix
from abc import ABC, abstractmethod


class AbstractEffect(ABC):
    @abstractmethod
    def build(self) -> ABC:
        """Prepares the necessary data which will be then passed to the respective controller to display the effect / mode"""
        pass

    @abstractmethod
    def run(self, matrix: RGBMatrix):
        """Runs the effect"""
        pass
