from modules.store.storage import redis
from modules.tools.utilities import get_a_Uuid


class Playlist(object):

    void = False
    tracks = []

    def __init__(self, name, create=False):
        self.name = name
        uuid = redis.get(name)
        if uuid:
            self.uuid = uuid
            self.tracks = redis.zrange(uuid, 0, -1, desc=True, withscores=True)
        elif create:
            self.uuid = get_a_Uuid()
            self.save()
        else:
            self.void = True

    def save(self):
        redis.set(self.name, self.uuid)

    def json(self):
        if not self.void:
            return {'name': self.name, 'uuid': self.uuid, 'tracks': self.tracks}
        return {}

unknown_track_data = {'score':0, 'void': True}

class Track(object):

    void = False

    def __init__(self, playlist_name, track_id, create=False):
        self.playlist = Playlist(playlist_name)
        self.id = track_id
        if not self.playlist.void:
            score = redis.zscore(self.playlist.uuid, track_id)
            if score:
                self.score = score
            elif create:
                self.score = 1
                self.save()
            else:
                self.is_unknown()
        else:
            self.is_unknown()

    def increment_score(self, amount=1):
        self.score = redis.zincrby(self.playlist.uuid, self.id)

    def is_unknown(self):
        for key in unknown_track_data:
            setattr(self, key, unknown_track_data[key])

    def save(self):
        redis.zadd(self.playlist.uuid, self.score, self.id)

    def json(self):
        if not self.void:
            return {'track_id': self.id, 'score': self.score}
        return {}