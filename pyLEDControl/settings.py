import logging
from enum import Enum

SERVER_PORT: int = 8080
LOG_LEVEL: logging._nameToLevel = "DEBUG"
ENABLE_STDOUT: bool = True


class MATRIX_EMULATION(Enum):
    HEIGHT = 64
    WIDTH = 64
