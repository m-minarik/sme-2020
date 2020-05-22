import re
import unicodedata
import json
import traceback

from bs4 import BeautifulSoup


"""
Extracts questions, all answers and the correct answer from downloaded
html files and saves them to 'test.questions.json'
"""

input_files = {"test0": "tests/Test0_review.html",
               "testA": "tests/TestA_review.html",
               "testB": "tests/TestB_review.html",
               "testC": "tests/TestC_review.html",
               "testD": "tests/TestD_review.html"}


def clear_text(text):
    text = text.strip().replace(u"\xa0", " ")
    return re.sub("(\\s{2,})", " ", re.sub(r"[\n\r\t\xa0]", " ", text))


def extract_qa(input_file):
    question_re_pattern = re.compile(r"que multichoice", re.IGNORECASE)
    answer_re_pattern = re.compile(
        r"(?:a. |b. |c. |d. |e. )(.*)", re.IGNORECASE)
    right_answer_re_pattern = re.compile(
        r"(?:Správná odpověď je: )(.*)", re.IGNORECASE)

    with open(input_file, mode="rb") as f:
        html = BeautifulSoup(f, "lxml")

    extracted_qa = []

    for q_div in html.find_all("div", class_=question_re_pattern):
        d = {"question": None,
             "answers": [],
             "correct_answer": None}
        try:
            d["question"] = clear_text(q_div.find(
                "div", {"class": "qtext"}).get_text())

            answers = []
            for a_div in q_div.find("div", {"class": "answer"}).find_all("div"):
                if a_div["class"][0] == "specificfeedback":
                    continue
                answer = clear_text(a_div.get_text().strip())

                answer = answer_re_pattern.findall(answer)[0]
                d["answers"].append(answer)

            correct_answer = clear_text(q_div.find(
                "div", {"class": "rightanswer"}).get_text())
            d["correct_answer"] = right_answer_re_pattern.findall(correct_answer)[
                0]

        except Exception as e:
            print("Couldn't parse question in {}:\n{}".format(
                input_file, d["question"]))
            print(e, "\nTraceback:", traceback.format_exc())
        else:
            extracted_qa.append(d)

    return extracted_qa


def extract_qa_test_b(input_file):
    question_re_pattern = re.compile(r"que multichoice", re.IGNORECASE)
    answer_re_pattern = re.compile(r"(?:a. |b. |c. |d. )(.*)", re.IGNORECASE)
    right_answer_re_pattern = re.compile(
        r"(?:Správná odpověď je: )(.*)", re.IGNORECASE)

    with open(input_file, mode="rb") as f:
        html = BeautifulSoup(f, "lxml")

    extracted_qa = []

    for q_div in html.find_all("div", class_=question_re_pattern):
        d = {"question": None,
             "answers": [],
             "correct_answer": None}
        try:
            d["question"] = clear_text(q_div.find(
                "div", {"class": "qtext"}).get_text())

            answers = []
            for a_div in q_div.find("div", {"class": "answer"}).find_all("div"):
                answer = clear_text(a_div.get_text().strip())
                answer = answer_re_pattern.findall(answer)[0]
                d["answers"].append(answer)

                if "incorrect" in a_div["class"]:
                    print("Please provide correct answer for {}".format(
                        d["question"]))
                    d["correct_answer"] = None

                if "correct" in a_div["class"]:
                    d["correct_answer"] = answer

        except Exception as e:
            print("Couldn't parse question in {}:\n{}".format(
                input_file, d["question"]))
            print(e, "\nTraceback:", traceback.format_exc())
        else:
            extracted_qa.append(d)

    return extracted_qa


if __name__ == "__main__":
    data = {}
    for k, v in input_files.items():
        if k == "testB":
            data[k] = extract_qa_test_b(v)
        else:
            data[k] = extract_qa(v)

    with open("test_questions.json", mode="w") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
