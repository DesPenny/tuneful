import unittest
import os
import shutil
import json
from urlparse import urlparse
from StringIO import StringIO

import sys; print sys.modules.keys()
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())

    def testGetEmptySongs(self):
        """ Getting songs from an empty database """
        response = self.client.get("/api/songs",
                                   headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data)
        self.assertEqual(data, [])    

    def testGetSongs(self):
        """ Getting songs from a populated database """
        fileA = models.File(filename="FileA.mp3")
        fileB = models.File(filename="FileB.mp3")

        session.add_all([fileA, fileB])
        session.commit()
        
        songA = models.Song(song_file_id= fileA.id)
        songB = models.Song(song_file_id= fileB.id)

        session.add_all([songA, songB])
        session.commit()
        
        response = self.client.get("/api/songs",
                                   headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")
        
        data=json.loads(response.data)
        
        # Test number of songs
        songs = session.query(models.Song).all()
        self.assertEqual(len(songs), 2)

        songA = data[0]
        self.assertEqual(songA["id"], songA["file"]["id"])
        self.assertEqual(songA["file"]["name"], "FileA.mp3")

        songB = data[1]
        self.assertEqual(songB["id"], songB["file"]["id"])
        self.assertEqual(songB["file"]["name"], "FileB.mp3")
        
    def test_get_single_song(self):
        """ Getting a single song from the database """
        fileA = models.File(filename="FileA.mp3")
        session.add(fileA)
        session.commit()

        songA = models.Song(song_file_id=fileA.id)
        session.add(songA)
        session.commit()

        response = self.client.get("/api/songs/{}".format(songA.id),
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        song = json.loads(response.data)
        self.assertEqual(song["id"], song["file"]["id"])
        self.assertEqual(song["file"]["name"], "FileA.mp3")
    
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
        self.assertEqual(data["id"], fileA.id)
        
        songs = session.query(models.Song).all()
        self.assertEqual(len(songs), 1)

        song = songs[0]
        self.assertEqual(song.id, fileA.id)
        
    def test_delete_single_song(self):
        """ Deleting a single song from the database """
        fileA = models.File(filename="FileA.mp3")
        session.add(fileA)
        session.commit()

        songA = models.Song(song_file_id=fileA.id)
        session.add(songA)
        session.commit()

        response = self.client.delete("/api/songs/{}".format(songA.id),
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/json")

        songs = session.query(models.Song).all()
        self.assertEqual(len(songs), 0)
    
    def test_get_uploaded_file(self):
        path =  upload_path("test.txt")
        with open(path, "w") as f:
            f.write("File contents")

        response = self.client.get("/uploads/test.txt")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/plain")
        self.assertEqual(response.data, "File contents")
        
    def test_file_upload(self):
        data = {
            "file": (StringIO("File contents"), "test.txt")
        }

        response = self.client.post("/api/files",
            data=data,
            content_type="multipart/form-data",
            headers=[("Accept", "application/json")]
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data)
        self.assertEqual(urlparse(data["path"]).path, "/uploads/test.txt")

        path = upload_path("test.txt")
        self.assertTrue(os.path.isfile(path))
        with open(path) as f:
            contents = f.read()
        self.assertEqual(contents, "File contents")
        
    def test_update_single_song(self):
        """ Testing update a song """
        # First, create a new post
        fileB = models.File(filename="FileB.mp3")
        data_inject = {
            "file": {
                  "id": fileB.id
                    }
        }
        
        fileA = models.File(filename="FileA.mp3")
        

        session.add_all([fileA])
        session.commit()
        
        songA = models.Song(song_file_id= fileA.id)
        songB = models.Song(song_file_id= fileB.id)
        session.add_all([songA])
        session.commit()
  
        #Now edit the post with new data
        response = self.client.put("/api/songs/{}".format(songA.id),
                                      data=json.dumps(data_inject),
                                      content_type="application/json",
                                      headers=[("Accept", "application/json")])
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, "application/json")

        data=json.loads(response.data)
        
        # Test that it contains the new data
        
        self.assertEqual(data["id"], fileB.id)
        
        songs = session.query(models.Song).all()
        self.assertEqual(len(songs), 1)

        song = songs[0]
        self.assertEqual(song.id, fileB.id)
if __name__ == "__main__":
    unittest.main()