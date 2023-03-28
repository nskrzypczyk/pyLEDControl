from flask import Flask
from control.led_controller import LedController
import server.server_settings as settings
from server.controller.led_control import led_control
from misc.logging import Log

log = Log("server")


def start_matrix():
    log.debug("Starting up the matrix")
    led_controller = LedController()


def run_server() -> Flask:
    start_matrix()

    log.debug("Setting up flask server")
    server: Flask = Flask("pyLedControlServer")

    log.debug("Registering ledControl blueprint")
    server.register_blueprint(led_control, url_prefix=settings.BASE_ROUTE)

    log.debug("Starting flask server")
    server.run(port=settings.PORT)
    return server
