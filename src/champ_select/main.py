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

    champions = apply_questions(champions, [lanes, aggression_level, blue_essence])
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
            "LOW": 0.0,
            "MED": 0.5,
            "HIGH": 1.0
        }
    else:
        probabilities = {
            "LOW": 1.0,
            "MED": 0.5,
            "HIGH": 0.0
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
