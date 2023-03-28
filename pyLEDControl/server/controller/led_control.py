from flask import Blueprint
from control.led_controller import LedController

led_control = Blueprint("led_control", __name__)


@led_control.get("/")
def index():
    return "Welcome to pyLEDControl!"
