import os

import yaml
from flask import Blueprint, jsonify, redirect, request
from werkzeug.utils import secure_filename

UPLOAD_DIR: str = "uploads"
CONF_DIR: str = "uploads_effect_config"
ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "gif"}

upload_bp = Blueprint("upload", __name__)
file_paths: list = []


@upload_bp.before_app_first_request
def load_existing_file_paths():
    global file_paths
    file_paths = load_file_paths()


@upload_bp.route(methods=("POST"))
def upload_custom_effect():
    if "file" not in request.files:
        return redirect(request.url)

    file = request.files["file"]

    if file.filename == "":
        return redirect(request.url)

    if file and is_file_allowed(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return "File uploaded successfully"
    else:
        return "Invalid file format. Allowed formats are jpg, jpeg, png, and gif."


@upload_bp.route(methods=("GET"))
def get_uploaded_effects():
    try:
        return jsonify(get_uploaded_effects())
    except Exception as e:
        return jsonify(e)


@upload_bp.route("/delete/<filename>", methods=["GET"])
def delete_file(filename):
    # Construct the full file path
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Check if the file exists
    if os.path.exists(file_path):
        # Remove the file
        os.remove(file_path)

        # Remove the entry from the file_paths list
        file_paths.remove(file_path)

        # Save updated file paths to YAML file
        save_file_paths()

        return f"File {filename} deleted successfully"
    else:
        return f"File {filename} not found"


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
