from RGBMatrixEmulator import RGBMatrixOptions as RGBMatrixOptionsEmulated
import logging
from enum import Enum
from misc.domain_data import ExecutionMode
from rgbmatrix import RGBMatrixOptions

SERVER_PORT: int = 8080
LOG_LEVEL: logging._nameToLevel = "DEBUG"
ENABLE_STDOUT: bool = True
MODE = ExecutionMode.REAL


class MATRIX_DIMENSIONS(Enum):
    HEIGHT: int = 64
    WIDTH: int = 64


def rgb_options():
    if MODE == ExecutionMode.EMULATED:
        rgb_options = RGBMatrixOptionsEmulated()
        rgb_options.pixel_size = 16
        rgb_options.pixel_style = "square"
        rgb_options.rows = MATRIX_DIMENSIONS.HEIGHT.value
        rgb_options.cols = MATRIX_DIMENSIONS.WIDTH.value
        return rgb_options
    elif MODE == ExecutionMode.REAL:
        rgb_options = RGBMatrixOptions()
        rgb_options.rows = 64
        rgb_options.cols = 64
        rgb_options.hardware_mapping = "adafruit-hat"
        # rgb_options.chain_length = 1
        # rgb_options.parallel = 1
        # rgb_options.row_address_type = 1
        # rgb_options.multiplexing = 0
        # rgb_options.pwm_bits = 11
        # rgb_options.brightness = 100
        # rgb_options.pwm_lsb_nanoseconds = 130
        # rgb_options.led_rgb_sequence = "RGB"
        # rgb_options.pixel_mapper_config = ""
        # rgb_options.panel_type = ""
        return rgb_options
    raise RuntimeError(f"Invalid execution mode {MODE}")
