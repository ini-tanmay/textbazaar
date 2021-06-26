import os
import urllib.parse
import redis
from redis import Redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = 'redis://redistogo:4d234d8e4f0faae5f701ef2c1b992926@spinyfin.redistogo.com:9064/'
# redis_url = os.getenv('REDISTOGO_URL')

urllib.parse.uses_netloc.append('redis')
url = urllib.parse.urlparse(redis_url)
conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
