import logging
from enum import Enum
from misc.domain_data import ExecutionMode

SERVER_PORT: int = 8080
LOG_LEVEL: logging._nameToLevel = "DEBUG"
ENABLE_STDOUT: bool = True
MODE = ExecutionMode.EMULATED


class MATRIX_EMULATION(Enum):
    HEIGHT: int = 64
    WIDTH: int = 64
