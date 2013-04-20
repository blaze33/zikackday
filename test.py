#!/usr/bin/env python

"""Tests for the Flask Heroku template."""

import json
import unittest
from app import app
from modules.store.storage import redis
from modules.playlist.models import Playlist, Track


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home_page_works(self):
        rv = self.app.get('/')
        self.assertTrue(rv.data)
        self.assertEquals(rv.status_code, 200)

    def test_about_page_works(self):
        rv = self.app.get('/about/')
        self.assertTrue(rv.data)
        self.assertEquals(rv.status_code, 200)

    def test_default_redirecting(self):
        rv = self.app.get('/about')
        self.assertEquals(rv.status_code, 301)

    def test_404_page(self):
        rv = self.app.get('/i-am-not-found/')
        self.assertEquals(rv.status_code, 404)

    def test_static_text_file_request(self):
        rv = self.app.get('/robots.txt')
        self.assertTrue(rv.data)
        self.assertEquals(rv.status_code, 200)

    # API tests
    def test_playlist_resource(self):
        # create a new playlist
        rv = self.app.put('/api/test_playlist/')
        self.assertTrue(rv.data)
        self.assertEquals(rv.status_code, 200)
        playlist = json.loads(rv.data)
        # get the playlist and compare results
        rv = self.app.get('/api/test_playlist/')
        self.assertTrue(rv.data)
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(json.loads(rv.data), playlist)
        #delete test_playlist
        redis.delete('test_playlist')

    def test_tracks_resource(self):
        # create a new playlist
        playlist = Playlist('test_playlist', create=True)
        # add tracks to the playlist
        rv = self.app.put('/api/test_playlist/1/')
        self.assertTrue(rv.data)
        self.assertEquals(rv.status_code, 200)
        track = json.loads(rv.data)
        # get the track and compare results
        rv = self.app.get('/api/test_playlist/1/')
        self.assertTrue(rv.data)
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(json.loads(rv.data), track)
        #delete test_playlist
        redis.delete('test_playlist')
        redis.delete(playlist.uuid)

    def test_tracks_vote(self):
        name = 'test_playlist'
        playlist = Playlist(name, create=True)
        track = Track(playlist.name, 1, create=True)
        self.assertEquals(track.score, 1)
        track.increment_score()
        self.assertEquals(track.score, 2)
        rv = self.app.put('/api/test_playlist/1/', data={'increment': True})
        self.assertTrue(rv.data)
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(json.loads(rv.data)['score'], 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
