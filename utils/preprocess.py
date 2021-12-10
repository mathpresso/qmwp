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
FIGURE_UNITS = ['각형', '각뿔', '각기둥', '면체']
REVERSE_UNITS = ['학년', '반', '층']
REVERSE_EXCEPTION_PREFIX = ['가장', '더']
REVERSE_EXCEPTION_WORDS = [
    ' 큽니', ' 클까', ' 작습니', ' 작을까', ' 큰 ', ' 작은 ',
    ' 많이 ', ' 조금 ', ' 적게 ', ' 많게 ', ' 적은 ', ' 많은 ', ' 많을까', ' 적을까',
    ' 가볍습', ' 무겁습', ' 가벼운 ', ' 무거운 ', ' 가벼울까', ' 무거울까',
    ' 높은 ', ' 낮은 ', ' 높습', ' 낮습', ' 높을까', ' 낮을까',
    ' 긴 ', ' 짧은 ', ' 깁니', ' 짧습', ' 길까', ' 짧을까',
    ' 넓은 ', ' 좁은 ', ' 넓습', ' 좁습', ' 넓을까', ' 좁을까',
    ' 깊은 ', ' 얕은 ', ' 깊습', ' 얕습', ' 깊을까', ' 얕을까',
    ' 빠른 ', ' 느린 ', ' 빠릅', ' 느립', ' 빠를까', ' 느릴까',
]
REVERSE_EXCEPTION_WORDS2 = [
    ' 왼쪽에서 ', ' 오른쪽에서 ', ' 위에서 ', ' 아래에서 ', ' 아래서 ', ' 위쪽에서 ', ' 아래쪽에서 ',
]
ARITHMETIC_OPERATIONS = [
    ('×', '*'),
    ('÷', '/'),
]
INDEX_UNITS = ['자리', '번']
KOREAN_NUMS = [
    (' 첫', ' 1'),
    (' 한', ' 1'),
    (' 두', ' 2'),
    (' 세', ' 3'),
    (' 네', ' 4'),
    (' 다섯', ' 5'),
    (' 여섯', ' 6'),
    (' 일곱', ' 7'),
    (' 여덟', ' 8'),
    (' 아홉', ' 9'),
    (' 열', ' 10'),
]
DIGITS = [
    (' 일', ' 1'),
    (' 십', ' 10'),
    (' 백', ' 100'),
    (' 천', ' 1000'),
    (' 만', ' 10000'),
    (' 십만', ' 100000'),
    (' 백만', ' 1000000'),
    (' 천만', ' 10000000'),
    (' 억', ' 100000000'),
]
DIGIT_UNITS = ['의 자리', '의자리']
DIGIT_UNIT_TARGET = '의 자리'


def _preprocess_number(q: str) -> str:
    return re.sub(r'(\d),(\d)', r'\1\2', q)


def _preprocess_time(q: str) -> str:
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


def _preprocess_figure(q: str) -> str:
    for unit in FIGURE_UNITS:
        for kor, num in KOREAN_NUMS_REVERSE[1:]:
            kor = kor.strip()
            num = num.strip()
            q = q.replace(f"{kor}{unit}", f"{num}{unit}")
    return q


def _preprocess_question(q: str) -> str:
    # INDEX and DIGITS
    q = ' ' + q
    reverse_convert = True
    for prefix in REVERSE_EXCEPTION_PREFIX + REVERSE_UNITS:
        for word in REVERSE_EXCEPTION_WORDS:
            if f'{prefix}{word}' in q:
                reverse_convert = False
            if not reverse_convert:
                break
        if not reverse_convert:
            break
    for word in REVERSE_EXCEPTION_WORDS2:
        if word in q:
            reverse_convert = False
            break
    if reverse_convert:
        for unit in REVERSE_UNITS:
            for to, source in KOREAN_NUMS_REVERSE:
                q = q.replace(f"{source} {unit}", f"{to}{unit}")
                q = q.replace(f"{source}{unit}", f"{to}{unit}")
    for source, to in ARITHMETIC_OPERATIONS:
        q = q.replace(source, to)
    for unit in INDEX_UNITS:
        for kor, num in KOREAN_NUMS:
            q = q.replace(f"{kor} {unit}", f"{num} {unit}")
    for t in ['소수', '소수점']:
        if t in q:
            # ['칸', '자리', '번']
            for unit in ['칸']:
                for kor, num in KOREAN_NUMS:
                    q = q.replace(f"{kor} {unit}", f"{num} {unit}")
    for unit in DIGIT_UNITS:
        for kor, num in DIGITS:
            q = q.replace(f"{kor}{unit}", f"{num}{DIGIT_UNIT_TARGET}")
    return q[1:]


def preprocess(question: str) -> str:
    question = _preprocess_number(question)
    question = _preprocess_time(question)
    question = _preprocess_figure(question)
    question = _preprocess_question(question)
    return question


assert _preprocess_number('100,000,000/2,203,133') == '100000000/2203133'
assert _preprocess_time('일주일 전에') == '7일 전에'
assert _preprocess_figure("정삼각형의 둘레의 길이는?") == "정3각형의 둘레의 길이는?"
assert _preprocess_question("어떤 세 자리 수를 다섯 번 더했더니 10이 되었다. 어떤 수를 구하시오.") == \
       '어떤 3 자리 수를 5 번 더했더니 10이 되었다. 어떤 수를 구하시오.'
