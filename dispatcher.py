import json
import logging
from conf.wsMessageFormat import WS_TYPE_CREATE_QUEST
from actions.actions import create_quest

def dispatch(msg):
    logging.info("Action received dispatch ...")
    try:
        json_data_array = json.loads(msg)
    
        for data in json_data_array:
            if data["type"] == WS_TYPE_CREATE_QUEST :
                create_quest(data=data)
            else:
                logging.info("Provided type not exist")
    except Exception as e:
        logging.info(f"Fail to parse action for dispatch {e}")