# 수 찾기
import random
from utils.common import NEWLINE, VARIABLES
from utils.utils import get_answer, postprocessing, postfix


def numbers_1_1():
    """
    template: x개의 수 a, b, c, d가 있습니다. 그 중에서 가장 큰 수와 가장 작은 수의 차는 얼마입니까?
    """
    eos_d = {
        1: [
            '얼마인가요?',
            '얼마입니까?',
        ],
        2: [
            '구하시오.'
        ]
    }

    templates = [
        (
            [
                '{length}개의 수 {lst}가 있습니다. 그 중에서 ',
                '{length}개의 수 {lst} 중에서 ',
                '{length}개의 수 {lst} 중 ',
                '{length}개의 수 {lst}가 있을 때, 그 중 ',
            ],
            "n0 = {length}{newline}{seq_n_string}{newline}",
        ),
        (
            [
                '{lst} 중에서 ',
                '{lst} 가 있을 때, 그 중에서 ',
                '{lst} 중 ',
            ],
            "{seq_n_string}{newline}",
        )
    ]

    cond_d = {
        'max': [
            '{s} 큰 수'
        ],
        'min': [
            '{s} 작은 수'
        ],
    }

    cond_to_str = {
        0: '가장',
        1: '첫 번째로',
        2: '두 번째로',
        3: '세 번째로',
        4: '네 번째로',
        5: '다섯 번째로',
        6: '여섯 번째로',
        7: '일곱 번째로',
        8: '여덟 번째로',
        9: '아홉 번째로',
    }

    predefined_func = {
        'max': 'nth_largest',
        'min': 'nth_smallest',
    }

    categories = [('+', '합'),
                  ('*', '곱'),
                  ('-', '차'),
                  ]
    op = random.choice(categories)

    # for sequence1
    seq_length = random.randint(4, 10)
    seq = random.sample(range(10, 1000), seq_length)
    seq_to_text = ', '.join(str(i) for i in seq)

    n1 = random.randint(0, seq_length - 1)
    n2 = random.randint(0, seq_length - 1)
    cond_key1 = random.choice(list(cond_d.keys()))
    cond_key2 = random.choice(list(cond_d.keys()))
    condition1 = random.choice(cond_d[cond_key1])
    condition2 = random.choice(cond_d[cond_key2])
    cond1_str = condition1.format(s=cond_to_str[n1])
    cond2_str = condition2.format(s=cond_to_str[n2])

    template_id = random.choice(range(len(templates)))
    q_templates, s_template = templates[template_id]
    q_template = random.choice(q_templates)

    if template_id == 0:
        n_index = 1
    else:
        n_index = 0
    seq_n_string = '\n'.join([f"n{idx + n_index} = {elem}" for idx, elem in enumerate(seq)])

    question = q_template.format(length=seq_length, lst=seq_to_text)
    model_output = s_template.format(length=seq_length, seq_n_string=seq_n_string, newline=NEWLINE)

    genre = op[1]
    eos_key = random.choice(list(eos_d.keys()))
    eos_term_str = random.choice(eos_d[eos_key])

    if eos_key == 1:
        genre_str = postfix(f'{genre}', '은(는)')
        eos_str = f'{genre_str} {eos_term_str}'
    elif eos_key == 2:
        genre_str = postfix(f'{genre}', '을(를)')
        eos_str = f'{genre_str} {eos_term_str}'

    question += cond1_str
    question += '와 '
    question += cond2_str
    question += '의 '
    question += eos_str

    # check which template used
    if template_id == 0:
        i1 = 1 + seq_length
        i2 = 2 + seq_length
        if n1 == 0:
            i2 -= 1
    else:
        i1 = 0 + seq_length
        i2 = 1 + seq_length
        if n1 == 0:
            i2 -= 1

    if n1 != 0:
        model_output += f"n{i1} = {n1}"
        model_output += NEWLINE
    if n2 != 0:
        model_output += f"n{i2} = {n2}"
        model_output += NEWLINE

    model_output += "l0 = {lst}{newline}".format(lst="[{}]".format(seq_to_text), newline=NEWLINE)
    # use nth_biggest, nth_smallest
    if n1 == 0:
        model_output += f"t0 = {cond_key1}(l0)"
    else:
        model_output += f"t0 = {predefined_func[cond_key1]}(l0, n{i1})"
    model_output += NEWLINE

    if n2 == 0:
        model_output += f"t1 = {cond_key2}(l0)"
    else:
        model_output += f"t1 = {predefined_func[cond_key2]}(l0, n{i2})"
    model_output += NEWLINE
    if op[0] == '-':
        model_output += "answer = abs(t0 - t1)"
    else:
        model_output += "answer = t0 {} t1".format(op[0])

    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return question, model_output, code, answer


def numbers_1_2():
    """
    template: "a, b, c, d 중에서 서로 다른 숫자 x개를 뽑아 만들 수 있는 세 자리 수 중에서 가장 작은 수를 쓰시오."
    """

    options1 = [
        "",
        "숫자 카드 ",
        "다음 수 ",
        "수열 ",
    ]

    options2 = [
        '서로 다른 숫자 ',
        '서로 다른 수 ',
        '숫자 ',
        '수 ',
        '',
    ]

    digits = {
        1: '한',
        2: '두',
        3: '세',
        4: '네',
        5: '다섯',
        6: '여섯',
        7: '일곱',
        8: '여덟',
        9: '아홉',
    }

    conds_t = [
        ('max', ['가장 큰 수를 구하시오.', '가장 큰 수는?', '가장 큰 수의 값은?', '가장 큰 수의 값을 구하면?', '가장 큰 수를 쓰시오.']),
        ('min', ['가장 작은 수를 구하시오.', '가장 작은 수는?', '가장 작은 수의 값은?', '가장 작은 수의 값을 구하면?', '가장 작은 수를 쓰시오.'])
    ]

    seq_len = random.randint(3, 6)
    count = random.randint(2, seq_len)
    seq = random.sample(range(0, 10), seq_len)
    lst = ', '.join([str(i) for i in seq])
    seq_n_string = '\n'.join([f"n{idx} = {elem}" for idx, elem in enumerate(seq)])
    l0 = "l0 = [{}]".format(lst)

    digit = digits[count]
    option1 = random.choice(options1)
    option2 = random.choice(options2)
    func, conds = random.choice(conds_t)
    cond = random.choice(conds)

    model_output_lst = []
    model_output_lst.append(seq_n_string)
    model_output_lst.append(f'n{seq_len} = {count}')
    model_output_lst.append(f'n{seq_len + 1} = {count}')
    model_output_lst.append(l0)
    model_output_lst.append(f"num_permutations(l0, n{seq_len})")
    model_output_lst.append(f"answer = {func}(result)")

    question = f"{option1}{lst} 중에서 {option2}{count}개를 뽑아 만들 수 있는 {digit} 자리 수 중에서 {cond}"
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return question, model_output, code, answer


def numbers_1_3():
    """
    template: "a에서 b까지의 수가 있을 때, x보다는 크고, y보다는 작은 수는 얼마입니까?"
    """

    range_st, range_ed = sorted(random.sample(range(0, 100), 2))
    compare_str_d = {
        'gt': [
            '초과',
            '보다 크고,',
            '보다는 크고,',
        ],
        'lt': [
            '미만인',
            '보다 작은',
            '보다는 작은',
        ],
        'gte': [
            '이상',
            '이상이고,',
            '보다 크거나 같고,',
            '보다 작지 않고,',
        ],
        'lte': [
            '이하인',
            '보다 작거나 같은',
            '보다 크지 않은',
        ]
    }
    op_d = {
        'gt': '<',
        'lt': '<',
        'gte': '<=',
        'lte': '<=',
    }

    eomi1 = random.choice(['에서', '부터'])
    op1 = random.choice(['gt', 'gte'])
    op2 = random.choice(['lt', 'lte'])
    op1_str = random.choice(compare_str_d[op1])
    op2_str = random.choice(compare_str_d[op2])
    template_id = random.randint(0, 1)
    # 값
    if template_id == 0:
        value = random.randint(range_st, range_ed)
        st = value - 1
        ed = value + 1
        if op1[-1] == 'e':
            st += 1
        if op2[-1] == 'e':
            ed -= 1
        template_str = random.choice([
            '수는 얼마입니까?',
            '수는 무엇입니까?',
            '수의 값은?',
            '수를 구하면?',
        ])
    # 개수
    elif template_id == 1:
        st, ed = sorted(random.sample(range(0, 100), 2))
        template_str = random.choice([
            '수의 개수는?',
            '수는 몇 개입니까?',
            '수는 모두 몇 개입니까?',
            '수는 모두 몇 개있습니까?',
            '수는 전부 몇 개일까요?',
        ])

    model_output_lst = []
    model_output_lst.append(f"n0 = {range_st}")
    model_output_lst.append(f"n1 = {range_ed}")
    model_output_lst.append(f"n2 = {st}")
    model_output_lst.append(f"n3 = {ed}")
    gt = op_d[op1]
    lt = op_d[op2]

    if template_id == 0:
        sol = "for i in range(n0, n1 + 1):\n" \
              f"\tif n2 {gt} i {lt} n3:\n" \
              "\t\tanswer = i"
    elif template_id == 1:
        sol = "result = []\n" \
              "for i in range(n0, n1 + 1):\n" \
              f"\tif n2 {gt} i {lt} n3:\n" \
              "\t\tresult.append(i)\n" \
              "answer = len(result)"
    model_output_lst.append(sol)

    question = f"{range_st}{eomi1} {range_ed}까지의 수가 있을 때, {st}{op1_str} {ed}{op2_str} {template_str}"
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return question, model_output, code, answer
