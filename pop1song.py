import os
from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session
from tuneful.models import Song, File
from tuneful.database import session


os.environ["CONFIG_PATH"] = "tuneful.config.DevelopmentConfig"


def create_new_songs(self):
        fileA = models.File(id=1,filename="FileA.mp3")
        fileB = models.File(id=2,filename="FileB.mp3")

        session.add_all([fileA, fileB])
        
        
        songA = models.Song(id=1,song_file_id=fileA.id)
        songB = models.Song(id=2,song_file_id=fileB.id)

        session.add_all([songA, songB])
        session.commit()
        
        
