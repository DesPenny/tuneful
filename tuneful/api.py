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
        "song_file_id": {"type": "string"}
    },
    "required": ["id", "song_file_id"]
}

@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def songs_get():
    """ Get a list of songs """
    
    songs = session.query(models.Song)
    

    # Convert the posts to JSON and return a response
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")
  
@app.route("/api/songs/<int:id>", methods=["GET"])
@decorators.accept("application/json")
def single_song_get(id):
    """ Get a single song """
    
    song = session.query(models.Song).get(id)
    
    # Check whether the post exists
    # If not return a 404 with a helpful message
    if not song:
        message = "Could not find song with id {}".format(id)
        data = json.dumps({"message": message})
        return Response(data, 404, mimetype="application/json")

    # Return the post as JSON
    data = json.dumps(song.as_dictionary())
    return Response(data, 200, mimetype="application/json")