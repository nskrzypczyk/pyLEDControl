from flask import Flask, jsonify
from control.led_controller import LedController
from control.effect_message import EffectMessage
import server.server_settings as settings
from misc.logging import Log
from multiprocessing import Process, Queue


class Server(Process):
    def __init__(self, queue: Queue):
        super(Server, self).__init__()
        self.log = Log(__class__.__name__)
        self.queue = queue

    def run_server(self):
        self.log.debug("Setting up flask server")
        app: Flask = Flask("pyLedControlServer")

        @app.get("/")
        def index():
            return "Hello World"

        @app.post("/effect/<effect>")
        def change_effect(effect: str):
            self.log.info("Received Effect: "+effect)
            message = EffectMessage().set_effect(effect).set_effect_changed(True)
            self.queue.put(message)
            return jsonify({"status": "success"})

        self.log.debug("Starting flask server")
        app.run(port=settings.PORT)

    def run(self):
        self.run_server()
