import os
import sys
import json
import random


# Choose which tests to include
from_tests = {"testA": True,
              "testB": True,
              "testC": True,
              "testD": True}


def clear():
    if os.name == 'nt':
        # FU Windows
        os.system('cls')
    else:
        os.system('clear')


def print_question(q):
    clear()

    print(q["question"])
    print(20 * "-")
    print("\n".join(q["answers"]), end="")


def print_correct_answer(q):
    print(20 * "=")
    print(q["correct_answer"])


def sme_test():
    with open("test_questions.json", mode="r") as f:
        extracted_qa = json.load(f)

    questions = []
    for k, v in from_tests.items():
        if v:
            questions.extend(extracted_qa[k])

    random.shuffle(questions)

    for q in questions:
        print_question(q)
        i = input()
        if i == "F":
            break
        print_correct_answer(q)
        i = input()
        if i == "F":
            break


if __name__ == "__main__":
    clear()
    print("Zdareeec")
    print("Otázka -> Enter -> Odpověď -> Enter -> Další otázka -> ... -> ezy A")
    print("F ukončí testík")
    print("---------------")
    print("Pokusit se o zvládnutí testu (Enter)")
    i = input()
    if i != "F":
        sme_test()
