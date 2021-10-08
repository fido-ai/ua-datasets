import json
from enum import Enum
from typing import List

from .uasquad_question_answering import UaSquadDataset


# Keywords - "Питання:", "Контекст:", "Відповідь:"
# Text - everything after the keyword up until the new keyword
# Sentence - key word + text
# 1. Answer MUST be a context's substring
# 2. Every sentence MUST start with a keyword
# 3. Keywords MUST ONLY be at the start of the sentence. There MUSTN'T be keywords inside text
# 4. The order of sentences is the following:
# Context-Question-Answer...Question-Answer-Context-Question-Answer...Question-Answer
# 5. It would be nice if context and question begin with an uppercase letter
def validate_txt(txt_path: str = "ua_squad_dataset.txt", show_warnings: bool = False):
    class Keyword(Enum):
        Context = 1
        Question = 2
        Answer = 3

    previous_keyword = Keyword.Answer  # 4

    with open(txt_path, 'r', encoding='utf-8') as txt_file:
        for line in txt_file.readlines():
            if line.startswith("Контекст:"):
                context = line[len("Контекст:"):].strip()

                if _any_substring(context, ["Питання:", "Контекст:", "Відповідь:"]):  # 3.
                    print("[CRITICAL] Keyword is in context: " + context)

                if previous_keyword != Keyword.Answer:  # 4
                    print("[CRITICAL] There must be answer sentence before context: " + line)
                previous_keyword = Keyword.Context

                if show_warnings and not context[0].isupper():  # 5.
                    print("[WARN] Context's text does not start with an uppercase letter: " + context)
            elif line.startswith("Питання:"):
                question = line[len("Питання:"):].strip()

                if _any_substring(question, ["Питання:", "Контекст:", "Відповідь:"]):  # 3.
                    print("[CRITICAL] Keyword is in question: " + question)

                if previous_keyword == Keyword.Question:  # 4
                    print("[CRITICAL] Two questions in a row: " + line)
                previous_keyword = Keyword.Question

                if show_warnings and not question[0].isupper():  # 5.
                    print("[WARN] Question's text does not start with an uppercase letter: " + question)
            elif line.startswith("Відповідь:"):
                answer = line[len("Відповідь:"):].strip()

                if answer not in context:  # 1.
                    print("[CRITICAL] Answer is not in context:")
                    print("Context: " + context)
                    print("Question: " + question)
                    print("Answer: " + answer)

                if _any_substring(answer, ["Питання:", "Контекст:", "Відповідь:"]):  # 3.
                    print("[CRITICAL] Keyword is in answer: " + answer)

                if previous_keyword != Keyword.Question:  # 4
                    print("[CRITICAL] There must be question sentence before answer: " + line)
                previous_keyword = Keyword.Answer
            else:  # 2.
                print("[CRITICAL] Sentence does not begin with a keyword: " + line),


def to_txt(json_path: str = ".", txt_path: str = "ua_squad_dataset.txt"):
    dataset = UaSquadDataset(json_path)

    with open(txt_path, 'w', encoding='utf-8') as file:
        context = ""
        for q, c, a in dataset:
            if context != c:
                file.write("Контекст: " + c + "\n")
                context = c
            file.write("Питання: " + q + "\n")
            file.write("Відповідь: " + a + "\n")


# In order to get a proper result txt file should be valid (see validate function above)
def to_json(txt_path: str = "ua_squad_dataset.txt", json_path: str = "ua_squad_dataset1.json"):
    json_obj = []

    with open(txt_path, 'r', encoding='utf-8') as txt_file:
        context = ""
        question = ""

        for line in txt_file.readlines():
            if line.startswith("Контекст: "):
                context = line[len("Контекст: "):]
            elif line.startswith("Питання: "):
                question = line[len("Питання: "):]
            elif line.startswith("Відповідь: "):
                answer = line[len("Відповідь: "):]
                json_obj.append({
                    "Question": question.strip(),
                    "Context": context.strip(),
                    "Answer": answer.strip()
                })

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_obj, json_file, ensure_ascii=False, indent=4)


def _any_substring(text: str, substrings: List[str]):
    return any(substring in text for substring in substrings)
