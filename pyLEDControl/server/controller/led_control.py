from flask import Blueprint

led_control = Blueprint("led_control", __name__)


@led_control.get("/")
def index():
    return "Welcome to pyLEDControl!"
