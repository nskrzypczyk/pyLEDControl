from flask import Blueprint, redirect, request
from werkzeug.utils import secure_filename
import os

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}

upload_bp = Blueprint("upload", __name__)

@upload_bp("/upload")
def upload_custom_effect():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and is_file_allowed(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return 'File uploaded successfully'
    else:
        return 'Invalid file format. Allowed formats are jpg, jpeg, png, and gif.'

@upload_bp
def get_uploaded_effects():
    pass

def is_file_allowed(filename)->bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS