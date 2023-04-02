from RGBMatrixEmulator import RGBMatrix
from abc import ABC, abstractmethod


class AbstractEffect(ABC):
    @staticmethod
    @abstractmethod
    def run(matrix: RGBMatrix):
        """Runs the effect"""
        pass
