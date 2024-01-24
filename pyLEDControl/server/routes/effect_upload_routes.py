import requests
from misc.logging import Log
import os

import yaml
from flask import Blueprint, jsonify, redirect, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import io

# TODO: Introduce settings for custom effects
# TODO: Add PUT route for updating an existing custom effect
UPLOAD_DIR: str = "uploads"
CONF_DIR: str = "uploads_effect_config"
ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "gif"}
YAML_EXTENSION = ".yaml"

upload_bp = Blueprint("upload", __name__)
log = Log(__name__)
file_paths: list = []
custom_effects_with_settings = {}


@upload_bp.before_app_first_request
def load_existing_file_paths():
    global file_paths, custom_effects_with_settings
    custom_effects_with_settings = {}
    file_paths = load_conf_file_paths()
    for path in file_paths:
        settings_file = yaml.safe_load(open(path))
        custom_effects_with_settings[settings_file.get("name", "")] = settings_file.get(
            "settings", None
        )
    log.debug([file_paths, custom_effects_with_settings])
    return custom_effects_with_settings


@upload_bp.route("/add", methods=["POST"])
def add_effect():
    file = request.files.get("file")
    effect_name = request.form.get("effect_name", default="").strip()

    if file is None or file.filename == "" or effect_name == "":
        return jsonify(error="Effect name and file must not be null!"), 400
    
    if file and is_file_allowed(file.filename):
        filename = secure_filename(file.filename)
        _, file_extension = os.path.splitext(filename)
        file_path = os.path.join(UPLOAD_DIR, effect_name + file_extension)

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        if os.path.exists(file_path):
            return jsonify(error="Effect with this name already exists!"), 400

        file.save(file_path)

        # write yaml config
        with open_conf_file(effect_name) as conf_file:
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

        load_existing_file_paths()
        return jsonify("File uploaded successfully"), 200
    else:
        return (
            jsonify(
                error=f"Invalid file format. Allowed formats are {ALLOWED_EXTENSIONS}"
            ),
            400,
        )


@upload_bp.route("/add/url", methods=["POST"])
def add_effect_url():
    effect_url = request.form.get("url", default="")
    effect_name = request.form.get("effect_name", default="").strip()

    if effect_url == "" or effect_name == "":
        return jsonify(error="Effect name and file must not be null!"), 400

    try:
        response = requests.get(effect_url)
        response.raise_for_status()
        content_type = response.headers["Content-Type"]

        if "image/gif" in content_type:
            file_extension = ".gif"
        elif "image/png" in content_type:
            file_extension = ".png"
        elif "image/jpeg" in content_type:
            file_extension = ".jpg"
        else:
            return jsonify(
                f"The URL '{effect_url}' does not point to a supported file. Content-Type: {response.headers['Content-Type']}",
                400,
            )

        file = FileStorage(
            stream=io.BytesIO(response.content),
            filename=effect_name+file_extension,
            content_type=content_type,
        )

    except requests.RequestException as e:
        jsonify(f"Error while processing the URL: {e}"), 500

    if file and is_file_allowed(file.filename):
        filename = secure_filename(file.filename)
        _, file_extension = os.path.splitext(filename)
        file_path = os.path.join(UPLOAD_DIR, effect_name + file_extension)

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        if os.path.exists(file_path):
            return jsonify(error="Effect with this name already exists!"), 400

        file.save(file_path)

        # write yaml config
        with open_conf_file(effect_name) as conf_file:
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

        load_existing_file_paths()
        return jsonify("File uploaded successfully"), 200
    else:
        return (
            jsonify(
                error=f"Invalid file format. Allowed formats are {ALLOWED_EXTENSIONS}"
            ),
            400,
        )


def open_conf_file(effect_name, read=False):
    if not os.path.exists(CONF_DIR):
        os.makedirs(CONF_DIR)
    return open(
        os.path.join(CONF_DIR, str(effect_name) + YAML_EXTENSION), "r" if read else "w"
    )


def load_yaml_file_as_dict(effect_name, read=False) -> dict:
    return yaml.safe_load(open_conf_file(effect_name, read))


@upload_bp.route("/get/all", methods=["GET"])
def get_uploaded_custom_effects():
    try:
        return jsonify(list(custom_effects_with_settings.keys())), 200
    except Exception as e:
        return jsonify(e), 500


@upload_bp.route("/delete/<effect_name>", methods=["DELETE"])
def delete_effect(effect_name):
    # Construct the full file paths for src and conf
    conf_path = get_effect_conf_path(effect_name)
    if os.path.exists(conf_path):
        src_path = yaml.safe_load(open(conf_path, "r")).get("source", None)
        # Check if the files exists
        if os.path.exists(src_path):
            # Remove the files
            os.remove(src_path)
            os.remove(conf_path)
            # Remove any pickled gif frames
            pkl_path = src_path.replace(".gif", ".pkl")
            if os.path.exists(pkl_path):
                os.remove(pkl_path)

            load_existing_file_paths()
            return jsonify(f"Effect {effect_name} deleted successfully"), 200

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
