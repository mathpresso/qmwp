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

    return question, model_output, code, answer


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

    return question, model_output, code, answer
