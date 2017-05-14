import json
import sys


class Story():
    quests = []
    def __init__(self, quests):
        self.quests = quests

    def toJSON(self):
        serialize = list((o.toJSON() for o in self.quests))

        return json.dumps(serialize, default=lambda o: o.__dict__, 
            sort_keys=False, indent=4)
