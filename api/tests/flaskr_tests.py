import os
import sys
import unittest
import tempfile
from flaskext.mysql import MySQL
from flask import jsonify
import mysql.connector
#Might need to be changed in the ec2 instance
topdir = os.path.join(os.path.dirname(__file__), "C:\\Users\\Vaios\\Desktop\\Dev\\sofaref\\api")
sys.path.append(topdir)
from app import app
import json
from database import create_tables, drop_tables, add_match, add_event, add_media, update, add_user, vote, create_role


mysql = MySQL()
mysql.init_app(app)

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        create_tables()
        

    def tearDown(self):
        drop_tables()

    def test_empty_db(self):
        rv = self.app.get('/getActiveMatches')
        #print(rv.data)
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data), 0)
        

    def test_get_active(self):
        add_match(0,0)
        add_match(1,1)
        rv = self.app.get('/getActiveMatches')
        #print(rv.data)
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], 1)
        self.assertEqual(data[0][1], 'Sat, 21 Jan 2017 10:10:10 GMT')
        self.assertEqual(data[0][2], 'Arsenal')
        self.assertEqual(data[0][3], 'Hull')
        self.assertEqual(data[0][4], 'BPL')
        self.assertEqual(data[0][5], 1)
        update(0,'matches')
        rv = self.app.get('/getActiveMatches')
        data = json.loads(rv.get_data(as_text=True))
        #print(data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0][0], 0)
        self.assertEqual(data[0][1], 'Sun, 21 Jan 2018 10:10:10 GMT')
        self.assertEqual(data[0][2], 'Changed team a')
        self.assertEqual(data[0][3], 'Changed team b')
        self.assertEqual(data[0][4], 'Changed competition')
        self.assertEqual(data[0][5], 1)   

        #assert b'No entries here so far' in rv.data
    def test_get_events(self):
        add_match(0,0)
        add_event(0,0)
        rv = self.app.get('/getEventsForMatchId/0')
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data),1)
        self.assertEqual(data[0][0], 0)
        self.assertEqual(data[0][1], 'Sat, 21 Jan 2017 10:10:10 GMT')
        self.assertEqual(data[0][2], 'Arsenal')
        self.assertEqual(data[0][3], 'Hull')
        self.assertEqual(data[0][4], 'BPL')
        self.assertEqual(data[0][5], 0)
        self.assertEqual(data[0][6], 0)
        self.assertEqual(data[0][7], 'Sample description')
        self.assertEqual(data[0][8], 'Sample question')
        add_event(1,0)
        add_match(1,0)
        update(1, 'events')
        rv = self.app.get('/getEventsForMatchId/1')
        data = json.loads(rv.get_data(as_text=True))
        #print(data)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0][0], 1)
        self.assertEqual(data[0][1], 'Sat, 21 Jan 2017 10:10:10 GMT')
        self.assertEqual(data[0][2], 'Arsenal')
        self.assertEqual(data[0][3], 'Hull')
        self.assertEqual(data[0][4], 'BPL')
        self.assertEqual(data[0][5], 0)
        self.assertEqual(data[0][6], 1)
        self.assertEqual(data[0][7], 'Changed description')
        self.assertEqual(data[0][8], 'Changed question')

    def test_get_votes(self):
        create_role()
        add_user(0)
        add_match(0,0)
        add_event(0,0)
        vote(0,0,0)
        rv = self.app.get('/getVotesForEventId/0')
        # returns vote id , user id, vote, event id / vote is always 1
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data),1)
        self.assertEqual(data[0][0], 0)
        self.assertEqual(data[0][1], 0)
        self.assertEqual(data[0][2], 1)
        self.assertEqual(data[0][3], 0)
        add_user(1)
        vote(1,1,0)
        rv = self.app.get('/getVotesForEventId/0')
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data),2)

    def test_media(self):
        add_match(0,0)
        add_event(0,0)
        add_media(0,0)
        rv = self.app.get('/getMediaForEventId/0')
        # returns media id, event id , media type, media url / media type for test is always 0
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data),1)
        self.assertEqual(data[0][0], 0)
        self.assertEqual(data[0][1], 0)
        self.assertEqual(data[0][2], 0)
        self.assertEqual(data[0][3], 'Sample url')
        add_event(1,0)
        update(0,'media')
        rv = self.app.get('/getMediaForEventId/1')
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data),1)
        self.assertEqual(data[0][0], 0)
        self.assertEqual(data[0][1], 1)
        self.assertEqual(data[0][2], 1)
        self.assertEqual(data[0][3], 'Changed url')




if __name__ == '__main__':
    unittest.main()