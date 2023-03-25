from flask import Flask
import server.server_settings as settings
from server.controller.ledControl import ledControl
from misc.logging import Log

log = Log("server")


def run_server() -> Flask:
    log.debug("Setting up flask server")
    server: Flask = Flask("pyLedControlServer")

    log.debug("Registering ledControl blueprint")
    server.register_blueprint(ledControl, url_prefix=settings.BASE_ROUTE)

    log.debug("Starting flask server")
    server.run(port=settings.PORT)
    return server
