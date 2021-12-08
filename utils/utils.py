import re
import string
from contextlib import redirect_stdout
from io import StringIO
from random import randint

import tossi

from .common import ALPHABETS_FOR_PARTICLE, NEWLINE, SPACE4
from .predefined_func import *


def _generate_number(scale=2, starts_from=0) -> str:
    """generates random number string (integer or fraction or decimal)

    Args:
        scale (int, optional): 10 ** scale. Defaults to 2.

    Returns:
        str: ex. "13", "13/24", "13.1"
    """
    cls = randint(0, 2)
    if cls == 0:
        # integer
        return f"{randint(starts_from, 10**scale)}"
    elif cls == 1:
        # fraction
        return f"{randint(starts_from, 10**scale)}/{randint(1, 10**scale)}"
    else:
        # decimal
        return f"{randint(starts_from, 10**(scale*2))/(10**scale)}"


def is_alphabet(c):
    return c in string.ascii_letters


def pick_e(name: str) -> str:
    """호석 -> 호석이. 윤기 -> 윤기.

    Args:
        name (str): human name

    Returns:
        str: human name with optionally '이' added at the end
    """
    if tossi.pick(name, '은') == '은':
        return name + '이'
    else:
        return name


def postfix(s, particle):
    particle = particle.strip()
    if is_alphabet(s[-1]):
        if particle in ['이', '가', '이(가)', '가(이)']:
            if s[-1] in ALPHABETS_FOR_PARTICLE:
                return s + '이'
            else:
                return s + '가'
        elif particle in ['을', '를', '을(를)', '를(을)']:
            if s[-1] in ALPHABETS_FOR_PARTICLE:
                return s + '을'
            else:
                return s + '를'
        elif particle in ['은', '는', '은(는)', '는(은)']:
            if s[-1] in ALPHABETS_FOR_PARTICLE:
                return s + '은'
            else:
                return s + '는'
        elif particle in ['와', '과', '와(과)', '과(와)']:
            if s[-1] in ALPHABETS_FOR_PARTICLE:
                return s + '과'
            else:
                return s + '와'
        elif particle in ['으로', '로', '(으)로']:
            if s[-1] in ALPHABETS_FOR_PARTICLE:
                return s + '으로'
            else:
                return s + '로'
    return tossi.postfix(s, particle)


def get_answer(equation):
    io = StringIO()
    with redirect_stdout(io):
        exec(equation, {})
    return io.getvalue().rstrip('\n')


def answer_formatting(code, question):
    answer_check_code = code + NEWLINE + ANSWER_CHECK_CODE
    ret = int(get_answer(answer_check_code))
    code = code.replace('\t', SPACE4)

    need_prime_solution = False
    # round
    q_split_l = re.split('[.,]', question)
    last_q = q_split_l[-1] if q_split_l[-1] else q_split_l[-2]
    decimal_q = [
        '소수부를',
        '소수점을',
        '소수점으로',
        '소수로',
        '소수 둘째 자리',
        '소수 셋째 자리',
        '소수 2째 자리',
        '소수 3째 자리',
        '소수 두번째 자리',
        '소수 세번째 자리',
        '소수 2번째 자리',
        '소수 3번째 자리',
        '소수 두 번째 자리',
        '소수 세 번째 자리',
        '소수 2 번째 자리',
        '소수 3 번째 자리',
        '소수점 둘째 자리',
        '소수점 셋째 자리',
        '소수점 2째 자리',
        '소수점 3째 자리',
        '소수점 두번째 자리',
        '소수점 세번째 자리',
        '소수점 2번째 자리',
        '소수점 3번째 자리',
        '소수점 두 번째 자리',
        '소수점 세 번째 자리',
        '소수점 2 번째 자리',
        '소수점 3 번째 자리',
    ]
    if any(q in last_q for q in decimal_q):
        need_prime_solution = True
    if ret == 2:
        # object, people name, ...
        return code + NEWLINE + "print(answer)"
    elif ret == 0 and not need_prime_solution:
        # integer
        return code + NEWLINE + "print(int(answer))"
    else:
        # (ret == 1 or ret == 0) and need_prime_solution
        if need_prime_solution:
            return IMPORT_MATH + NEWLINE + code + NEWLINE + ANSWER_ROUND_TWO + NEWLINE + "print('{:.2f}'.format(answer))"
        else:
            return IMPORT_MATH + NEWLINE + code + NEWLINE + ANSWER_ROUND_ZERO + NEWLINE + "print(answer)"


def postprocessing(code, question):
    imports = []
    remains = []

    # imports
    if "nth_smallest" in code:
        imports.append(IMPORT_NTH_SMALLEST)
    if "nth_largest" in code:
        imports.append(IMPORT_NTH_LARGEST)

    # predefined function
    for line in code.split(NEWLINE):
        if "num_permutations(" in line:
            tmp = NEWLINE.join(imports + remains)
            tmp += NEWLINE
            tmp += IMPORT_NUM_PERMUTATIONS
            tmp += NEWLINE
            indent = line.rpartition("num_permutations(")[0]
            tmp += indent
            tmp += f"processed = {line}\n"
            tmp += indent
            tmp += "print(processed)"
            processed = get_answer(tmp)
            remains.append(processed)
        else:
            remains.append(line)
    code = NEWLINE.join(imports + remains)
    # round / int
    code = answer_formatting(code, question)

    return code
