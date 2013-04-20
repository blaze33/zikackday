import base64
import uuid
from flask import request
from flask.ext.restful import Resource
from flask.ext.restful import Resource, fields, marshal_with
from modules.store.storage import redis
from modules.tools.utilities import get_a_Uuid
from modules.playlist.models import Playlist, Track

resource_fields = {
    'name': fields.String,
    'uuid': fields.String,
}

class PlaylistResource(Resource):
    url = '/<string:name>/'

    # @marshal_with(resource_fields)
    def get(self, name):
        return Playlist(name).json()

    def put(self, name):
        return Playlist(name, create=True).json()


class TrackResource(Resource):

    url = '/<string:playlist_name>/<int:track_id>/'

    def get(self, playlist_name, track_id):
        return Track(playlist_name, track_id).json()

    def put(self, playlist_name, track_id):
        track = Track(playlist_name, track_id, create=True)
        if 'increment' in request.form:
            track.increment_score()
        return track.json()

