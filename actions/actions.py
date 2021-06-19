from tasks.Quest import Quest
from conf.redisConf import QUESTS_STREAM_NAME
import logging

def create_quest(data, redis_instance):
    new_quest = Quest(data["title"], data["description"], data["rewards"], data["level_gain"], data["requirements"])

    # Check if stream exists or not
    if redis_instance.xlen(QUESTS_STREAM_NAME) != 0 :
        print("Quests stream already exists")
    else:
        logging.info("Init quests stream ...")
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

                
        print(keys_values)
        # redis_instance.xadd(QUESTS_STREAM_NAME, keys_values, id='*', maxlen=None, approximate=True)
        
        # logging.info(f"Quest added with success {str(keys_values)}")
        # logging.info("Stream created with success.")
    

# p = r.xadd("quests", fields, id='*', maxlen=None, approximate=True)
# r.xadd("quests", fields, id='*', maxlen=None, approximate=True)

# print(p)

    # TODO save each quest to redis
