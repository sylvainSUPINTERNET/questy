from tasks.Quest import Quest

def create_quest(data):
    new_quest = Quest(data["title"], data["description"], data["rewards"], data["level"], data["requirements"])
    # TODO save each quest to redis

def delete_quests():
    print("delete oldeest quest")