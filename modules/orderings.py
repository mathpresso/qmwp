# 순서정하기
import random
from ..utils.common import *
from ..utils.utils import get_answer, postprocessing, postfix, pick_e

SIMPLE_EOMIS = ['구하시오.', '구하세요.', '구하여라.', '쓰시오.',
    '알아보세요.', '알아보시오.', '알아보아라.']
EOMIS = ['입니까?', '인가요?', '인가?', '인지 구하시오.', '인지 구하세요.', '인지 구하여라.', '인지 쓰시오.',
    '인지 알아보세요.', '인지 알아보시오.', '인지 알아보아라.']

def _ordering():
    """
    순서정하기 유형
    1-1: x명의 학생들이 한 줄로 줄을 섰습니다. X의 앞에 y명의 학생들이 서 있습니다. X의 뒤에 서 있는 학생은 몇 명입니까?
    1-2: 달리기 시합에서 X는 x등을 했고, Y는 y등을 했습니다. Z는 X보다 잘했지만 Y보다는 못했습니다. Z의 등수는 몇 등입니까?
    1-3: 키가 작은 사람부터 순서대로 x명이 한 줄로 서 있습니다. X가 앞에서부터 y_kr 번째에 서 있습니다.
         키가 큰 사람부터 순서대로 다시 줄을 서면 X는 앞에서부터 몇 번째에 서게 됩니까?

    2-1: 학교에서 subject_seq의 순서로 시험을 봤습니다. x번째로 시험을 본 과목을 무엇입니까?
    2-2: 1-2와 중복
    2-3 학생들이 한 줄로 서 있습니다. X는 맨 뒤에 서 있습니다. Y는 앞에서 x번째에 서 있습니다. X와 Y 사이에 y명이 서 있을 때,
        줄을 서 있는 학생은 모두 몇 명입니까?
    2-4 X는 왼쪽에서 x번째 열, 오른쪽에서 y번째 열, 앞에서 z번째 줄, 뒤에서 w번째 줄에 서서 action를 하고 있습니다.
        각 줄마다 서 있는 학생의 수가 같다고 할 때, action를 하고 있는 학생은 모두 몇 명입니까?
    2-5 도서관에 똑같은 책장이 x개 있습니다. 각 책장은 y층이고, 각 층마다 꽂혀있는 책의 수는 같습니다. subject책은 어느 책장의 
    한 층의 왼쪽에서 z번째, 오른쪽에서 w번째에 꽂혀 있습니다. 도서관의 책장에 꽂혀 있는 책은 모두 몇 권입니까?
    
    code = postprocessing(model_output, question)
    answer = get_answer(code)

    return: Tuple[] or List[Tuple[]]
        question: str
        model output: str
        code: str
        answer: int? str?
    """
    results = []

    # 1-1 유형
    # x명의 학생들이 한 줄로 줄을 섰습니다. X의 앞에 y명의 학생들이 서 있습니다. X의 뒤에 서 있는 학생은 몇 명입니까?
    # 전체 - (앞/뒤 + 1)
    t_1_1 = [
        ('{total}명의 학생들이 한 줄로 줄을 섰습니다. {A}의 앞에 {front}명의 학생들이 서 있습니다. {A}의 앞에 서 있는 학생은 몇 명{eomi}',
         'n0 = {total}\nn1 = {front}\nanswer = n1'),
        ('{total}명의 학생들이 한 줄로 줄을 섰습니다. {A}의 뒤에 {back}명의 학생들이 서 있습니다. {A}의 뒤에 서 있는 학생은 몇 명{eomi}',
         'n0 = {total}\nn1 = {back}\nanswer = n1'),
    ]

    total = random.randint(2, 100)
    front = random.randint(0, total-1)
    back = random.randint(0, total-1)
    rank = random.randint(0, total-1)
    back_rank = random.randint(0, total-1)

    A = pick_e(random.choice(PEOPLE_NAMES))
    animal = random.choice(ANIMAL_NAMES)

    eomi = random.choice(EOMIS)

    o_1_1 = random.choice(t_1_1)
    results.append(
        tuple(map(lambda x: x.format(total=total, front=front, back=back, rank=rank, 
            back_rank=back_rank, A=A, animal=animal, animal_josa=postfix(animal, '은'), eomi=eomi,
        ), o_1_1))
    )

    # 1-2 유형
    # 달리기 시합에서 X는 x등을 했고, Y는 y등을 했습니다. Z는 X보다 잘했지만 Y보다는 못했습니다. Z의 등수는 몇 등입니까?
    t_1_2 = [
        ('달리기 시합에서 {A}는 {former}등을 했고, {B}는 {latter}등을 했습니다. {C}는 {B}보다 잘했지만 {A}보다는 못했습니다. {C}의 등수는 몇 등{eomi}',
         'n0 = {former}\nn1 = {latter}\nanswer = n0 + 1'),
        ('달리기 시합에서 {A}는 {former}등을 했고, {B}는 {latter}등을 했습니다. {C}는 {A}보다 못했지만 {B}보다는 잘했습니다. {C}의 등수는 몇 등{eomi}',
         'n0 = {former}\nn1 = {latter}\nanswer = n0 + 1'),
    ]
    A, B, C = list(map(pick_e, random.sample(PEOPLE_NAMES, 3)))
    former = random.randint(1, 100)
    latter = former + 2
    total = random.randint(3, 100)
    total_1 = total - 1
    front = random.randint(1, total_1 - 1)
    
    test_type = '달리기'

    eomi = random.choice(EOMIS)

    o_1_2 = random.choice(t_1_2)
    results.append(
        tuple(map(lambda x: x.format(A=A, B=B, C=C, former=former, 
            latter=latter, total=total, total_1=total_1, front=front, test_type=test_type, A_rank=former, B_rank=total,
            eomi=eomi,
        ), o_1_2))
    )

    return results

def _postprocess_results(results):
    ret = []
    for result in results:
        question, model_output = result
        code = postprocessing(model_output, question)
        answer = get_answer(code)
        ret.append((question, model_output, code, answer))
    return ret


def ordering(num_samples_to_generate: int = 1_000) -> list:
    """generate ordering (순서정하기 유형) questions

    Args:
        num_samples_to_generate (int, optional): Defaults to 1_000.

    Returns:
        list: list of (question, model output, code, answer)
    """
    results = []
    while num_samples_to_generate > 0:
        temp = _postprocess_results(_ordering())
        if num_samples_to_generate < len(temp):
            return results + random.sample(temp, num_samples_to_generate)
        else:
            results += temp
            num_samples_to_generate -= len(temp)

    return results


if __name__ == "__main__":
    print(ordering())