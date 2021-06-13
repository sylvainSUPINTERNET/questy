import asyncio
import websockets
from conf.config import WS_HOST,WS_PORT
from tasks.Quest import Quest
from dispatcher import dispatch
import schedule, time
from actions.actions import delete_quests

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


# Check every minutes if some quests must be deleted in redis DB
logging.info("Init schedule for removing quests")
schedule.every(1).seconds.do(delete_quests)

async def server(websocket, path):
    msg = await websocket.recv()
    dispatch(msg)



    # print(f"< {name}")
    # greeting = f"Hello {name}!"
    # await websocket.send(greeting)
    # print(f"> {greeting}")

start_server = websockets.serve(server, WS_HOST, WS_PORT)
asyncio.get_event_loop().run_until_complete(start_server)
schedule.run_pending()
print(f"WS server started on : ws://{WS_HOST}:{WS_PORT}")
asyncio.get_event_loop().run_forever()




