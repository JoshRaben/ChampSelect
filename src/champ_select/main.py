import sys
from champ_select.champion import Champion


def main():
    if len(sys.argv) == 3:
        json_file = sys.argv[3]
    else:
        json_file = "champions-small.json"

    champions = Champion.from_json(json_file)

    print("ChampSelect. An AI that picks your League of Legends.")
    print()

    champions = apply_questions(champions, [lanes, aggression_level])
    print()

    print("Your champion(s):")
    for champ in champions:
        print("\t" + champ.name)


def apply_questions(champions, questions):
    for question in questions:
        champions = list(question(champions))

        if len(champions) <= 1:
            break
    return champions


def lanes(champions):
    """
    Prompts the user to select their preferred lane. This function just filters
    out all champions that are not in their selected lane.
    """
    choice = prompt_user("What lane would you like to play?", ["Top", "Jungle", "Mid", "ADC", "Support"])
    champions = filter(lambda champ: choice in champ.lanes, champions)
    return champions


def aggression_level(champions):
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

    return filter(lambda champ: probabilities[champ.aggression_level] >= 0.5, champions)


def objective_based(champions):
    choice = prompt_user("Are you more objective oriented or do you concentrate on your own lane?", ["Teamwork", "Solo"])
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
            "SPLITPUSH": 0.65,
            "MOBILE": 0.55,
            "ENGAGE": -0.75,
            "PEEL": -0.85,
            "POKE": 0.0,
            "WAVECLEAR": 0.0,
            "SIEGE": 0.45,
            "BURST": 0.0
        }

        return lambda champ: probabilities[champ.playstyle] >= 0.5, champions

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
