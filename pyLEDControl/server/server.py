from flask import Flask, jsonify
from control.effect_message import EffectMessage, effect_list
import settings
from misc.logging import Log
from multiprocessing import Process, Queue


class Server(Process):
    def __init__(self, queue: Queue):
        super(Server, self).__init__()
        self.log = Log(__class__.__name__)
        self.queue = queue

        self.current_effect = "DigiClock"
        self.current_brightness = 100

    def run_server(self):
        self.log.debug("Setting up flask server")
        app: Flask = Flask("pyLedControlServer")

        @app.get("/")
        def index():
            return "Hello World"

        @app.get("/effect/available")
        def get_effects():
            return jsonify(effect_list)

        @app.get("/effect/current")
        def get_current_effect():
            return jsonify({
                "effect": self.current_effect,
                "brightness": self.current_brightness
            })

        @app.post("/effect/<effect>/<int:brightness>")
        def change_effect(effect: str, brightness: int):
            if brightness > 100 or brightness < 0:
                return jsonify("brightness must be a interval value in [0;100]")
            try:
                self.log.info("Received Effect: " + effect)
                message = EffectMessage().set_effect(effect).set_brightness(brightness)
                self.queue.put(message)
                self.current_effect = effect
                self.current_brightness = brightness
                return jsonify({"status": "success"})
            except Exception as e:
                return jsonify(e)

        self.log.debug("Starting flask server")
        app.run(host="0.0.0.0", port=settings.SERVER_PORT)

    def run(self):
        # Start clock on startup
        message = EffectMessage().set_effect(
            self.current_effect).set_brightness(self.current_brightness)
        self.queue.put(message)
        self.run_server()
