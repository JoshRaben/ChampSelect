import json

"""
A champion in our domain model. It contains all properties that we use to
compute the proper champion for a user.
"""
class Champion(object):
    name = None
    difficulty = None
    lanes = None
    tags = None
    attack_range = None

    def __init__(self, name):
        self.name = name

    @staticmethod
    def from_json(json_filename):
        champions = []
        champions_from_json = {}
        with open(json_filename, "r") as champion_json:
            champions_from_json = json.load(champion_json)
        champions_json_data = champions_from_json["data"]

        for _, champ_data in champions_json_data.items():
            champ = Champion(champ_data["name"])
            champ.difficulty = champ_data["info"]["difficulty"]
            champ.tags = champ_data["tags"]
            champ.attack_range = champ_data["stats"]["attackrange"]
            champ.lanes = champ_data["lane"]
            champions.append(champ)


        return champions
