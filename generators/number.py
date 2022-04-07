# 수 찾기
import random

from utils.common import NEWLINE, VARIABLES
from utils.utils import get_answer, postfix, postprocessing

"""
numbers_1_1
- x개의 수 a, b, c, d가 있습니다. 그 중에서 가장 큰 수와 가장 작은 수의 차는 얼마입니까?

numbers_1_2
- a, b, c, d 중에서 서로 다른 숫자 x개를 뽑아 만들 수 있는 세 자리 수 중에서 가장 작은 수를 쓰시오.

numbers_1_3
- a에서 b까지의 수가 있을 때, x보다는 크고, y보다는 작은 수는 얼마입니까?

numbers_2_1
- A를 7로 나누면 몫은 B이고 나머지는 C가 됩니다. 이 식에서 몫과 나머지가 같습니다. A 중 가장 큰 수를 구하시오

numbers_2_2
- 서로 다른 두 자연수 A, B가 있습니다. A를 a로 나누면 몫은 b이고 나머지는 B가 됩니다. 나머지 B가 가장 큰 수일 때 A를 구하시오.

numbers_2_3
- 네 자리 수 5A31를 백의 자리에서 반올림하면 5000이 됩니다. 0부터 9까지의 숫자 중 A에 쓸 수 있는 숫자는 모두 몇 개입니까?

numbers_3_1
- 두 자리 수끼리의 곱셈에서 곱하는 수의 십의 자리 숫자 a를 b로 잘못 보고 계산한 값이 c가 되었습니다.
  바르게 계산한 값이 d일 때, 두 개의 두 자리 수 중 더 작은 수를 쓰시오.

numbers_3_2
- 어떤 수에 a를 더한 후 b를 곱하고, c를 뺀 값을 d로 나누면 e이 됩니다. 어떤 수를 구하시오.
"""


def numbers_1_1():
    """
    template: x개의 수 a, b, c, d가 있습니다. 그 중에서 가장 큰 수와 가장 작은 수의 차는 얼마입니까?
    """
    q_type = '수 찾기 1'
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

    return question, model_output, code, answer, q_type


def numbers_1_2():
    """
    template: "a, b, c, d 중에서 서로 다른 숫자 x개를 뽑아 만들 수 있는 세 자리 수 중에서 가장 작은 수를 쓰시오."
    """
    q_type = '수 찾기 2'
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

    return question, model_output, code, answer, q_type


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
    q_type = '수 찾기 3'
    return question, model_output, code, answer, q_type


def numbers_2_1():
    """
    template: "A를 7로 나누면 몫은 B이고 나머지는 C가 됩니다. 이 식에서 몫과 나머지가 같습니다. A 중 가장 큰 수를 구하시오"
    """
    templates = [
        (
            [
                "{x0_str} {n0_str} {op_str} 몫은 {x1_str} 나머지는 {x2_str} ",
            ],
            "n0 = {n0}",
            "x0 = '{x0}'{newline}x1 = '{x1}'{newline}x2 = '{x2}'",
        ),
    ]

    options1 = [
        ("", 0),
        ("{lst_str} 자연수입니다. ", 1),
        ("{lst_str} 모두 자연수입니다. ", 1),
        ("{lst_str} 정수입니다. ", 0),
    ]

    op_strs = [
        '나누면',
        '나누었을 때',
        '나누게 되면',
    ]

    x0, x1, x2 = random.sample(VARIABLES, 3)
    n0 = random.randint(2, 20)

    op_str = random.choice(op_strs)
    x0_str = postfix(f'{x0}', '을(를)')
    x1_str = random.choice([
        f'{x1}이며',
        f'{x1}이고',
        "{} 되고".format(postfix(f'{x1}', '이(가)')),
        f'{x1}',
    ])
    x2_str = random.choice([
        "{} 됩니다.".format(postfix(f'{x2}', '이(가)')),
        f'{x2}입니다.',
    ])
    n0_str = postfix(f'{n0}', '으로')

    q_templates, init_n_template, init_x_template = random.choice(templates)
    question = random.choice(q_templates).format(
        x0_str=x0_str, n0_str=n0_str, op_str=op_str, x1_str=x1_str, x2_str=x2_str)

    model_logic = []
    init_n = [init_n_template.format(n0=n0)]

    # add optional string to question
    lst_str = postfix(f'{x0}, {x1}, {x2}', '은(는)')
    option1, option_cond_key = random.choice(options1)
    question += option1.format(lst_str=lst_str)

    # condition
    cond_options = [
        "이 식에서 ",
        "다음 식에서 ",
        "식에서 ",
        "",
    ]

    eos_conds1 = [
        "같습니다.",
        "같을 때,",
    ]

    eos_cond = random.choice(eos_conds1)
    cond_option = random.choice(cond_options)

    n1 = random.randint(1, n0 - 1)
    n1_str = random.choice([
        f'{n1}만큼',
        f'{n1}',
        postfix(f'{n1}', '이(가)'),
    ])

    cond_template = [
        (
            [
                "{cond_option}몫과 나머지가 {eos_cond}",
                "{cond_option}나머지와 몫이 {eos_cond}",
            ],
            "t1 = f'{x1} = {x2}'",
            f"{x1} == {x2}",
        ),
        (
            [
                "{cond_option}몫이 나머지보다 {n1_str} 클 때,",
                "{cond_option}몫이 나머지보다 {n1_str} 큽니다.",
            ],
            "t1 = f'{x1} = {x2} + {n1}'",
            f"{x1} == {x2} + n1",
        ),
        (
            [
                "{cond_option}나머지가 몫보다 {n1_str} 작을 때,",
                "{cond_option}나머지가 몫보다 {n1_str} 작습니다.",
            ],
            "t1 = f'{x2} = {x1} - {n1}'",
            f"{x2} == {x1} - n1",
        ),
        (
            [
                "{cond_option}몫이 나머지보다 {n1_str} 작을 때,",
                "{cond_option}몫이 나머지보다 {n1_str} 작습니다.",
            ],
            "t1 = f'{x1} = {x2} - {n1}'",
            f"{x1} == {x2} - n1",
        ),
        (
            [
                "{cond_option}나머지가 몫보다 {n1_str} 클 때,",
                "{cond_option}나머지가 몫보다 {n1_str} 큽니다.",
            ],
            "t1 = f'{x2} = {x1} + {n1}'",
            f"{x2} == {x1} + n1",
        ),
    ]

    cond_template_key = random.randint(0, len(cond_template) - 1)
    cond_qs, cond_s, cond_s2 = cond_template[cond_template_key]
    cond_q = random.choice(cond_qs)

    if cond_template_key != 0:
        init_n.append(f"n1 = {n1}")

    # cond
    question += cond_q.format(cond_option=cond_option, eos_cond=eos_cond, n1_str=n1_str)

    # nth_largest, smallest 는 skip
    target_conds = [
        ('max', ['가장 큰 수를 구하시오.', '가장 큰 수는?', '가장 큰 수의 값은?', '가장 큰 수의 값을 구하면?', '가장 큰 수를 쓰시오.']),
        ('min', ['가장 작은 수를 구하시오.', '가장 작은 수는?', '가장 작은 수의 값은?', '가장 작은 수의 값을 구하면?', '가장 작은 수를 쓰시오.']),
    ]

    target_f, target_cond_strs = random.choice(target_conds)
    target_cond_str = random.choice(target_cond_strs)

    target_option1 = random.choice(
        [
            "",
            "나누는 수 ",
            "피제수 ",
        ]
    )
    target_option2 = random.choice(
        [
            "",
            "나머지 "
        ]
    )

    target_template = [
        (
            [
                f"{x0} 중 {target_cond_str}",
                f"나누어지는 수 {x0} 중 {target_cond_str}",
                f"피제수 {x0} 중 {target_cond_str}",
            ],
            f"answer = {target_f}(result[x0])",
            f"{x0}",
        ),
        (
            [
                f"{target_option1}{x1} 중 {target_cond_str}",
            ],
            f"answer = {target_f}(result[x1])",
            f"{x1}",
        ),
        (
            [
                f"{target_option2}{x2} 중 {target_cond_str}",
            ],
            f"answer = {target_f}(result[x2])",
            f"{x2}",
        ),
    ]

    targets, target_code, target_v = random.choice(target_template)
    target = random.choice(targets)

    # 자연수 조건
    if option_cond_key == 1:
        cond_s2 = f"{cond_s2} and {x0} > 0 and {x1} > 0 and {x2} > 0"

    sol = f"result = []\n" \
          f"for {x0} in range(1, 10000):\n" \
          f"\t{x1} = {x0} // n0\n" \
          f"\t{x2} = {x0} % n0\n" \
          f"\tif {cond_s2}:\n" \
          f"\t\tresult.append({target_v})"

    model_logic.append(sol)
    model_logic.append(f"answer = {target_f}(result)")

    question += ' '
    question += target
    model_output = NEWLINE.join(init_n + model_logic)
    code = postprocessing(model_output, question)
    answer = get_answer(code)
    q_type = '수 찾기 4'
    return question, model_output, code, answer, q_type


def numbers_2_2(solution_id=1):
    """
    template: "서로 다른 두 자연수 A, B가 있습니다. A를 a로 나누면 몫은 b이고 나머지는 B가 됩니다. 나머지 B가 가장 큰 수일 때 A를 구하시오."
    """

    p, q = random.sample(range(5, 100), 2)
    a, b = random.sample(VARIABLES, 2)
    a_l = postfix(a, '을(를)')
    b_e = postfix(b, '이(가)')

    init_n = []
    init_x = []
    model_logic = []

    option1, init_n_1, n_index, condition = random.choice([
        (f"서로 다른 두 자연수 {a}, {b_e} 있습니다. ", "n0 = 2", 1, "{0} > 0 and {1} > 0 and {0} != {1}"),
        (f"두 자연수 {a}, {b_e} 있습니다. ", "n0 = 2", 1, "{0} > 0 and {1} > 0"),
        (f"두 수 {a}, {b_e} 있습니다. ", "n0 = 2", 1, ""),
        (f"서로 다른 두 수 {a}, {b_e} 있습니다. ", "n0 = 2", 1, "{0} != {1}"),
        (f"두 정수 {a}, {b_e} 있습니다. ", "n0 = 2", 1, ""),
        (f"서로 다른 자연수 {a}, {b_e} 있습니다. ", "", 0, "{0} > 0 and {1} > 0 and {0} != {1}"),
        (f"정수 {a}, {b_e} 있습니다. ", "", 0, ""),
        (f"자연수 {a}, {b_e} 있습니다. ", "", 0, "{0} > 0 and {1} > 0"),
        (f"", "", 0, ""),
    ])
    init_n_1 = ""
    n_index = 0

    n1_str = postfix(str(p), '로')
    n2_str = random.choice([
        f'{q}이고',
        '{} 되고'.format(postfix(str(q), '이(가)')),
        f'{q}이며,'

    ])
    x2_str = random.choice([
        f'{b_e} 됩니다.',
        f'{b}입니다.',
        f'{b}일 때,',
    ])

    t1 = a
    t2 = b
    if random.random() < 0.5:
        t1 = b
        t2 = a

    t1_str = postfix(t1, '이(가)')
    t2_str = random.choice([
        '{} 구하시오.'.format(postfix(t2, '을(를)')),
        f'{t2}의 값을 구하시오.',
        f'{t2}의 값은?',
    ])

    cond_d = {
        'max': '{} 큰 수',
        'min': '{} 작은 수',
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

    cond_n = random.randint(0, min(p, 9))
    cond_f = random.choice(['min', 'max'])

    cond_str = cond_d[cond_f].format(cond_to_str[cond_n]) + '일 때'

    # init n
    if init_n_1:
        init_n.append(init_n_1)
    init_n.append(f'n{n_index} = {p}')
    init_n.append(f'n{n_index + 1} = {q}')
    if cond_n > 0:
        init_n.append(f'n{n_index + 2} = {cond_n}')

    # init x
    init_x.append(f"x0 = '{a}'")
    init_x.append(f"x1 = '{b}'")

    # model logic1
    # loop 돌면서 조건을 만족하는 수 중 이후에 활용할 값을(t1) result에 담고 조건에 맞게 뽑은 다음에 구하고자 하는 target(t2) 를 계산한다.
    if condition:
        condition_str = condition.format(a, b)
        sol1 = "result = []\n" \
               f"for {a} in range(1, 10000):\n" \
               f"\t{b} = {a} % n{n_index}\n" \
               f"\tif {a} // n{n_index} == n{n_index + 1} and {condition_str}:\n"
    else:
        sol1 = "result = []\n" \
               f"for {a} in range(1, 10000):\n" \
               f"\t{b} = {a} % n{n_index}\n" \
               f"\tif {a} // n{n_index} == n{n_index + 1}:\n"
    if t1 == a:
        sol_1_1 = f"\t\tresult.append({a})"
    else:
        sol_1_1 = f"\t\tresult.append({b})"

    model_logic.append(sol1 + sol_1_1)

    if cond_n > 1:
        func = predefined_func[cond_f]
        model_logic.append(f"t0 = {func}(result, n{n_index + 2})")
    else:
        func = cond_f
        model_logic.append(f"t0 = {func}(result)")

    if t2 == a:
        model_logic.append(f"t1 = n{n_index} * n{n_index + 1}")
        model_logic.append(f"answer = t1 + t0")
    else:
        model_logic.append(f"answer = t0 % n{n_index}")

    # model logic2
    # 공식 풀이
    # TODO: 정수, 자연수 처리 해야함. 안되어있음.
    model_logic2 = []
    # 피제수
    if t2 == a:
        model_logic2.append(f"t0 = n{n_index} * n{n_index + 1}")
        if cond_f == 'min':
            if cond_n:
                model_logic2.append(f"answer = t0 + n{n_index + 2} - 1")
            else:
                model_logic2.append(f"answer = t0")
        else:
            if cond_n:
                model_logic2.append(f"t1 = t0 + n{n_index}")
                model_logic2.append(f"answer = t1 - n{n_index + 2}")
            else:
                model_logic2.append(f"answer = t0 + n{n_index} - 1")
    # 나머지
    elif t2 == b:
        if cond_f == 'min':
            if cond_n:
                model_logic2.append(f"answer = n{n_index + 2} - 1")
            else:
                model_logic2.append(f"answer = 0")
        else:
            if cond_n:
                model_logic2.append(f"answer = n{n_index} - n{n_index + 2}")
            else:
                model_logic2.append(f"answer = n{n_index} - 1")

    question = f"{option1}{a_l} {n1_str} 나누면 몫은 {n2_str} 나머지는 {x2_str} {t1_str} {cond_str} {t2_str}"

    if solution_id == 1:
        model_output_lst = init_n + model_logic
    else:
        model_output_lst = init_n + model_logic2
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)
    q_type = '수 찾기 5'
    return question, model_output, code, answer, q_type


def numbers_2_3():
    """
    template: "네 자리 수 5A31를 백의 자리에서 반올림하면 5000이 됩니다. 0부터 9까지의 숫자 중 A에 쓸 수 있는 숫자는 모두 몇 개입니까?"
    """

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

    round_digits = {
        1: '일',
        2: '십',
        3: '백',
        4: '천',
        5: '만',
        6: '십만',
        7: '백만',
        8: '천만',
        9: '억',
    }

    target = random.choice([
        "쓸 수 있는 숫자는 모두 몇 개입니까?",
        "들어갈 수 있는 수는 몇 개 있습니까?",
        "넣을 수 있는 수는 모두 몇 개입니까?",
        "들어갈 수 있는 수의 개수는?",
        "들어갈 수 있는 수의 개수를 구하시오.",
    ])

    eomi1 = random.choice([
        "이 됩니다.",
        "입니다.",
        "이 될 때,",
        "일 때,",
    ])

    op = random.choice(["올림", "버림", "반올림"])
    digit = random.randint(2, 9)
    digit_str = digits[digit]
    tmp_value = random.randint(10 ** (digit - 1), 10 ** digit)
    round_digit = random.randint(1, digit)
    round_digit_value = 10 ** (round_digit - 1)
    tmp_value_str = str(tmp_value)
    banolim_key = random.randint(0, 1)
    if op == "버림" or (op == "반올림" and banolim_key == 0):
        if round_digit == digit:
            target_value_str = '0'
        else:
            target_value_str = tmp_value_str[:digit - round_digit] + '0' * round_digit
    elif op == "올림" or (op == "반올림" and banolim_key == 1):
        if round_digit == digit:
            target_value_str = '1' + '0' * round_digit
        else:
            c = int(tmp_value_str[digit - round_digit - 1])
            target_value = int(tmp_value_str[:digit - round_digit - 1] + '0' * (round_digit + 1)) + int(
                str(c + 1) + '0' * round_digit)
            target_value_str = str(target_value)
    x = random.choice(VARIABLES)
    value_str = tmp_value_str[:digit - round_digit] + x + tmp_value_str[digit - round_digit + 1:]
    value_str_eomi = postfix(value_str, '을(를)')
    round_str = round_digits[round_digit]

    option1 = random.choice([
        f"{digit_str} 자리 수 ",
        "",
    ])

    st, ed = sorted(random.sample(range(0, 10), 2))
    question = f"{option1}{value_str_eomi} {round_str}의 자리에서 {op}하면 {target_value_str}{eomi1} {st}부터 {ed}까지의 숫자 중 {x}에 {target}"

    # TODO: 일, 십, 백의 자리 -> 초기화 해야 하는가?
    # TODO: 6A42 는 초기화 해야 하는가 ?

    init_n = []
    n_index = 0
    if option1:
        init_n.append(f"n{n_index} = {digit}")
        n_index += 1
    init_n.append(f"n{n_index} = {round_digit_value}")
    init_n.append(f"n{n_index + 1} = {target_value_str}")
    init_n.append(f"n{n_index + 2} = {st}")
    init_n.append(f"n{n_index + 3} = {ed}")

    model_logic = []
    conds = []
    if round_digit == digit:
        conds.append("i != 0")
    if op == "반올림":
        if banolim_key == 0:
            conds.append("i < 5")
        else:
            conds.append("i >= 5")

    if conds:
        conds_str = "if {}:\n".format(" and ".join(conds))
        sol = "result = []\n" \
              F"for i in range(n{n_index + 2}, n{n_index + 3} + 1):\n" \
              f"\t{conds_str}" \
              "\t\tresult.append(i)\n" \
              "answer = len(result)"
    else:
        sol = "result = []\n" \
              f"for i in range(n{n_index + 2}, n{n_index + 3} + 1):\n" \
              "\tresult.append(i)\n" \
              "answer = len(result)"

    model_logic.append(sol)
    model_output_lst = init_n + model_logic
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)
    q_type = '수 찾기 6'
    return question, model_output, code, answer, q_type


def numbers_3_1():
    """
    template: "두 자리 수끼리의 곱셈에서 곱하는 수의 십의 자리 숫자 a를 b로 잘못 보고 계산한 값이 c가 되었습니다. " \
              "바르게 계산한 값이 d일 때, 두 개의 두 자리 수 중 더 작은 수를 쓰시오."
    """

    init_n = []
    init_x = []
    model_logic = []

    option1, option1_init = random.choice([
        ("두 자리 수끼리의", 1),
        ("두 자리 수들의", 1),
        ("두 개의 두 자리 수끼리의", 2),
    ])
    option1_init = 1

    categories = [('*', '곱셈에서', ['곱하는 수의 ', ''], '/')]

    op, op_str, op_options, op_inv = random.choice(categories)
    op_option_str = random.choice(op_options)

    key = random.randint(0, 1)
    mis_template = [(1, '일'), (10, '십')]
    mis_init, mis_str = mis_template[key]

    n1 = random.randint(10, 99)
    n2 = random.randint(10, 99)
    if key == 0:
        n1_str = str(n1)
        m1 = n1_str[1]
        m2 = random.choice([c for c in '0123456789' if c != m1])
        n1_new = int(n1_str[0] + m2)
        v1 = n1_new * n2
        v2 = n1 * n2
    elif key == 1:
        n1_str = str(n1)
        m1 = n1_str[0]
        m2 = random.choice([c for c in '123456789' if c != m1])
        n1_new = int(m2 + n1_str[1])
        v1 = n1_new * n2
        v2 = n1 * n2
    m1_l = postfix(m1, '을')
    m2_r = postfix(m2, '로')
    v1_str = '{} 되었습니다.'.format(postfix(str(v1), '이'))
    t1 = random.choice([
        "바르게 계산한 값이",
        "바르게 계산하면",
        "올바른 계산 결과는",
        "올바른 계산은",
        "올바른 계산 결과 값은",
    ])
    v2_str = f'{v2}일 때,'

    # ~ 개 -> init X
    option2, option2_init = random.choice([
        ("두 개의 두 자리 수 가운데", 2),
        ("두 개의 수 중", 1),
        ("두 개의 수 가운데", 1),
    ])
    option2_init -= 1

    option3 = random.choice(['더 ', ''])
    cond_f, cond_strs = random.choice([
        ('max', ['큰 수를 구하시오.', '큰 수는?', '큰 수의 값은?', '큰 수의 값을 구하면?', '큰 수를 쓰시오.', '큰 수는 얼마입니까?']),
        ('min', ['작은 수를 구하시오.', '작은 수는?', '작은 수의 값은?', '작은 수의 값을 구하면?', '작은 수를 쓰시오.', '작은 수는 얼마입니까?'])
    ])
    cond_str = random.choice(cond_strs)

    question = f"{option1} {op_str} {op_option_str}{mis_str}의 자리 숫자 {m1_l} {m2_r} 잘못 보고 계산한 값이 " \
               f"{v1_str} {t1} {v2_str} {option2} {option3}{cond_str}"

    # init_n
    n_index = 0
    for i in range(option1_init):
        init_n.append(f'n{n_index} = 2')
        n_index += 1
    mis_index = n_index
    init_n.append(f'n{n_index} = {mis_init}')  # 일의 자리, 십의 자리
    n_index += 1
    m1_index = n_index
    m2_index = n_index + 1
    v1_index = n_index + 2
    v2_index = n_index + 3
    init_n.append(f'n{m1_index} = {m1}')
    init_n.append(f'n{m2_index} = {m2}')
    init_n.append(f'n{v1_index} = {v1}')
    init_n.append(f'n{v2_index} = {v2}')
    n_index += 4
    for i in range(option2_init):
        init_n.append(f'n{n_index} = 2')
        n_index += 1

    # model_logic
    model_logic.append(f"t0 = n{v1_index} - n{v2_index}")
    model_logic.append(f"t1 = n{m2_index} - n{m1_index}")
    model_logic.append(f"t2 = t1 * n{mis_index}")
    model_logic.append(f"t3 = t0 / t2")
    model_logic.append(f"t4 = n{v2_index} / t3")
    model_logic.append(f"answer = {cond_f}([t3, t4])")

    model_output_lst = init_n + init_x + model_logic
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)
    q_type = '수 찾기 7'
    return question, model_output, code, answer, q_type


def numbers_3_2():
    """
    template: "어떤 수에 a를 더한 후 b를 곱하고, c를 뺀 값을 d로 나누면 e이 됩니다. 어떤 수를 구하시오."
    """

    init_n = []
    init_x = []
    model_logic = []

    categories = [('+', ['더하고', '더한 후', '더한 후에', '더하고 나서', '더한 결과에', '더한 값에'],
                   ['더하고', '더한 후에', '더하고 나서', '더한 결과를', '더한 값을'],
                   ['더하면', '더한 결과는', '더한 값은'], '-'),
                  ('-', ['빼고', '뺀 후에', '뺀 후', '뺀 결과에', '뺀 값에'],
                   ['빼고', '뺀 후에', '뺀 결과를', '뺀 값을'],
                   ['빼면', '뺀 결과는', '뺀 값은'], '+'),
                  ('*', ['곱하고', '곱한 후', '곱하고 나서', '곱한 후에', '곱한 결과에', '곱한 값에'],
                   ['곱하고', '곱하고 나서', '곱한 후에', '곱한 결과를', '곱한 값을'],
                   ['곱하면', '곱한 결과는', '곱한 값은'], '/'),
                  ('/', ['나눈 후', '나누고', '나누고 나서', '나눈 후에', '나눈 결과에', '나눈 값에'],
                   ['나누고', '나눈 후에', '나눈 결과를', '나눈 값을'],
                   ['나누면', '나눈 결과는', '나는 값은'], '*'),
                  ]

    eos = random.choice([
        '어떤 수를 구하시오.',
        '어떤 수는?',
        '어떤 수의 값은?',
        '어떤 수의 값을 구하시오.',
        '어떤 수는 얼마인가?',
    ])

    op_count = random.randint(2, 6)
    op_lst = [random.choice(categories) for _ in range(op_count)]
    MIN = 1
    MAX = 300
    n_lst = [random.randint(MIN, MAX) for _ in range(op_count)]
    n_result = random.randint(100, 10000)
    josa_lst = []

    for op_tuple in op_lst:
        if op_tuple[0] == '/':
            josa_lst.append(2)
        else:
            josa_lst.append(1)
    josa_lst.append(3)

    if josa_lst[0] == 2:
        question = '어떤 수를 '
    else:
        question = '어떤 수에 '

    question_lst = []
    for i, op_tuple in enumerate(op_lst):
        op = op_tuple[0]
        josa = random.choice(op_tuple[josa_lst[i + 1]])
        n = n_lst[i]
        if op == '/':
            n_str = postfix(str(n), '로')
        else:
            n_str = postfix(str(n), '를')
        question_lst.append(f'{n_str} {josa}')

    n_result_str = random.choice([
        '{} 됩니다.'.format(postfix(str(n_result), '이')),
        '{}일 때,'.format(n_result),
        '{}입니다.'.format(n_result),
    ])

    question_lst.append(n_result_str)
    question_lst.append(eos)
    question += ' '.join(question_lst)

    # init_n
    for i, n in enumerate(n_lst):
        init_n.append(f'n{i} = {n}')
    length = len(n_lst)
    init_n.append(f'n{length} = {n_result}')

    # init_x
    init_x.append("x0 = 'A'")

    # model_logic
    # TODO: this should be solution 2
    t_index = 0
    for i, op_tuple in enumerate(op_lst[::-1]):
        op = op_tuple[4]  # 역함수
        if i == 0:
            model_logic.append(f't{t_index} = n{length} {op} n{length - 1 - i}')
        elif i == length - 1:
            model_logic.append(f'answer = t{t_index} {op} n0')
        else:
            model_logic.append(f't{t_index + 1} = t{t_index} {op} n{length - 1 - i}')
            t_index += 1

    # TODO: consider init_x (어떤 수)
    model_output_lst = init_n + model_logic
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)
    q_type = '일차방정식'
    return question, model_output, code, answer, q_type


def generate_numbers(num_samples_to_generate: int = 10000) -> list:
    ratio = [
        (numbers_1_1, 10), (numbers_1_2, 15), (numbers_1_3, 10),
        (numbers_2_1, 15), (numbers_2_2, 10), (numbers_2_3, 15),
        (numbers_3_1, 10), (numbers_3_2, 15),
    ]
    targets = []
    for func, count in ratio:
        targets.extend([func] * count)

    MAX_RETRIES = 10
    results = []
    while num_samples_to_generate > 0:
        tmps = []
        for func in targets:
            for attempt in range(MAX_RETRIES):
                try:
                    ret = func()
                    tmps.append(ret)
                # fail so retry
                except:
                    pass
                # success
                else:
                    break
            # all retries failed
            else:
                print(f"All retries failed. check template '{func.__name__}'")
        num_samples_to_generate -= len(tmps)
        results.extend(tmps)
    return results
