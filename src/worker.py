import os

from redis import Redis
from rq import Worker

redis_conn = Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=os.getenv('REDIS_PORT', 6379))

w = Worker(['default'], connection=redis_conn)
w.work()
