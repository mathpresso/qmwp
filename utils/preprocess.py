import re


def preprocess_number(q: str) -> str:
    return re.sub(r'(\d),(\d)', r'\1\2', q)


assert preprocess_number('100,000,000/2,203,133') == '100000000/2203133'


def preprocess(question: str) -> str:
    question = preprocess_number(question)
    return question
