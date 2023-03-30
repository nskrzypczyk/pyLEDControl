from flask import Flask
from control.led_controller import LedController
import server.server_settings as settings
from misc.logging import Log
from multiprocessing import Process
from control.led_service import LedService


class Server(Process):
    def __init__(self, service: LedService):
        super(Server, self).__init__()
        self.log = Log(__class__.__name__)
        self.led_service = service

    def run_server(self):
        self.log.debug("Setting up flask server")
        app: Flask = Flask("pyLedControlServer")

        @app.get("/")
        def index():
            return "Hello World"

        @app.post("/effect/<effect>")
        def change_effect(effect: str):
            self.log.info("Received Effect: "+effect)
            self.led_service.effect = self.led_service.effect_dict[effect]
            return "Success"

        self.log.debug("Starting flask server")
        app.run(port=settings.PORT)

    def run(self):
        self.run_server()
