import json
from flask import Flask, jsonify, request
from control.abstract_effect_options import AbstractEffectOptions
from control.effects import effect_dict
from control.effects.effect_message_builder import EffectMessageBuilder
import settings
from misc.logging import Log
from multiprocessing import Process, Queue
from flask_cors import CORS


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
        CORS(app)

        @app.get("/")
        def index():
            return "Hello World"

        @app.get("/effect/available")
        def get_effects():
            return jsonify(list(effect_dict.keys()))

        @app.get("/effect/current")
        def get_current_effect():
            return jsonify(
                {"effect": self.current_effect, "brightness": self.current_brightness}
            )

        @app.post("/effect/<effect>/<int:brightness>")
        def change_effect(effect: str, brightness: int):
            """ 
            TODO: Modify endpoint: 
            - Backend: Options class should contain neccessary information like brightness etc.
            - Frontend: Build payload 
            """
            if brightness > 100 or brightness < 0:
                return jsonify("brightness must be a interval value in [0;100]")
            try:
                self.log.info("Received Effect: " + effect)

                raw_options_data = json.loads(request.json)
                options_instance = effect_dict[effect].Options(**raw_options_data)

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
        message = (
            EffectMessageBuilder()
            .set_effect(self.current_effect)
            .set_brightness(self.current_brightness)
            .build()
        )
        self.queue.put(message)
        self.run_server()
