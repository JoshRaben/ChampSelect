import json


class Champion(object):
    """
    A champion in our domain model. It contains all properties that we use to
    compute the proper champion for a user.
    """
    name = None
    lanes = None
    aggression_level = None

    def __init__(self, name):
        self.name = name

    @staticmethod
    def from_json(json_filename):
        champions = []

        with open(json_filename, "r") as champion_json:
            input_champions = json.load(champion_json)

        for _, champ_data in input_champions.items():
            champ = Champion(champ_data["name"])
            champ.lanes = champ_data["lane"]
            champ.aggression_level = champ_data["aggressionlevel"]
            champions.append(champ)

        return champions
