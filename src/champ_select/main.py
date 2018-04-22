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
    choice = prompt_user("Do you like to be in the action or are you more laid back and methodical?", ["In the action", "Laid back"])
    probabilities = {}
    if choice == "In the action":
        probabilities = {
            "LOW": 0.25,
            "MED": 0.5,
            "HIGH": 1.0
        }
    else:
        probabilities = {
            "LOW": 1.0,
            "MED": 0.5,
            "HIGH": 0.25
        }

    for champ in champions:
        champ.probability = probabilities[champ.aggression_level]

    return champions


def moba_experience(champions):
    choice = prompt_user("How much experience do you have in the MOBA category of games?", ["Very little (less than 100 hours)",
                                                                                            "Some (100-300 hours",
                                                                                            "Moderate (300-1000 hours)",
                                                                                            "A lot (1000+ hours)"])
    probabilities = {}
    if choice == "Very little (less than 100 hours)":
        probabilities = {
            "1": 0.99,
            "2": 0.99,
            "3": 0.99,
            "4": 0.99,
            "5": 0.2,
            "6": 0.2,
            "7": 0.1,
            "8": -0.2,
            "9": -0.5,
            "10": -0.8,
        }
    if choice == "Some (100-300 hours)":
        probabilities = {
            "1": 0.99,
            "2": 0.99,
            "3": 0.99,
            "4": 0.99,
            "5": 0.6,
            "6": 0.3,
            "7": 0.2,
            "8": 0.0,
            "9": -0.2,
            "10": -0.5,
        }
    if choice == "Moderate (300-1000 hours)":
        probabilities = {
            "1": 0.99,
            "2": 0.99,
            "3": 0.99,
            "4": 0.99,
            "5": 0.99,
            "6": 0.99,
            "7": 0.99,
            "8": 0.3,
            "9": -0.1,
            "10": -0.3,
        }
    if choice == "A lot (1000+ hours)":
        probabilities = {
            "1": 0.99,
            "2": 0.99,
            "3": 0.99,
            "4": 0.99,
            "5": 0.99,
            "6": 0.99,
            "7": 0.99,
            "8": 0.99,
            "9": 0.8,
            "10": 0.6,
        }

        for champion in champions:
                champion.certainty_combined(probabilities[champion.difficulty])


def mechanical_level(champions):
    choice = prompt_user("Do you enjoy playing high skill cap champions?", ["I like highly mechanical champions.",
                                                                            "I like my champion to involve a little skill.",
                                                                            "I prefer simple champions."])
    probabilities = {}
    if choice == "I like highly mechanical champions.":
        probabilities = {
            "1": -0.5,
            "2": -0.5,
            "3": -0.3,
            "4": -0.3,
            "5": 0.3,
            "6": 0.3,
            "7": 0.7,
            "8": 0.7,
            "9": 0.7,
            "10": 0.7,
        }

    if choice == "I like my champion to involve a little skill.":
        probabilities = {
            "1": -0.3,
            "2": -0.3,
            "3": -0.1,
            "4": -0.1,
            "5": 0.7,
            "6": 0.7,
            "7": 0.2,
            "8": 0.2,
            "9": 0.0,
            "10": 0.0,
        }

    if choice == "I prefer simple champions.":
        probabilities = {
            "1": 0.7,
            "2": 0.7,
            "3": 0.5,
            "4": 0.5,
            "5": 0.2,
            "6": 0.2,
            "7": -0.5,
            "8": -0.5,
            "9": -0.7,
            "10": -0.7,
        }

        for champion in champions:
                champion.certainty_combined(probabilities[champion.difficulty])


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
