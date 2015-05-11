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

    def testGetSong(self):
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
        
if __name__ == "__main__":
    unittest.main()