import asyncio
import websockets
import redis

from conf.config import WS_HOST,WS_PORT
from tasks.Quest import Quest
from dispatcher import dispatch

from tasks.jobs import job_delete_quests
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
job_remove_old_quest = scheduler.add_job(job_delete_quests, 'interval', minutes=1)
scheduler.start()

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


cache = redis.Redis(host='localhost', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

count = get_hit_count()
print(count)

# Check every minutes if some quests must be deleted in redis DB
logging.info("Init schedule for removing quests")

async def server(websocket, path):
    msg = await websocket.recv()
    dispatch(msg)
    

    # print(f"< {name}")
    # greeting = f"Hello {name}!"
    # await websocket.send(greeting)
    # print(f"> {greeting}")

start_server = websockets.serve(server, WS_HOST, WS_PORT)
asyncio.get_event_loop().run_until_complete(start_server)
print(f"WS server started on : ws://{WS_HOST}:{WS_PORT}")
asyncio.get_event_loop().run_forever()



