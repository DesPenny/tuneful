from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session
from tuneful.models import Song, File
from tuneful.database import session
#from flask.ext.script import Manager

#@manager.command
"""def pop1():
        fileA = models.File(filename="FileA.mp3")
        fileB = models.File(filename="FileB.mp3")

        session.add_all([fileA, fileB])
        session.commit()
        
        songA = models.Song(song_file_id= fileA.id)
        songB = models.Song(song_file_id= fileB.id)

        session.add_all([songA, songB])
        session.commit()
        
        songs = session.query(models.Song).all()
        return songs
      
        print songs
        """
def testSongPost(self):
        """ Posting a new song """
        fileA = models.File(filename="FileA.mp3")
        session.add(fileA)
        session.commit()
        
        data = {
            "file": {
                  "id": fileA.id
                    }
        }

        response = self.client.post("/api/songs",
            data=json.dumps(data),
            content_type="application/json",
            headers=[("Accept", "application/json")]
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, "application/json")
        self.assertEqual(urlparse(response.headers.get("Location")).path,
                         "/api/songs")

        data = json.loads(response.data)
        #self.assertEqual(data["id"], fileA.id)
        
        songs = session.query(models.Song).all()
        #self.assertEqual(len(songs), 1)

        song = songs[0]
        #self.assertEqual(song.id, fileA.id)
        print song