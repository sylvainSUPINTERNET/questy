from conf.wsMessageFormat import QUESTS_AVAILABLE_MAX
from conf.redisConf import QUESTS_STREAM_NAME, MAX_XREAD_COUNT
import logging
import redis

'''
Delete current quest and create new one to be notified
'''

def job_delete_quests():
    logging.info("Recycle quests job started")

    redis_instance = redis.Redis(host='localhost', port=6379, db=0)

     # Delete current quest in redis stream
    data_list_byte = redis_instance.xread({"quests":"0"},count=MAX_XREAD_COUNT)   

    # Remove existing quests
    if not len(data_list_byte):
        logging.info("No quests active for the moment.")
    else:
        for quest in data_list_byte[0][1]:
            logging.info(f"Delete {quest[0].decode('utf-8')}")
            redis_instance.xdel(QUESTS_STREAM_NAME, quest[0].decode("utf-8"))
        logging.info("Quests stream deleted with success")

     # Generate new quest from file