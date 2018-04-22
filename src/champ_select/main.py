import sys
import math

from champ_select.champion import Champion


def main():
    if len(sys.argv) == 3:
        json_file = sys.argv[3]
    else:
        json_file = "champions-small.json"

    champions = Champion.from_json(json_file)

    print("ChampSelect. An AI that picks your League of Legends.")
    print()

    champions = apply_questions(champions, [lanes, aggression_level, blue_essence, player_type])
    print()

    print("Your champion(s):")
    champions.sort(key=lambda x: x.certainty_factor, reverse=True)
    for champ in champions[:10]:
        print("\t" + champ.name + "\t" + "Certainty: " + str(champ.certainty_factor))


def apply_questions(champions, questions):
    for question in questions:
        champions = list(question(champions))

        if len(champions) <= 1:
            break
    return champions


def lanes(champions):
    """
    Prompts the user to select their preferred lane and picks only characters
    in that lane.

    Available options:
        Top,
        Jungle
        Mid,
        ADC,
        Support
    """
    choice = prompt_user("What lane would you like to play?", ["Top", "Jungle", "Mid", "ADC", "Support"])
    champions = filter(lambda champ: choice in champ.lanes, champions)
    return champions


def aggression_level(champions):
    """
    Asks if the player is aggressive and picks characters based on the probability of our aggression level
    """
    choice = prompt_user("Do you like to be in the action or are you more laid back and methodical?", ["Yes", "No"])
    probabilities = {}
    if choice == "Yes":
        probabilities = {
            "LOW": -0.5,
            "MED": 0.0,
            "HIGH": 0.5
        }
    else:
        probabilities = {
            "LOW": 0.5,
            "MED": 0.0,
            "HIGH": -0.5
        }

    for champ in champions:
        champ.certainty_combined(probabilities[champ.aggression_level])

    return champions


def blue_essence(champions):
    min_choice, _ = prompt_range("How much Blue Essence do you have to spend on a champion?", 450)
    cheap_certainty = 0.25
    expensive_certainty = -0.99

    for champ in champions:
        if champ.price < min_choice:
            champ.certainty_combined(cheap_certainty)
        else:
            champ.certainty_combined(expensive_certainty)

    return champions


def player_type(champions):
    """
    Possible player types:
        Marksman
        Mage
        Fighter
        Tank
        Assassin
        Support
    """
    done = False
    type_set = ["MARKSMAN", "MAGE", "FIGHTER", "TANK", "ASSASSIN", "SUPPORT"]
    user_types = []

    while not done:
        print("What champion types do you want? (Marksman, Mage, Fighter, Tank, Assassin, Support). ")
        print("Type \"done\" when you are done adding types.")

        type = input("> ")
        if type.upper().strip() == "DONE":
            done = True
        elif type.upper().strip() in type_set:
            user_types.append(type)
        else:
            print("\"" + type + "\" isn't a valid type.")
    if not len(user_types) == 0:
        for champ in champions:
            champ_has_type = False
            for champ_type in champ.types:
                if champ_type.upper().strip() in user_types:
                    champ_has_type = True
                    champ.certainty_combined(0.65)

            if not champ_has_type:
                champ.certainty_combined(-0.65)

    return champions


def prompt_range(question, min_number, max_number=0):
    question += " (separated by commas)"
    while True:
        if max_number != 0:
            print(question + " min: " + str(min_number) + " max: " + str(max_number))
        else:
            print(question + " min: " + str(min_number) + " max: unbounded")

        answer_str = input("> ").strip()
        min_answer = math.inf
        max_answer = -math.inf

        try:
            answers = answer_str.split()
            min_answer = int(answers[0].strip())
            if max_number != 0:
                max_answer = int(answers[1].strip())
            else:
                max_answer = math.inf
        except ValueError:
            print("You answer needs to be an integer. Try again.")

        if min_answer < max_answer:
            break
        else:
            print("Your min number must be before you max number. Try again.")

    return min_answer, max_answer


def objective_based(champions):
    choice = prompt_user("Are you more objective oriented or do you concentrate on your own lane?",
                         ["Teamwork", "Solo"])
    probabilities = {}
    if choice == "Teamwork":
        probabilities = {
            "SPLITPUSH": -0.65,
            "MOBILE": -0.35,
            "ENGAGE": 0.75,
            "PEEL": 0.85,
            "POKE": 0.0,
            "WAVECLEAR": 0.0,
            "SIEGE": 0.25,
            "BURST": 0.0
        }
    else:
        probabilities = {
            "SPLITPUSH": 0.45,
            "MOBILE": 0.55,
            "ENGAGE": -0.75,
            "PEEL": -0.85,
            "POKE": 0.0,
            "WAVECLEAR": 0.0,
            "SIEGE": 0.45,
            "BURST": 0.0
        }

        for champion in champions:
            champion.certainty_combined(probabilities[champion.playstyle])

        return champions


def split_or_tf(champions):
    choice = prompt_user("Do you like to split push or team fight",
                         ["Split Push", "Team Fight"])
    probabilities = {}
    if choice == "Split Push":
        probabilities = {
            "SPLITPUSH": 0.85,
            "MOBILE": 0.35,
            "ENGAGE": 0.15,
            "PEEL": -0.25,
            "POKE": 0.0,
            "WAVECLEAR": 0.0,
            "SIEGE": 0.25,
            "BURST": 0.0
        }
    else:
        probabilities = {
            "SPLITPUSH": -0.75,
            "MOBILE": 0.65,
            "ENGAGE": 0.25,
            "PEEL": 0.60,
            "POKE": 0.35,
            "WAVECLEAR": 0.15,
            "SIEGE": 0.45,
            "BURST": 0.35
        }

        for champion in champions:
            champion.certainty_combined(probabilities[champion.playstyle])

        return champions


def roaming(champions):
    choice = prompt_user("Do you enjoy roaming to support your team?",
                         ["Yes", "No"])
    probabilities = {}
    if choice == "Yes":
        probabilities = {
            "SPLITPUSH": -0.15,
            "MOBILE": 0.75,
            "ENGAGE": 0.65,
            "PEEL": -0.25,
            "POKE": -0.25,
            "WAVECLEAR": 0.15,
            "SIEGE": 0.45,
            "BURST": 0.25
        }
    else:
        probabilities = {
            "SPLITPUSH": 0.5,
            "MOBILE": -0.25,
            "ENGAGE": -0.15,
            "PEEL": 0.45,
            "POKE": 0.25,
            "WAVECLEAR": 0.45,
            "SIEGE": -0.35,
            "BURST": -0.35
        }

        for champion in champions:
            champion.certainty_combined(probabilities[champion.playstyle])

        return champions


def prompt_user(question, answers):
    while True:
        print(question)
        for i, choice in enumerate(answers):
            row_number = i + 1
            print("\t" + str(row_number) + ".) " + choice)
        try:
            answer = int(input("> ").strip()) - 1
        except ValueError:
            continue

        if 0 <= answer < len(answers):
            break

    return answers[answer]


if __name__ == '__main__':
    main()
