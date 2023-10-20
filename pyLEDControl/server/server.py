import json
from flask import Flask, jsonify, request
from misc.utils import to_json_td
from control.effects import get_effects
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
        def get_all_effects():
            return jsonify(list(get_effects().keys()))
        
        @app.get("/effect/<effect>/options")
        def get_effect_option_parameters(effect:str):
            return jsonify(to_json_td(get_effects()[effect].Options))

        @app.get("/effect/current")
        def get_status():
            return jsonify(
                self.current_options_instance
            )

        @app.post("/effect/<effect>")
        def change_effect(effect:str):
            """ 
            TODO: Modify endpoint: 
            - Backend: Options class should contain neccessary information like brightness etc.
            - Frontend: Build payload 
            """
            try:
                formdata = request.get_json(force=True)
                brightness = formdata["brightness"]
                if brightness > 100 or brightness < 0:
                    return jsonify("brightness must be a interval value in [0;100]")
                self.log.info("Received Effect: " + effect)

                raw_options_data = formdata
                effect_class = get_effects()[effect]
                options_instance = effect_class.Options(**raw_options_data)

                self.queue.put((effect_class, options_instance))
                self.current_effect = effect
                self.current_brightness = brightness
                self.current_options_instance = options_instance
                return jsonify({"status": "success"})
            except Exception as e:
                return jsonify(e)

        self.log.debug("Starting flask server")
        app.run(host="0.0.0.0", port=settings.SERVER_PORT)

    def run(self):
        # Start clock on startup
        effect_dict = get_effects()
        effect_class = effect_dict[self.current_effect]
        self.current_options_instance = effect_class.Options(
            brightness=self.current_brightness, effect=effect_dict[self.current_effect])
        self.queue.put((effect_class,self.current_options_instance))
        self.run_server()
