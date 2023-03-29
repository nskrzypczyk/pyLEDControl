from flask import Flask
from control.led_controller import LedController
import server.server_settings as settings
from misc.logging import Log
from multiprocessing import Process
from control.led_service import LedService


log = Log("server")


class Server(Process):
    def __init__(self, service: LedService):
        super(Server, self).__init__()
        self.led_service = service

    def run_server(self):
        log.debug("Setting up flask server")
        app: Flask = Flask("pyLedControlServer")

        @app.get("/")
        def index():
            return "Hello World"

        log.debug("Starting flask server")
        app.run(port=settings.PORT)

    def run(self):
        self.run_server()
