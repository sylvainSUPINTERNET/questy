from tasks.Quest import Quest
from conf.redisConf import QUESTS_STREAM_NAME, MAX_XREAD_COUNT
import logging



def delete_quest_stream(data,redis_instance):
    logging.info(f"Delete quest with ID : {data['id']} ... ")
    redis_instance.xdel(QUESTS_STREAM_NAME, data['id'])
    logging.info(f"Delete with success")


def delete_quests_stream(data, redis_instance):
    logging.info("Delete stream quests")
    # Using incomplete ids 0 (could be $ for example here)
    # XREAD COUNT 4 STREAMS quests 0 ( or $ for the latest result if you using READ BLOCK )
    data_list_byte = redis_instance.xread({"quests":"0"},count=MAX_XREAD_COUNT)

    for quest in data_list_byte[0][1]:
        logging.info(f"Delete {quest[0].decode('utf-8')}")
        redis_instance.xdel(QUESTS_STREAM_NAME, quest[0].decode("utf-8"))
    logging.info("Quests stream deleted with success")


def create_quest(data, redis_instance):
    new_quest = Quest(data["title"], data["description"], data["rewards"], data["level_gain"], data["requirements"])
    # Check if stream exists or not
    keys_values = new_quest.__dict__
    for k,v in keys_values.items():

        # Cleanup tuple format from WS payload (since Redis don't accept this type)
        if type(v) is tuple:
            tmp = ""
            for m in keys_values[k]:
                for idx,z in enumerate(m) :
                    if idx == len(m) - 1:
                        tmp += str(z);
                    else:
                        tmp += str(z) + ",";
            keys_values[k] = tmp

    redis_instance.xadd(QUESTS_STREAM_NAME, keys_values, id='*', maxlen=None, approximate=True)                
        
    logging.info(f"Quest added with success {str(keys_values)}")
    logging.info("Stream created with success.")
    
