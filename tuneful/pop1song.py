from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session
from tuneful.models import Song, File
from tuneful.database import session

def pop1():
        fileA = models.File(filename="FileA.mp3")
        fileB = models.File(filename="FileB.mp3")

        session.add_all([fileA, fileB])
        session.commit()
        
        songA = models.Song(song_file_id= fileA.id)
        songB = models.Song(song_file_id= fileB.id)

        session.add_all([songA, songB])
        session.commit()