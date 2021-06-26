from django.apps import AppConfig
import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)



class WriterConfig(AppConfig):
    name = 'writer'
    def ready(self):
        with Connection(conn):
            worker = Worker(map(Queue, listen))
            worker.work()


        pass # startup code here

