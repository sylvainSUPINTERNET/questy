class Quest:

    title = "";
    description = "";
    requirements = "";
    rewards = [];
    level = 1;


    def __init__(self, title, description, rewards, level, requirements):
        self.title = title
        self.description = description
        self.level = level
        self.rewards = rewards,
        self.requirements = requirements
        


