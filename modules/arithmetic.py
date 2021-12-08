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
