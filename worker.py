import os

import redis
from rq import Worker, Queue, Connection
from app.main import create_app

listen = ['default']

redis_url = os.getenv('REDISURL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

app = create_app(os.getenv('ENV') or 'dev')
app.app_context().push()
q = Queue(connection=conn)


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work(with_scheduler=True)