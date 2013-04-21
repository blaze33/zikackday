import os
from redis import StrictRedis

url = os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379')
redis = StrictRedis.from_url(url)
