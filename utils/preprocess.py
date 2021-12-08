import re


KOREAN_NUMS_REVERSE = [
    (' 일', ' 1'),
    (' 이', ' 2'),
    (' 삼', ' 3'),
    (' 사', ' 4'),
    (' 오', ' 5'),
    (' 육', ' 6'),
    (' 칠', ' 7'),
    (' 팔', ' 8'),
    (' 구', ' 9'),
    (' 십', ' 10'),
    (' 십일', ' 11'),
    (' 십이', ' 12'),
    (' 십삼', ' 13'),
    (' 십사', ' 14'),
    (' 십오', ' 15'),
    (' 십육', ' 16'),
    (' 십칠', ' 17'),
    (' 십팔', ' 18'),
    (' 십구', ' 19'),
    (' 이십', ' 20'),
    (' 이십일', ' 21'),
    (' 이십이', ' 22'),
    (' 이십삼', ' 23'),
    (' 이십사', ' 24'),
    (' 이십오', ' 25'),
    (' 이십육', ' 26'),
    (' 이십칠', ' 27'),
    (' 이십팔', ' 28'),
    (' 이십구', ' 29'),
    (' 삼십', ' 30'),
    (' 삼십일', ' 31'),
]
TIME_UNITS = [
    ('초', ['초']),
    ('분', ['분']),
    ('시간', ['시간', '시']),
]
TIME_UNITS2 = [
    ('일', ['주일', '주'], 7)
]


def preprocess_number(q: str) -> str:
    return re.sub(r'(\d),(\d)', r'\1\2', q)


def preprocess_time(q):
    q = ' ' + q
    for num_kor, num in KOREAN_NUMS_REVERSE:
        for to, froms, value in TIME_UNITS2:
            for _from in froms:
                new_num = int(num) * value
                q = q.replace(f'{num_kor}{_from}', f' {new_num}{to}')
                q = q.replace(f'{num_kor} {_from}', f' {new_num}{to}')
                q = q.replace(f'{num}{_from}', f' {new_num}{to}')
                q = q.replace(f'{num} {_from}', f' {new_num}{to}')
    return q[1:]


def preprocess(question: str) -> str:
    question = preprocess_number(question)
    question = preprocess_time(question)
    return question


assert preprocess_number('100,000,000/2,203,133') == '100000000/2203133'
assert preprocess_time('일주일 전에') == '7일 전에'
