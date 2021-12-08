# 조합하기
import random
from itertools import permutations, combinations
from utils.utils import postprocessing, get_answer


Q_EOMIS = ['입니까?', '인가요?', '인가?', '인지 구하시오.', '인지 구하세요.', '인지 구하여라.', '인지 쓰시오.',
           '인지 알아보세요.', '인지 알아보시오.', '인지 알아보아라.']
SIMPLE_Q_EOMIS = ['구하시오.', '구하세요.', '구하여라.', '쓰시오.',
                  '알아보세요.', '알아보시오.', '알아보아라.']
EOMIS = ['다.', '습니다.', '어요.']
WORD_1 = ['중에서', '중', '사이에서', '에서', '가 있습니다.']

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

digits_long_kr = {
    1: '몇',
    2: '몇십 몇',
    3: '몇백 몇십 몇',
    4: '몇천 몇백 몇십 몇'
}

digits_decimal_kr = {
    1: '일',
    2: '십',
    3: '백',
    4: '천',
    5: '만',
    6: '십만',
    7: '백만',
    8: '천만',
    9: '억',
    10: '십억'
}


def comb_num_seq_counting():
    """
    Rule
    영어 대문자 : 사람이름
    영어 소문자 : 수 or 숫자
    num_seq : 나열된 수 or 숫자
    {영어 소문자}_kr : 숫자, 수 한글화

    t_1_1
        num_seq 중에서 서로 다른 숫자 x개를 뽑아 만들 수 있는 가장 큰 x_kr 자리 수를 구하시오.

    t_1_2
        x부터 y까지 자연수를 쓰려고 합니다. 숫자 z는 모두 몇 번 써야 합니까?

    t_1_3
        x보다 작은 자연수 중에서 서로 다른 y_kr 수를 동시에 뽑으려고 합니다. y_kr 수의 합이 z인 경우의 수를 구하시오.

    t_1_4
        num_seq 중에서 x개를 뽑아 한 번씩 사용하여 x_kr 자리 수를 만들려고 합니다. 만들 수 있는 수 중에서 y_kr의 자리 숫자가 z인 가장 큰 수를 쓰시오.

    t_1_5
        num_seq 를 한 번씩만 사용하여 x_kr 자리 수를 2개 만들려고 합니다. 만든 두 수의 차가 가장 크게 될 때 그 차는 얼마입니까?

    t_1_6
        num_seq 중에서 2개를 골라 곱을 구하려고 합니다. 두 수의 곱이 가장 큰 경우와 가장 작은 경우의 합을 구하시오.

    t_1_7
        num_seq 중 합이 x가 되는 두 수로 곱셈식을 만들었습니다. 두 수의 곱이 가장 큰 경우와 가장 작은 경우의 합을 구하시오.
    """

    sample_l = []

    seq_len = random.randint(3, 7)
    num_seq = random.sample(range(0, 10), seq_len)
    count = random.randint(2, min(seq_len, 4))
    count_kr = digits[count]

    num_perm_l = []
    for c in permutations(num_seq, count):
        num = int(''.join(str(i) for i in c))
        if len(str(num)) == count and num not in num_perm_l:
            num_perm_l.append(num)

    num_perm_l_wo_count = []
    for c in permutations(num_seq, seq_len):
        num = int(''.join(str(i) for i in c))
        if len(str(num)) == seq_len and num not in num_perm_l_wo_count:
            num_perm_l_wo_count.append(num)

    digit_in_count = random.randint(1, count)
    # num_in_seq_with_digit : digit_in_count 의 자리수에 맞는 숫자 in num_seq
    if 0 in num_seq and digit_in_count == count:
        num_seq.remove(0)
        num_in_seq_with_digit = random.choice(num_seq)
        num_seq.append(0)
    else:
        num_in_seq_with_digit = random.choice(num_seq)

    add_val_in_seq_l = []  # list of int
    for c in permutations(num_seq, 2):
        if not c[0] + c[1] in add_val_in_seq_l:
            add_val_in_seq_l.append(c[0] + c[1])
    add_val_in_seq = random.choice(add_val_in_seq_l)

    # '{num_seq_str} 를 한 번씩 사용하여 {digits[seq_len]} 자리 수를 만들려고 합니다. {fixed_num_decimal_kr}인 {digits[seq_len]} 자리 수를 모두 쓰시오.'
    check_num = random.choice(range(1, min(4, seq_len)))
    binary_digit_str = bin(random.choice(range(1, 1 << check_num)))[2:]
    # 자리수 맞추기 : '101' -> '00101'
    while check_num == len(binary_digit_str):
        binary_digit_str = '0' + binary_digit_str
    rand_num_in_perm = str(random.choice(num_perm_l_wo_count))

    txt_l = []
    code_arg_l = []
    code_tuple_l = []
    for i, b in enumerate(binary_digit_str):
        if b == '1':
            txt_l.insert(0, f'{digits_decimal_kr[i+1]}의 자리 숫자가 {rand_num_in_perm[-i-1]}')
            code_arg_l.insert(0, int(rand_num_in_perm[-i-1]))
            code_arg_l.insert(0, int(10 ** i))
            code_tuple_l.append((i+1, int(rand_num_in_perm[-i-1])))

    # problem text object
    num_seq_str = ', '.join([str(i) for i in num_seq])

    # code object
    seq_n_string = '\n'.join([f"n{idx} = {elem}" for idx, elem in enumerate(num_seq)])

    # unit 문구
    simple_q_eomis = random.choice(SIMPLE_Q_EOMIS)
    q_eomis = random.choice(Q_EOMIS)
    word_1 = random.choice(WORD_1)

    t_1_1 = [
        (f'{num_seq_str} {word_1} 서로 다른 숫자 {count}개를 뽑아 만들 수 있는 가장 큰 {count_kr} 자리 수를 {simple_q_eomis}',
         f'{seq_n_string}\n'
         f'n{seq_len} = {count}\n'
         f'n{seq_len + 1} = {count}\n'
         f'l0 = [{num_seq_str}]\n'
         f'num_permutations(l0, n{seq_len})\n'
         f'answer = max(result)'),
    ]

    sample_l.append(random.choice(t_1_1))

    tmp_rand_num = random.sample(range(3, 1000), 2)
    nat_num_min, nat_num_max = min(tmp_rand_num), max(tmp_rand_num)
    rand_digit = random.randint(0, 9)

    t_1_2 = [
        (f'{nat_num_min}부터 {nat_num_max}까지 자연수를 쓰려고 합니다. 숫자 {rand_digit}는 모두 몇 번 써야 합니까?',
         f'n0 = {nat_num_min}\n'
         f'n1 = {nat_num_max}\n'
         f'n2 = {rand_digit}\n'
         f'count_digit(n0, n1, n2)\n'
         f'answer = result')
    ]

    sample_l.append(random.choice(t_1_2))

    tmp_rand_num_1 = random.randint(5, 15)
    tmp_rand_num_2 = random.randint(2, 4)
    sum_l = list(map(lambda x: sum(x), combinations(range(1, tmp_rand_num_1+1), tmp_rand_num_2)))
    tmp_rand_num_3 = random.choice(sum_l)

    t_1_3 = [
        (f'{tmp_rand_num_1}보다 작은 자연수 {word_1} 서로 다른 {digits[tmp_rand_num_2]} 수를 동시에 뽑으려고 합니다. {digits[tmp_rand_num_2]} 수의 합이 {tmp_rand_num_3}인 경우의 수를 {simple_q_eomis}',
         f'n0 = {tmp_rand_num_1}\n'
         f'n1 = {tmp_rand_num_3}\n'
         f't0 = list(combinations(range(1, n0), {tmp_rand_num_2}))\n'
         f'filter_sum(t0, n1)\n'
         f'answer = len(result)'),
    ]

    sample_l.append(random.choice(t_1_3))

    t_1_4 = [
        (f'{num_seq_str} {word_1} {count}개를 뽑아 한 번씩 사용하여 {count_kr} 자리 수를 만들려고 합니다. 만들 수 있는 수 {word_1} {digits_decimal_kr[digit_in_count]}의 자리 숫자가 {num_in_seq_with_digit} 인 가장 큰 수를 {simple_q_eomis}',
         f'{seq_n_string}\n'
         f'n{seq_len} = {count}\n'
         f'n{seq_len+1} = 1\n'
         f'n{seq_len+2} = {count}\n'
         f'n{seq_len+3} = {int(10 ** (digit_in_count-1))}\n'
         f'n{seq_len+4} = {num_in_seq_with_digit}\n'
         f'l0 = [{num_seq_str}]\n'
         f'num_permutations(l0, n{seq_len})\n'
         f't0 = list(filter(lambda x: str(x)[-{digit_in_count}] == str(n{seq_len+4}), result))\n'
         f'answer = max(t0)'),
    ]

    sample_l.append(random.choice(t_1_4))

    tmp_num_1 = random.randint(2, 3)
    seq_len_1_6 = 2 * tmp_num_1
    tmp_num_seq_l = random.sample(range(0, 10), seq_len_1_6)
    num_seq_str_1_6 = tmp_num_seq_l.__repr__()[1:-1]
    seq_n_string_1_6 = '\n'.join([f"n{idx} = {elem}" for idx, elem in enumerate(tmp_num_seq_l)])

    t_1_5 = [
        (f'{num_seq_str_1_6} 를 한 번씩만 사용하여 {digits[tmp_num_1]} 자리 수를 2개 만들려고 합니다. 만든 두 수의 차가 가장 크게 될 때 그 차는 얼마{q_eomis}',
         f'{seq_n_string_1_6}\n'
         f'n{seq_len_1_6} = 1\n'
         f'n{seq_len_1_6+1} = {tmp_num_1}\n'
         f'n{seq_len_1_6+2} = 2\n'
         f'l0 = [{num_seq_str_1_6}]\n'
         f'num_permutations_partition_sub(l0)\n'
         f'answer = max(result)'),
    ]

    sample_l.append(random.choice(t_1_5))

    t_1_6 = [
        (f'{num_seq_str} 중에서 2개를 골라 곱을 구하려고 합니다. 두 수의 곱이 가장 큰 경우와 가장 작은 경우의 합을 {simple_q_eomis}',
         f'{seq_n_string}\n'
         f'n{seq_len} = 2\n'
         f'l0 = [{num_seq_str}]\n'
         f'num_mul_permutations(l0)\n'
         f'answer = max(result) + min(result)'),
    ]

    sample_l.append(random.choice(t_1_6))

    t_1_7 = [
        (f'{num_seq_str} 중 합이 {add_val_in_seq}가 되는 두 수로 곱셈식을 만들었습니다. 두 수의 곱이 가장 큰 경우와 가장 작은 경우의 합을 {simple_q_eomis}',
         f'{seq_n_string}\n'
         f'n{seq_len} = {add_val_in_seq}\n'
         f'l0 = [{num_seq_str}]\n'
         f'num_permutations_filter_add(l0, n{seq_len})\n'
         f't0 = [c[0] * c[1] for c in result]\n'
         f'answer = max(t0) + min(t0)'),
    ]

    sample_l.append(random.choice(t_1_7))

    return sample_l


def _comb() -> list:
    results = []
    for i in [comb_num_seq_counting, ]:
        for question, model_output in i():
            try:
                code = postprocessing(model_output, question)
                answer = get_answer(code)
            except:
                print('==========question=========')
                print(question)
                print('==========model_output======')
                print(model_output)
                print('==========code==========')
                print(code)
                raise Exception("something wrong_comb")
            results.append((question, model_output, code, answer))
    return results


def comb(num_samples_to_generate: int = 1000):
    """generate figure (조합하기) questions

    Args:
        num_samples_to_generate (int, optional): Defaults to 1_000.

    Returns:
        list: list of (question, model output, code, answer)
    """
    results = []
    while num_samples_to_generate > 0:
        temp = _comb()
        if num_samples_to_generate < len(temp):
            return results + random.sample(temp, num_samples_to_generate)
        else:
            results += temp
            num_samples_to_generate -= len(temp)
    return results
