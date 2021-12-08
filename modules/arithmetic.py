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
