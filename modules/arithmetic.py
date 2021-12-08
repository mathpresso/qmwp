# 산술연산
import random
from utils.common import NEWLINE, PEOPLE_NAMES, OBJECTS, CONTAINERS, SUBJECTS
from utils.utils import get_answer, postprocessing, postfix, pick_e


def simple_arithmetic_1():
    """
    template: container 안에 9개의 obj이 있습니다. A가 x개의 obj을 container 안에 더 넣었습니다. container 안에 있는 obj은 모두 몇 개입니까?
    """
    # functions
    def init(container, H, value, obj):
        obj_str = postfix(obj, '이(가)')
        templates = [
            f'{container} 안에 {value}개의 {obj_str} 있습니다.',
            f'{container}에 {obj_str} {value}개 들어있습니다.',
            f'{obj_str} {container}에 {value}개 들어있습니다.',
            f'{container}에는 {obj_str} {value}개 들어있습니다.',
        ]
        return random.choice(templates)

    def init_middle(container, H, value, obj):
        obj_str = postfix(obj, '이(가)')
        templates = [
            f'처음에 {container} 안에는 {value}개의 {obj_str} 있었습니다.',
            f'처음 {container}에는 {obj_str} {value}개 들어있었습니다.',
            f'처음에 {obj_str} {container} 안에 {value}개 들어있었습니다.',
        ]
        return random.choice(templates)

    def add(container, H, M, O):
        O = postfix(O, '을(를)')
        H_e = pick_e(H)
        H = f'{H_e}가'
        p2 = random.choice(["를", ""])
        templates = [
            f'{O} {H} {M}개 더 넣었습니다.',
            f'{O} {H} {M}개 넣었습니다.',
            f'{O} {H} {M}개 집어넣었습니다.',
            f'{O} {H} {M}개 추가했습니다.',
            f'{H} {M}개의 {O} 더 넣었습니다.',
            f'{H} {M}개의 {O} 넣었습니다.',
            f'{H} {M}개의 {O} 집어넣었습니다.',
            f'{H} {M}개의 {O} 추가했습니다.',
            f'{H} {M}개{p2} 더 넣었습니다.',
            f'{H} {M}개{p2} 넣었습니다.',
            f'{H} {M}개{p2} 집어넣었습니다.',
            f'{H} {M}개{p2} 추가했습니다.',
        ]
        t1 = [
            f'{container} 안에 ',
            f'{container}에 ',
        ]
        if random.random() < 0.5:
            return random.choice(t1) + random.choice(templates)
        else:
            return random.choice(templates)

    def sub(container, H, M, O):
        O = postfix(O, '을(를)')
        H_e = pick_e(H)
        H = f'{H_e}가'
        p2 = random.choice(["를", ""])
        templates = [
            f'{H} {M}개의 {O} 꺼내었습니다.',
            f'{H} {M}개의 {O} 꺼냈습니다.',
            f'{H} {M}개의 {O} 가져갔습니다.',
            f'{H} {M}개의 {O} 집어갔습니다.',
            f'{H} {M}개{p2} 꺼내었습니다.',
            f'{H} {M}개{p2} 꺼냈습니다.',
            f'{H} {M}개{p2} 가져갔습니다.',
            f'{H} {M}개{p2} 집어갔습니다.',
            f'{O} {H} {M}개{p2} 꺼내었습니다.',
            f'{O} {H} {M}개{p2} 꺼냈습니다.',
            f'{O} {H} {M}개{p2} 가져갔습니다.',
            f'{O} {H} {M}개{p2} 집어갔습니다.',
        ]
        t1 = [
            f'{container} 안에서 ',
            f'{container}에서 ',
        ]
        if random.random() < 0.5:
            return random.choice(t1) + random.choice(templates)
        else:
            return random.choice(templates)

    def end(C, O):
        O1 = postfix(O, '이(가)')
        O3 = postfix(O, '은(는)')
        templates = [
            f'{C} 안에 있는 {O3} 모두 몇 개입니까?',
            f'{C} 안에 있는 {O3} 몇 개입니까?',
            f'{C} 안에 있는 {O3} 전부 몇 개입니까?',
            f'{C} 안에는 총 몇 개의 {O1} 있습니까?',
            f'{C} 안에는 몇 개의 {O1} 있습니까?',
            f'몇 개의 {O1} {C} 안에 있습니까?',
            f'총 몇 개의 {O1} {C} 안에 있습니까?',
        ]
        return random.choice(templates)

    # initialize
    MAX_N = 100
    MAX_M = 100
    MAX_repeat = 3
    INIT = 0
    ADD = 1
    SUB = 2

    container = random.choice(CONTAINERS)
    obj = random.choice(OBJECTS)

    # generate
    inputs = []
    init_index = None
    solution_lst = []
    questions = []

    r = random.randint(1, MAX_repeat)
    func_lst = [random.choice([add, sub]) for _ in range(r)]
    func_lst.append(init)

    random.shuffle(func_lst)

    index = 0
    for func in func_lst:
        name = random.choice(PEOPLE_NAMES)
        value = random.randint(1, MAX_M)
        if func == init:
            value = random.randint(1, MAX_N)
            key = INIT
        else:
            if func == add:
                key = ADD
            else:
                key = SUB
        if key == INIT:
            init_index = index
        else:
            solution_lst.append((key, index, value))
        if key == INIT and index != 0:
            questions.append(init_middle(container, name, value, obj))
        else:
            questions.append(func(container, name, value, obj))
        inputs.append(value)
        index += 1

    questions.append(end(container, obj))

    # initialize
    init_inputs = []
    for i, v in enumerate(inputs):
        init_inputs.append(f'n{i} = {v}')

    # solution
    solution_length = len(solution_lst)
    target_index = 0
    solutions = []
    prev = None

    for i, ret in enumerate(solution_lst):
        key, index, value = ret
        solution = '{} = {} {} {}'
        if i == 0:
            prev = init_index
            if key == ADD:
                solution = solution.format({}, f'n{prev}', '+', f'n{index}')
            elif key == SUB:
                solution = solution.format({}, f'n{prev}', '-', f'n{index}')
        else:
            if key == ADD:
                solution = solution.format({}, f't{prev}', '+', f'n{index}')
            elif key == SUB:
                solution = solution.format({}, f't{prev}', '-', f'n{index}')
        if i == solution_length - 1:
            solution = solution.format('answer')
        else:
            solution = solution.format(f't{target_index}')
            prev = target_index
            target_index += 1
        solutions.append(solution)

    question = ' '.join(questions)

    model_output = ''
    model_output += NEWLINE.join(init_inputs)
    model_output += NEWLINE
    model_output += NEWLINE.join(solutions)

    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return question, model_output, code, answer


def simple_arithmetic_1_1():
    """
    template: "subject 책 x권 중에서 y권을 읽었는데 subject 책 z권을 선물 받았습니다. 읽지 않은 subject 책은 몇 권입니까?"
    """

    all_str = random.choice(["모두 ", "전부 ", ""])
    obj = random.choice(["동화책", "책", "만화책", "소설책", "수학책"])
    obj_option = random.choice([f"{obj} ", ""])
    p1, p2 = random.sample(PEOPLE_NAMES, 2)
    p1_e = pick_e(p1)
    p2_e = pick_e(p2)
    p1_str = random.choice([
        f"{p1_e}가 ", ""
    ])
    p2_str = random.choice([
        f"{p2_e}에게 ", ""
    ])
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = a + b + random.randint(0, 100)
    target, key1 = random.choice([
        (f" 읽지 않은 {obj}은 {all_str}몇 권입니까?", 0),
        (f" 읽은 {obj}은 {all_str}몇 권입니까?", 1),
    ])

    question, key2 = random.choice([
        (f"{p1_str}{obj} {c}권 중에서 {a}권을 읽고 {obj_option}{b}권을 더 읽었습니다.", 0),
        (f"{p1_str}{obj} {c}권 중에서 {a}권을 읽었는데 {p2_str}{obj_option}{b}권을 선물 받았습니다.", 1),
        (f"{p1_str}{obj} {c}권 중에서 {a}권을 읽었는데 {obj_option}{b}권을 더 샀습니다.", 1),
    ])

    init_n = []
    model_logic = []

    question += target

    init_n.append(f"n0 = {c}")
    init_n.append(f"n1 = {a}")
    init_n.append(f"n2 = {b}")

    if key2 == 0:
        if key1 == 0:
            model_logic.append(f"t0 = n1 + n2")
            model_logic.append(f"answer = n0 - t0")
        else:
            model_logic.append(f"answer = n1 + n2")
    else:
        if key1 == 0:
            model_logic.append(f"t0 = n0 - n1")
            model_logic.append(f"answer = t0 + n2")
        else:
            model_logic.append(f"answer = n1")

    model_output_lst = init_n + model_logic
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return question, model_output, code, answer


def simple_arithmetic_2_1():
    """
    template: "obj이 x개씩 y봉지, 낱개 z개 있습니다. obj은 모두 몇 개입니까?
               obj가 x장씩 y묶음과 낱개로 z장 있습니다. obj는 모두 몇 장입니까?
               A는 줄넘기를 x번씩 y회한후 z번을 더 했습니다. A는 줄넘기를 모두 몇 번 했습니까?
               A가 obj을 x송이씩 꽃병 y개에 꽂았는데 z송이가 남았습니다. obj은 모두 몇 송이입니까?"
    """
    obj = random.choice(OBJECTS)
    obj_e = postfix(obj, '이')
    obj_n = postfix(obj, '은')

    a = random.randint(5, 20)
    b = random.randint(1, 10)
    c = random.randint(0, a)
    all_str = random.choice(["모두 ", "총 ", "전부 ", ""])

    question = f'{obj_e} {a}개씩 {b}묶음, 낱개로 {c}개 있습니다. {obj_n} {all_str}몇 개입니까?'

    init_n = []
    model_logic = []

    init_n.append(f"n0 = {a}")
    init_n.append(f"n1 = {b}")
    init_n.append(f"n2 = {c}")
    model_logic.append("t0 = n0 * n1")
    model_logic.append("answer = t0 + n2")

    model_output_lst = init_n + model_logic
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return question, model_output, code, answer


def equation_1():
    """
    template: "합이 x이고 차가 y인 두 수가 있습니다. 두 수 중에서 더 작은 수를 구하시오."
    """

    model_logic = []
    op_str = random.choice([
        "큰",
        "작은",
    ])
    x, y = sorted(random.sample(range(1, 300), 2))
    a = x + y
    b = y - x

    question, init_n, a_index, b_index = random.choice([
        (f"합이 {a}이고 차가 {b}인 두 수가 있습니다. 두 수 중에서 더 {op_str} 수를 구하시오.", [f"n0 = {a}", f"n1 = {b}"], 0, 1),
        (f"차가 {b}이고 합이 {a}인 두 수가 있습니다. 두 수 중에서 더 {op_str} 수를 구하시오.", [f"n0 = {b}", f"n1 = {a}"], 1, 0),
    ])
    if op_str == "큰":
        model_logic.append("t0 = n0 + n1")
    else:
        # TODO: abs()
        model_logic.append(f"t0 = abs(n{a_index} - n{b_index})")
    model_logic.append("answer = t0 / 2")

    model_output_lst = init_n + model_logic
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return question, model_output, code, answer


def equation_2():
    """
    template: "A가 책을 펼쳤는데 두 쪽수의 합이 x이었습니다. A가 펼친 두 쪽수 중 큰 수를 쓰시오."
    """

    person = random.choice(PEOPLE_NAMES)
    person_e = pick_e(person)
    subject = random.choice(SUBJECTS + [""])
    op, cond_str1 = ('+', '합이')

    v1 = random.randint(50, 200)
    if op == '*':
        value = v1 * (v1 + 1)
    else:
        value = v1 + (v1 + 1)

    option2 = random.choice([
        "두 쪽수 ",
        "페이지 ",
        "두 페이지 ",
        "쪽수 ",
        "쪽 ",
    ])

    cond2, cond_strs2 = random.choice([
        ('max', ['큰 수를 구하시오.', '큰 수는?', '큰 수의 값은?', '큰 수의 값을 구하면?', '큰 수를 쓰시오.']),
        ('min', ['작은 수를 구하시오.', '작은 수는?', '작은 수의 값은?', '작은 수의 값을 구하면?', '작은 수를 쓰시오.'])
    ])
    cond_str2 = random.choice(cond_strs2)

    model_output_lst = []
    model_output_lst.append(f"n0 = {value}")

    if cond2 == 'max':
        model_output_lst.append(f"answer = n0 // 2 + 1")
    if cond2 == 'min':
        model_output_lst.append(f"answer = n0 // 2")

    question = f"{person_e}가 {subject}책을 펼쳤는데 두 쪽수의 {cond_str1} {value}이었습니다. {person_e}가 펼친 {option2}중 {cond_str2}"
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return question, model_output, code, answer


def equation_3():
    """
    template: "obj1과 obj2이 모두 합해서 x개 있습니다. obj1이 obj2보다 y개 더 적다면 obj1은 몇 개 있습니까?"
    """

    obj1, obj2 = random.sample(OBJECTS, 2)
    obj1_w = postfix(obj1, '와')
    obj2_e = postfix(obj2, '이')
    p = random.choice(PEOPLE_NAMES)
    container = random.choice(CONTAINERS)
    p_e = pick_e(p)

    option1 = random.choice([
        "",
        f"{p_e}네 집에 ",
        f"{container}에 ",
    ])

    t1, t2 = random.sample([obj1, obj2], 2)
    t1_e = postfix(t1, '이')
    target = random.choice([obj1, obj2])
    target_n = postfix(target, '은')
    eomi = random.choice([
        "있습니다.", "있을 때", "있고"
    ])
    all_str = random.choice(["모두 ", "전부 ", ""])

    c = random.randint(10, 100)
    d = random.randint(10, 100)

    flag = False
    if c == d:
        flag = True

    op_gt = random.choice([
        "많을 때", "많다면", "많습니다."
    ])
    op_lt = random.choice([
        "적을 때", "적다면", "적습니다."
    ])
    op_eq = random.choice([
        "같을 때", "같다면", "같습니다."
    ])

    a = c + d
    b = c - d
    # obj1 > obj2
    if b > 0:
        if t1 == obj1:
            op_str = op_gt
        else:
            op_str = op_lt
        if target == obj1:
            op = '+'
        else:
            op = '-'
    # obj1 < obj2
    else:
        if t1 == obj1:
            op_str = op_lt
        else:
            op_str = op_gt
        if target == obj1:
            op = '-'
        else:
            op = '+'
    b = abs(b)

    question = f"{option1}{obj1_w} {obj2_e} {all_str}합해서 {a}개 {eomi} {t1_e} {t2}보다 {b}개 더 {op_str} {target_n} 몇 개 있습니까?"
    if flag:
        op_str = op_eq
        question = f"{option1}{obj1_w} {obj2_e} {all_str}합해서 {a}개 {eomi} {obj1_w} {obj2}의 수가 {op_str} {target_n} 몇 개 있습니까?"

    init_n = []
    model_logic = []

    init_n.append(f"n0 = {a}")
    if not flag:
        init_n.append(f"n1 = {b}")

    if not flag:
        model_logic.append(f"t0 = n0 {op} n1")
        model_logic.append(f"answer = t0 // 2")
    else:
        model_logic.append(f"answer = n0 // 2")

    model_output_lst = init_n + model_logic
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return question, model_output, code, answer


def range_condition_1():
    """
    template: "a부터 b까지의 홀수의 합을 구하시오."
    """

    start, end = sorted(random.sample(range(1, 1000), 2))
    if end + 20 < start:
        end = random.randint(start + 20, 1100)

    n = random.randint(2, 9)
    n_r = postfix(str(n), '으로')
    r = random.randint(0, n - 1)

    range_d = {
        'gte_lte': [
            f'{start}부터 {end}까지',
            f'{start}부터 {end}까지의 자연수 중에서',
            f'{start}부터 {end}까지의 자연수 중에서',
            f'{start}보다 크거나 같고 {end}보다 작거나 같은',
            f'{start}보다 크거나 같고 {end}보다 크지 않은',
            f'{start}보다 작지 않고 {end}보다 작거나 같은',
            f'{start}보다 작지 않고 {end}보다 크지 않은',
        ],
        'gt_lt': [
            f'{start}보다 크고 {end}보다 작은',
            f'{start}보다 작거나 같지 않고 {end}보다 작은',
            f'{start}보다 크고 {end}보다 크거나 같지 않은',
            f'{start}보다 작거나 같지 않고 {end}보다 크거나 같지 않은',
        ],
        'gt_lte': [
            f'{start}보다 크고 {end}보다 작거나 같은',
            f'{start}보다 크고 {end}보다 크지 않은',
            f'{start}보다 작거나 같지 않고 {end}보다 작거나 같은',
            f'{start}보다 작거나 같지 않고 {end}보다 크지 않은',
        ],
        'gte_lt': [
            f'{start}보다 크거나 같고 {end}보다 작은',
            f'{start}보다 크거나 같고 {end}보다 크거나 같지 않은',
            f'{start}보다 작지 않고 {end}보다 작은',
            f'{start}보다 작지 않고 {end}보다 크거나 같지 않은',
        ],
    }

    condition_d = {
        'even': [
            ('짝수', ""),
            ('2로 나누었을때 나머지가 0인 수', "n2 = 2\nn3 = 0"),
            ('2로 나누어 떨어지는 수', "n2 = 2"),
        ],
        'odd': [
            ('홀수', ""),
            ('2로 나누었을때 나머지가 1인 수', "n2 = 2\nn3 = 1"),
            ('2로 나누어 떨어지지 않는 수', "n2 = 2"),
        ],
        'mod': [
            (f'{n_r} 나누었을때 나머지가 {r}인 수', f"n2 = {n}\nn3 = {r}"),
            (f'{n_r} 나누면 {r}이 남는 수', f"n2 = {n}\nn3 = {r}"),
        ],
        'multiple': [
            (f'{n}의 배수', f"n2 = {n}"),
            (f'{n_r} 나누어 떨어지는 수', f"n2 = {n}"),
        ],
    }

    range_key = random.choice(list(range_d.keys()))
    range_str = random.choice(range_d[range_key])
    condition_key = random.choice(list(condition_d.keys()))
    condition_str, cond_init = random.choice(condition_d[condition_key])

    target_key = random.randint(0, 1)
    targets = [
        ["의 합을 구하시오.", "를 모두 더하면?", "를 모두 더한 값은?"],
        ["의 개수는 모두 몇 개입니까?", "는 전부 몇 개입니까?", "의 개수를 구하시오."],
    ]
    target_str = random.choice(targets[target_key])

    question = f"{range_str} {condition_str}{target_str}"

    init_n = []
    model_logic = []

    init_n.append(f"n0 = {start}")
    init_n.append(f"n1 = {end}")
    if cond_init:
        init_n.append(cond_init)

    st_value = "n0 + 1"
    ed_value = "n1"
    if "gte" in range_key:
        st_value = "n0"
    if "lte" in range_key:
        ed_value = "n1 + 1"

    n_value = "n2"
    r_value = "n3"
    if condition_key in ["even", "odd", "multiple"]:
        if "n3" not in cond_init:
            r_value = "0"
        if "n2" not in cond_init:
            n_value = "2"

    if target_key == 0:
        func = "sum"
    else:
        func = "len"

    model_logic.append(f"result = []")
    model_logic.append(f"for i in range({st_value}, {ed_value}):")
    model_logic.append(f"\tif i % {n_value} == {r_value}:")
    model_logic.append(f"\t\tresult.append(i)")
    model_logic.append(f"answer = {func}(result)")

    model_output_lst = init_n + model_logic
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return question, model_output, code, answer


def average_1():
    """
    template: "A, B, C의 수학점수는 각각 x점, y점, z점입니다. 이 셋을 제외한 학급의 수학점수 평균은 a점입니다.
               A네 학급 인원수가 b명일 때, 학급 수학 평균 점수는 몇 점입니까?"
    """

    count = random.randint(2, 5)
    people = random.sample(PEOPLE_NAMES, count)
    subject = random.choice(SUBJECTS)

    tt = []
    for i in range(20, 40):
        if i % count == 0:
            tt.append(i)

    total = random.choice(tt)
    avg = random.randint(30, 70)
    deviation = random.randint(-3, 3)
    diff_sum = deviation * total
    delta = diff_sum // count
    people_str = ', '.join(people)
    people_str_e = pick_e(people_str)

    a, b = random.sample(range(1, 10), 2)
    if count % 2 == 0:
        value_d = [a, -a, b, -b]
    else:
        value_d = [0, a, -a, b, -b]

    value_d = value_d[:count]
    value_d = [value + avg + delta for value in value_d]
    random.shuffle(value_d)
    seq_n_string = '\n'.join([f"n{idx} = {elem}" for idx, elem in enumerate(value_d)])

    value_str = "점, ".join(str(value) for value in value_d)

    eomi = random.choice(["입니다.", '일 때', "이고"])
    op1 = random.choice([f"{subject}점수의 ", ""])
    end = random.choice([
        "평균 점수는 몇 점입니까?",
        "점수의 평균을 구하시오.",
        "점수의 평균은 얼마입니까?",
        "점수의 평균은 몇 점입니까?",
    ])

    question = f"{people_str_e}의 {subject}점수는 각각 {value_str}점 {eomi} 이들을 제외한 {op1}평균은 {avg}점 입니다. " \
               f"학급 인원수가 {total}명일 때 학급 {subject} {end}"

    init_n = []
    model_logic = []

    init_n.append(seq_n_string)
    init_n.append(f"n{count} = {avg}")
    init_n.append(f"n{count + 1} = {total}")

    tis = []
    for i in range(count):
        model_logic.append(f"t{i} = n{i} - n{count}")
        tis.append(f"t{i}")

    ti_sum = " + ".join(tis)
    # TODO: check this. TOO LONG
    model_logic.append(f"answer = n{count} + ({ti_sum}) / n{count + 1}")

    model_output_lst = init_n + model_logic
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return question, model_output, code, answer


def ratio_1():
    """
    template: "A네 반 전체 학생 수는 x명입니다. 그중에서 남학생은 전체의 y_fraction 입니다. 남학생 중에서 안경을 낀 학생은
               남학생 전체의 z_fraction 입니다. A네 반에서 안경을 끼지 않은 남학생은 몇 명입니까?"
    """

    p = random.choice(PEOPLE_NAMES)
    s = random.choice(["남학생", "여학생"])
    target_s = random.choice(["남학생", "여학생"])
    p_e = pick_e(p)

    op1 = random.choice([
        f"{p_e}네 반 ",
        "",
    ])

    eomi1 = random.choice([
        "입니다.",
        "이고,"
    ])

    op2 = random.choice([
        "그 중에서 ",
        "이 중에서 ",
        ""
    ])

    eomi2 = random.choice([
        "입니다.", "이고"
    ])

    eomi3 = random.choice([
        "입니다.", "일 때"
    ])

    op3 = ""
    if op1:
        op3 = op1[:-1] + "에서 "

    target_key = random.randint(0, 1)
    targets = [
        f"{op3}안경을 끼지 않은 {target_s}은 몇 명입니까?",
        f"{op3}안경을 낀 {target_s}은 몇 명입니까?"
    ]
    target_str = targets[target_key]

    d1, d2 = random.sample(range(3, 10), 2)
    a = d1 * d2
    p1 = random.randint(1, d1 - 1)
    p2 = random.randint(1, d2 - 1)
    b = f'{p1}/{d1}'
    c = f'{p2}/{d2}'

    question = f"{op1}전체 학생 수는 {a}명{eomi1} {op2}{s}은 전체의 {b}{eomi2} {target_s} 중에서 안경을 낀 학생은 {c}{eomi3} {target_str}"

    init_n = []
    model_logic = []

    init_n.append(f"n0 = {a}")
    init_n.append(f"n1 = {b}")
    init_n.append(f"n2 = {c}")

    model_logic.append(f"t0 = n0 * n1")
    if target_s == s:
        if target_key == 0:
            model_logic.append("t1 = t0 * n2")
            model_logic.append("answer = t0 - t1")
        else:
            model_logic.append(f"answer = t0 * n2")
    else:
        model_logic.append("t1 = n0 - t0")
        if target_key == 0:
            model_logic.append("t2 = t1 * n2")
            model_logic.append("answer = t1 - t2")
        else:
            model_logic.append(f"answer = t1 * n2")

    model_output_lst = init_n + model_logic
    model_output = NEWLINE.join(model_output_lst)
    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return question, model_output, code, answer
