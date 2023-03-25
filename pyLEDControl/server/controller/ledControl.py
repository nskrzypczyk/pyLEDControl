from flask import Blueprint

ledControl = Blueprint("ledControl", __name__)


@ledControl.get("/")
def index():
    return "Welcome to pyLEDControl!"
