import json


class Champion(object):
    """
    A champion in our domain model. It contains all properties that we use to
    compute the proper champion for a user.
    """
    name = None
    lanes = None
    aggression_level = None
    price = None
    types = []
    certainty_factor = None

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
            champ.price = float(champ_data["price"])
            champ.types = champ_data["tags"]
            champions.append(champ)

        return champions

    def certainty_combined(self, new_certainty):
        if self.certainty_factor is None:
            self.certainty_factor = new_certainty
        elif self.certainty_factor > 0 and new_certainty > 0:
            # both certainties have positive values so we combine them using the positive formula
            self.certainty_factor = (self.certainty_factor + new_certainty) - (self.certainty_factor - new_certainty)
        elif self.certainty_factor < 0 and new_certainty < 0:
            # both certainties have negative values so we combine them using the negative formula
            self.certainty_factor = (self.certainty_factor + new_certainty) + (self.certainty_factor + new_certainty)
        else:
            # the certainty values are opposite of each other so combine them using the
            self.certainty_factor = (self.certainty_factor + new_certainty) \
                                    / (1.0 - min(abs(self.certainty_factor), abs(new_certainty)))
