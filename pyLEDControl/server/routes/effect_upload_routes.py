from misc.logging import Log
import os

import yaml
from flask import Blueprint, jsonify, redirect, request
from werkzeug.utils import secure_filename

# TODO: Introduce settings for custom effects
# TODO: Add PUT route for updating an existing custom effect

UPLOAD_DIR: str = "uploads"
CONF_DIR: str = "uploads_effect_config"
ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "gif"}
YAML_EXTENSION = ".yaml"

upload_bp = Blueprint("upload", __name__)
log = Log(__name__)
file_paths: list = []
custom_effects_names = []


@upload_bp.before_app_first_request
def load_existing_file_paths():
    global file_paths, custom_effects_names
    file_paths = load_conf_file_paths()
    custom_effects_names = [
        yaml.safe_load(open(path)).get("name", "") for path in file_paths
    ]
    log.debug([file_paths, custom_effects_names])


@upload_bp.route("/add", methods=["POST"])
def add_effect():
    file = request.files["file"]
    effect_name = request.form.get("effect_name", default="")

    if file.filename == "" or effect_name == "":
        return jsonify(error="Effect and file names must not be null!"), 400

    if file and is_file_allowed(file.filename):
        filename = secure_filename(file.filename)
        _, file_extension = os.path.splitext(filename)
        file_path = os.path.join(UPLOAD_DIR, effect_name + file_extension)

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        if os.path.exists(file_path):
            return jsonify(error="Effect with this name already exists!"), 400

        file.save(file_path)

        # write yaml config
        with open(
            os.path.join(CONF_DIR, effect_name + YAML_EXTENSION), "w"
        ) as conf_file:
            yaml.dump(
                yaml.safe_load(
                    f"""
                    name: {effect_name}
                    source: {file_path}
                    settings: 
                    """
                ),
                conf_file,
            )

        return jsonify("File uploaded successfully"), 200
    else:
        return (
            jsonify(
                error=f"Invalid file format. Allowed formats are {ALLOWED_EXTENSIONS}"
            ),
            400,
        )


@upload_bp.route("/get/all", methods=["GET"])
def get_uploaded_custom_effects():
    try:
        return jsonify(custom_effects_names), 200
    except Exception as e:
        return jsonify(e), 500


@upload_bp.route("/delete/<effect_name>", methods=["DELETE"])
def delete_effect(effect_name):
    # Construct the full file paths for src and conf
    conf_path = get_effect_conf_path(effect_name)
    src_path = yaml.safe_load(open(conf_path, "r")).get("source", None)

    # Check if the files exists
    if os.path.exists(src_path) and os.path.exists(conf_path):
        # Remove the files
        os.remove(src_path)
        os.remove(conf_path)

        return jsonify(f"Effect {effect_name} deleted successfully"), 200
    else:
        return jsonify(f"Effect {effect_name} not found"), 404


def is_file_allowed(filename) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def load_conf_file_paths():
    if os.path.exists(CONF_DIR):
        return [
            os.path.join(CONF_DIR, file_name)
            for file_name in os.listdir(CONF_DIR)
            if os.path.isfile(os.path.join(CONF_DIR, file_name))
        ]
    return []


def get_effect_conf_path(effect_name: str) -> str:
    return os.path.join(CONF_DIR, effect_name + YAML_EXTENSION)
