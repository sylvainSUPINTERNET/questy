import json
import logging
from conf.wsMessageFormat import WS_TYPE_CREATE_QUEST, WS_TYPE_DELETE_QUEST, WS_TYPE_DELETE_QUESTS
from actions.actions import create_quest, delete_quest_stream, delete_quests_stream

def dispatch(msg, redis_instance):
    logging.info("Action received dispatch ...")

    try:
        payload_ws = json.loads(msg)

        if "type" in payload_ws:
            # Not array format (delete quest by id / delete quests)
            if payload_ws["type"] == WS_TYPE_DELETE_QUEST:
                delete_quest_stream(payload_ws, redis_instance)
            elif payload_ws["type"] == WS_TYPE_DELETE_QUESTS : 
                delete_quests_stream(payload_ws, redis_instance)
            else:
                logging.info("Command send not defined. Please check message format configuration for commands list")
        else:
            # Array format for create multiple quests to stream
            for data in payload_ws:
                if data["type"] == WS_TYPE_CREATE_QUEST :
                    create_quest(data=data, redis_instance=redis_instance)
                else:
                    logging.info("Provided type not exist")
    except Exception as e:
        logging.info(f"Fail to parse action for dispatch : {e}")