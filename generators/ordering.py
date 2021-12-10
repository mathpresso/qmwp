# 순서정하기
import random

from utils.common import *
from utils.utils import get_answer, pick_e, postfix, postprocessing

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
    front = random.randint(0, total - 1)
    back = random.randint(0, total - 1)
    rank = random.randint(0, total - 1)
    back_rank = random.randint(0, total - 1)

    A = pick_e(random.choice(PEOPLE_NAMES))
    animal = random.choice(ANIMAL_NAMES)

    eomi = random.choice(EOMIS)

    o_1_1 = random.choice(t_1_1)
    results.append(
        tuple(map(lambda x: x.format(total=total, front=front, back=back, rank=rank,
                                     back_rank=back_rank, A=A, animal=animal, animal_josa=postfix(animal, '은'),
                                     eomi=eomi,
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
                                     latter=latter, total=total, total_1=total_1, front=front, test_type=test_type,
                                     A_rank=former, B_rank=total,
                                     eomi=eomi,
                                     ), o_1_2))
    )

    # 1-3 유형
    # 키가 작은 사람부터 순서대로 x명이 한 줄로 서 있습니다. X가 앞에서부터 y_kr 번째에 서 있습니다.
    # 키가 큰 사람부터 순서대로 다시 줄을 서면 X는 앞에서부터 몇 번째에 서게 됩니까?
    # reversed = 전체 - (본인 - 1)
    t_1_3_1 = [
        (['키가 작은 사람부터 순서대로 {total}명이 한 줄로 서 있습니다. {A}가 앞에서부터 {rank} 번째에 서 있습니다. '
          '키가 큰 사람부터 순서대로 다시 줄을 서면 {A}는 앞에서부터 몇 번째에 서게 됩니까?'],
         'n0 = {total}\nn1 = {rank}\nt0 = n0 - n1\nanswer = t0 + 1'),
    ]

    seq_len = random.randint(3, 9)
    rank = random.randint(1, seq_len)
    A = pick_e(random.choice(PEOPLE_NAMES))
    seq = random.sample(range(100), seq_len)
    seq_str = ', '.join([str(i) for i in seq])
    seq_josa = postfix(seq_str, '을(를)')
    eomi = random.choice(['에 쓰인 수를 ', '의 값을 ', '에 적힌 숫자를 ', '에 쓰인 값을 ']) \
           + random.choice(SIMPLE_EOMIS)

    t_1_3_all = [t_1_3_1]
    t_1_3 = random.choice(t_1_3_all)
    if t_1_3 == t_1_3_1:
        n_index = 1
        seq_n_string = '\n'.join([f"n{idx + n_index} = {elem}" for idx, elem in enumerate(seq)])
        n_index = 0
    else:
        n_index = 0
        seq_n_string = '\n'.join([f"n{idx + n_index} = {elem}" for idx, elem in enumerate(seq)])
        n_index = len(seq)

    o_1_3 = random.choice(t_1_3)
    q_1_3 = random.choice(o_1_3[0])
    s_1_3 = o_1_3[1]
    question = q_1_3.format(A=A, total=total, rank=rank, seq=seq, seq_str=seq_str, seq_josa=seq_josa,
                            n_index=n_index, seq_n_string=seq_n_string, eomi=eomi)
    model_output = s_1_3.format(A=A, total=total, rank=rank, seq=seq, seq_str=seq_str, seq_josa=seq_josa,
                                n_index=n_index, seq_n_string=seq_n_string, eomi=eomi)
    results.append((question, model_output))

    # 2-1 유형
    # 학교에서 subject_seq의 순서로 시험을 봤습니다. x번째로 시험을 본 과목을 무엇입니까?
    # l0 = [국어, 수학, 영어, 과학, 사회]; answer = l0[n0 - 1]
    t_2_1 = [
        ('학교에서 {subject_seq_q}의 순서로 시험을 봤습니다. {subject_i} 번째로 시험을 본 과목은 무엇{eomi}',
         'n0 = {subject_i}\nl0 = [{subject_seq}]\nanswer = l0[n0 - 1]')
    ]
    front = random.randint(1, 100)
    back = front + random.randint(1, 100)
    rank = random.randint(1, back - front + 1)

    subject_count = random.randint(3, len(SUBJECTS))
    subjects = random.sample(SUBJECTS, subject_count)
    subject_seq_q = ', '.join(subjects)
    subject_seq = ', '.join([f"'{x}'" for x in subjects])
    subject_i = random.randint(1, len(subjects))

    eomi = random.choice(EOMIS)

    o_2_1 = random.choice(t_2_1)
    results.append(
        tuple(map(lambda x: x.format(
            front=front, back=back, rank=rank,
            subject_seq_q=subject_seq_q, subject_seq=subject_seq, subject_i=subject_i,
            seq_str=seq_str, seq_n_string=seq_n_string, eomi=eomi,
        ), o_2_1))
    )

    # 2-2
    # 1-2와 중복

    # 2-3
    # 학생들이 한 줄로 서 있습니다. X는 맨 뒤에 서 있습니다. Y는 앞에서 x번째에 서 있습니다. X와 Y 사이에 y명이 서 있을 때,
    # 줄을 서 있는 학생은 모두 몇 명입니까?
    t_2_3 = [
        ('학생들이 한 줄로 서 있습니다. {A}는 맨 뒤에 서 있습니다. {B}는 앞에서 {front}번째에 서 있습니다. '
         '{A}와 {B} 사이에 {between}명이 서 있을 때, 줄을 서 있는 학생은 모두 몇 명{eomi}',
         'n0 = {front}\nn1 = {between}\nanswer = n0 + n1 + 1'),
    ]

    A, B = list(map(pick_e, random.sample(PEOPLE_NAMES, 2)))
    front = random.randint(1, 20)
    back = random.randint(1, 20)
    between = random.randint(1, 20)

    eomi = random.choice(EOMIS)

    o_2_3 = random.choice(t_2_3)
    results.append(
        tuple(map(lambda x: x.format(
            A=A, B=B, front=front, back=back, between=between, eomi=eomi,
        ), o_2_3))
    )

    # 2-4
    # X는 왼쪽에서 x번째 열, 오른쪽에서 y번째 열, 앞에서 z번째 줄, 뒤에서 w번째 줄에 서서 action를 하고 있습니다.
    # 각 줄마다 서 있는 학생의 수가 같다고 할 때, action를 하고 있는 학생은 모두 몇 명입니까?
    t_2_4 = [
        ('{A}는 왼쪽에서 {left}번째 열, 오른쪽에서 {right}번째 열, 앞에서 {front}번째 줄, 뒤에서 {back}번째 줄에 서서 체조를 하고 있습니다. '
         '각 줄마다 서 있는 학생의 수가 같다고 할 때, 체조를 하고 있는 학생은 모두 몇 명{eomi}',
         'n0 = {left}\nn1 = {right}\nn2 = {front}\nn3 = {back}\nt0 = n0 + n1\n'
         't1 = t0 - 1\nt2 = n2 + n3\nt3 = t2 - 1\nanswer = t1 * t3'),
    ]
    A = pick_e(random.choice(PEOPLE_NAMES))
    front = random.randint(1, 20)
    back = random.randint(1, 20)
    left = random.randint(1, 20)
    right = random.randint(1, 20)

    eomi = random.choice(EOMIS)

    o_2_4 = random.choice(t_2_4)
    results.append(
        tuple(map(lambda x: x.format(
            A=A, front=front, back=back, left=left, right=right, eomi=eomi,
        ), o_2_4))
    )

    # 2-5
    # 도서관에 똑같은 책장이 x개 있습니다. 각 책장은 y층이고, 각 층마다 꽂혀있는 책의 수는 같습니다.
    # subject책은 어느 책장의 한 층의 왼쪽에서 z번째, 오른쪽에서 w번째에 꽂혀 있습니다. 도서관의 책장에 꽂혀 있는 책은 모두 몇 권입니까?
    t_2_5 = [
        ('도서관에 똑같은 책장이 {N}개 있습니다. 각 책장은 {M}층이고, 각 층마다 꽂혀있는 책의 수는 같습니다. '
         '{subject}책은 어느 책장의 한 층의 왼쪽에서 {left}번째, 오른쪽에서 {right}번째에 꽂혀 있습니다. 도서관의 책장에 꽂혀 있는 책은 모두 몇 권{eomi}',
         'n0 = {N}\nn1 = {M}\nn2 = {left}\nn3 = {right}\nt0 = n0 * n1\nt1 = n2 + n3\nt2 = t1 - 1\nanswer = t0 * t2'),
    ]
    N = random.randint(1, 20)
    M = random.randint(1, 20)
    left = random.randint(1, 20)
    right = random.randint(1, 20)
    subject = random.choice(SUBJECTS)

    eomi = random.choice(EOMIS)

    o_2_5 = random.choice(t_2_5)
    results.append(
        tuple(map(lambda x: x.format(
            N=N, M=M, left=left, right=right, subject=subject, eomi=eomi,
        ), o_2_5))
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


def generate_ordering(num_samples_to_generate: int = 1_000) -> list:
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
    print(generate_ordering())
