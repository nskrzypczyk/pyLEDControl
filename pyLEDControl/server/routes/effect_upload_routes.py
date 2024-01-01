import os

import yaml
from flask import Blueprint, jsonify, redirect, request
from werkzeug.utils import secure_filename

from control.effects.abstract.uploaded_effect import get_uploaded_effects

UPLOAD_DIR: str = "uploads"
CONF_DIR: str = "uploads_effect_config"
ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "gif"}

upload_bp = Blueprint("upload", __name__)
file_paths: list = []


@upload_bp.before_app_first_request
def load_existing_file_paths():
    global file_paths
    file_paths = load_file_paths()


@upload_bp.route("/add", methods=["POST"])
def add_effect():
    file = request.files["file"]
    effect_name = request.form.get("effect_name", default="")
    
    if file.filename == "" or effect_name == "":
        return jsonify(error="Effect and file names must not be null!"), 400

    if file and is_file_allowed(file.filename):
        filename = secure_filename(file.filename)
        _, file_extension = os.path.splitext(filename)
        file_path = os.path.join(UPLOAD_DIR, effect_name+file_extension)

        os.makedirs(UPLOAD_DIR, exist_ok=True)

        if os.path.exists(file_path):
            return jsonify(error="Effect with this name already exists!"), 400

        file.save(file_path)
        return jsonify("File uploaded successfully"), 200
    else:
        return jsonify(error=f"Invalid file format. Allowed formats are {ALLOWED_EXTENSIONS}"), 400


@upload_bp.route("/get/all", methods=["GET"])
def get_uploaded_custom_effects():
    try:
        return jsonify(get_uploaded_effects())
    except Exception as e:
        return jsonify(e)


@upload_bp.route("/delete/<effect_name>", methods=["DELETE"])
def delete_effect(effect_name):
    # Construct the full file path
    file_path = os.path.join(UPLOAD_DIR, effect_name)

    # Check if the file exists
    if os.path.exists(file_path):
        # Remove the file
        os.remove(file_path)

        # Remove the entry from the file_paths list
        file_paths.remove(file_path)

        # Save updated file paths to YAML file
        save_file_paths()

        return f"Effect {effect_name} deleted successfully"
    else:
        return f"Effect {effect_name} not found"


def is_file_allowed(filename) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def load_file_paths():
    if os.path.exists(CONF_DIR):
        with open(CONF_DIR, "r") as file:
            return yaml.safe_load(file) or []
    return []


def save_file_paths():
    with open(CONF_DIR, "w") as file:
        yaml.dump(file_paths, file)
