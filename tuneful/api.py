import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

import models
import decorators
from tuneful import app
from database import session
from utils import upload_path

# JSON Schema describing the structure of a song
song_schema = {
    "properties": {
        "id" : {"type" : "integer"},
        "song_file": {"type": "string"}
    },
    "required": ["id", "song_file"]
}

@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def songs_get():
    """ Get a list of songs """
    
    songs = session.query(models.Song)
    

    # Convert the posts to JSON and return a response
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")
