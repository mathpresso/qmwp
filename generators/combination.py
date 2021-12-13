# 조합하기
import random
from itertools import combinations, permutations, product

from utils.common import ANIMAL_NAMES, COLORS, OBJECTS, PEOPLE_NAMES
from utils.utils import get_answer, postprocessing

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
            txt_l.insert(0, f'{digits_decimal_kr[i + 1]}의 자리 숫자가 {rand_num_in_perm[-i - 1]}')
            code_arg_l.insert(0, int(rand_num_in_perm[-i - 1]))
            code_arg_l.insert(0, int(10 ** i))
            code_tuple_l.append((i + 1, int(rand_num_in_perm[-i - 1])))

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
    sum_l = list(map(lambda x: sum(x), combinations(range(1, tmp_rand_num_1 + 1), tmp_rand_num_2)))
    tmp_rand_num_3 = random.choice(sum_l)

    t_1_3 = [
        (
        f'{tmp_rand_num_1}보다 작은 자연수 {word_1} 서로 다른 {digits[tmp_rand_num_2]} 수를 동시에 뽑으려고 합니다. {digits[tmp_rand_num_2]} 수의 합이 {tmp_rand_num_3}인 경우의 수를 {simple_q_eomis}',
        f'n0 = {tmp_rand_num_1}\n'
        f'n1 = {tmp_rand_num_3}\n'
        f't0 = list(combinations(range(1, n0), {tmp_rand_num_2}))\n'
        f'filter_sum(t0, n1)\n'
        f'answer = len(result)'),
    ]

    sample_l.append(random.choice(t_1_3))

    t_1_4 = [
        (
        f'{num_seq_str} {word_1} {count}개를 뽑아 한 번씩 사용하여 {count_kr} 자리 수를 만들려고 합니다. 만들 수 있는 수 {word_1} {digits_decimal_kr[digit_in_count]}의 자리 숫자가 {num_in_seq_with_digit} 인 가장 큰 수를 {simple_q_eomis}',
        f'{seq_n_string}\n'
        f'n{seq_len} = {count}\n'
        f'n{seq_len + 1} = 1\n'
        f'n{seq_len + 2} = {count}\n'
        f'n{seq_len + 3} = {int(10 ** (digit_in_count - 1))}\n'
        f'n{seq_len + 4} = {num_in_seq_with_digit}\n'
        f'l0 = [{num_seq_str}]\n'
        f'num_permutations(l0, n{seq_len})\n'
        f't0 = list(filter(lambda x: str(x)[-{digit_in_count}] == str(n{seq_len + 4}), result))\n'
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
         f'n{seq_len_1_6 + 1} = {tmp_num_1}\n'
         f'n{seq_len_1_6 + 2} = 2\n'
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


def comb_choice():
    """
    대상들 중에서 지정된 개수를 선택하는 것과 관련된 조합 문제

    Rule
    영어 대문자 : 사람이름
    영어 소문자 : 수 or 숫자
    num_seq : 나열된 수 or 숫자
    {영어 소문자}_kr : 숫자, 수 한글화

    t_2_1
        obj_seq이 1개씩 있습니다. 이 obj1 중 서로 다른 x개의 obj1을 고르는 방법은 모두 몇 가지입니까?

    t_2_2
        obj1 x개를 서로 다른 y_kr 마리의 obj2에게 나누어 주려고 합니다. obj2는 적어도 obj1 1개는 받습니다. obj1를 나누어 주는 방법은 모두 몇 가지입니까?

    t_2_3
        people_seq x명이 한 줄로 설 떄, X, Y이가 이웃하여 서는 경우의 수를 구하시오.

    t_2_4
        두개의 주사위를 동시에 던질 때, 나오는 눈의 수의 합이 x가 되는 경우의 수는 얼마인가?

    t_2_5
        X이가 obj1에서 x원짜리 obj2를 사려고 한다. y원짜리 동전 z개, a원 짜리 동전 b개, c원짜리 동전 d개를 가지고 있을 때, obj2 값을 지불하는 방법의 수는?
    """

    sample_l = []

    # unit 문구
    simple_q_eomis = random.choice(SIMPLE_Q_EOMIS)
    q_eomis = random.choice(Q_EOMIS)

    o1 = random.choice(OBJECTS)

    tmp_num_l = random.sample(range(1, 10), 2)
    n, r = max(tmp_num_l), min(tmp_num_l)
    color_l = random.sample(COLORS, n)

    def o_str(o_l):
        return ', '.join(o_l)

    def o_code(o_l):
        txt_l = []
        for o in o_l:
            txt_l.append('\'' + o + '\'')
        return ', '.join(txt_l)

    def o_with_ad_str(obj, adj_l):
        txt_l = []
        for adj in adj_l:
            txt_l.append(adj + ' ' + obj)
        return ', '.join(txt_l)

    def o_with_ad_code(obj, adj_l):
        txt_l = []
        for adj in adj_l:
            txt_l.append('\'' + adj + ' ' + obj + '\'')
        return ', '.join(txt_l)

    # 기본 조합
    t_2_1 = [
        (f'{o_with_ad_str(o1, color_l)}이 1개씩 있습니다. 이 {o1} 중 서로 다른 {r}개의 {o1}을 고르는 방법은 모두 몇 가지 {q_eomis}',
         f'n0 = 1\n'
         f'n1 = {r}\n'
         f'l0 = [{o_with_ad_code(o1, color_l)}]\n'
         f't0 = list(combinations(l0, n1))\n'
         f'answer = len(t0)'),
    ]

    sample_l.append(random.choice(t_2_1))

    o2 = random.choice(OBJECTS)
    tmp_n_0 = random.randint(2, 4)
    tmp_n_1 = tmp_n_0 + random.randint(0, 5)
    animal = random.choice(ANIMAL_NAMES)

    tmp_w_l_0 = ['합니다.', '하는데,', '할 때,']
    tmp_w_0 = random.choice(tmp_w_l_0)
    # 분배 조합
    t_2_2 = [
        (
        f'{o2} {tmp_n_1}개를 서로 다른 {digits[tmp_n_0]} 마리의 {animal}에게 나누어 주려고 {tmp_w_0} {animal}들은 적어도 {o2} 1개는 받습니다. {o2}를 나누어 주는 방법은 모두 몇 가지{q_eomis}',
        f'n0 = {tmp_n_1}\n'
        f'n1 = 1\n'
        f'C(n0-1, {tmp_n_0}-1)\n'
        f'answer = result'),
    ]

    sample_l.append(random.choice(t_2_2))

    tmp_n_0 = random.randint(3, 7)
    tmp_name_l = random.sample(PEOPLE_NAMES, tmp_n_0)
    tmp_name_l_2 = random.sample(tmp_name_l, 2)

    # 줄세우기
    tmp_w_l_0 = ['설 때,', '세울 때,']
    t_2_3 = [
        (
        f'{o_str(tmp_name_l)} {tmp_n_0}명이 한 줄로 {random.choice(tmp_w_l_0)} {o_str(tmp_name_l_2)}이가 이웃하여 서는 경우의 수를 {simple_q_eomis}',
        f'n0 = {tmp_n_0}\n'
        f'l0 = [{o_code(tmp_name_l)}]\n'
        f'l1 = [{o_code(tmp_name_l_2)}]\n'
        f'answer = math.factorial(n0-1) * 2'),
    ]

    sample_l.append(random.choice(t_2_3))

    # 주사위
    rand_dice_add = random.randint(3, 11)

    t_2_4 = [
        (f'2개의 주사위를 동시에 던질 때, 나오는 눈의 수의 합이 {rand_dice_add}가 되는 경우의 수는 얼마{q_eomis}',
         f'n0 = 2\n'
         f'n1 = {rand_dice_add}\n'
         f'dice_add_eq(n1)\n'
         f'answer = result'),
    ]

    sample_l.append(random.choice(t_2_4))

    # 화폐 모아서 가격 지불하는 경우의 수
    name_2_5 = random.choice(PEOPLE_NAMES)
    MARKET = ['슈퍼마켓', '시장', '슈퍼', '문방구', '문구점', '자판기', '가게', '편의점']
    tmp_obj = random.choice(OBJECTS)
    market_2_5 = random.choice(MARKET)
    coins = [10, 50, 100, 500]
    coin_cnt = random.randint(1, len(coins))
    coin_cnt_dict = {}
    coin_pick = random.sample(coins, coin_cnt)
    for coin in coin_pick:
        coin_cnt_dict[coin] = random.choice(range(1, 9))

    tmp_prod_iter = product(*list(map(lambda x: range(1, x + 1), coin_cnt_dict.values())))
    coin_val_l = []
    for p in tmp_prod_iter:
        coin_val_l.append(sum([x * y for x, y in zip(coin_cnt_dict.keys(), p)]))
    rand_coin_val = random.choice(coin_val_l)

    def tmp_coin_cotext(idx: int, coin_d: dict) -> tuple:
        tmp_txt_l = []
        tmp_code_l = []
        tmp_dict_code_l = []
        for _i, _k in enumerate(coin_d.keys()):
            _coin = _k
            _coin_cnt = coin_d[_k]
            tmp_txt_l.append(f'{_coin}원짜리 동전 {_coin_cnt}개')
            tmp_code_l.append(f'n{idx + 2 * _i} = {_k}')
            tmp_code_l.append(f'n{idx + 1 + 2 * _i} = {_coin_cnt}')
            tmp_dict_code_l.append(f'n{idx + 2 * _i}: n{idx + 1 + 2 * _i}')

        tmp_txt = ', '.join(tmp_txt_l)
        tmp_code = '\n'.join(tmp_code_l)
        tmp_dict_code = '{' + ', '.join(tmp_dict_code_l) + '}'

        return tmp_txt, tmp_code, tmp_dict_code

    t_2_5 = [
        (
        f'{name_2_5}이가 {market_2_5}에서 {rand_coin_val}원짜리 {tmp_obj}를 사려고 한다. {tmp_coin_cotext(1, coin_cnt_dict)[0]}를 가지고 있을 때, {tmp_obj} 값을 지불하는 방법의 수는 얼마{q_eomis}',
        f'n0 = {rand_coin_val}\n'
        f'{tmp_coin_cotext(1, coin_cnt_dict)[1]}\n'
        f't0 = {tmp_coin_cotext(1, coin_cnt_dict)[2]}\n'
        f'count_coin(n0, t0)\n'
        f'answer = result'),
    ]

    sample_l.append(random.choice(t_2_5))

    return sample_l


def _comb() -> list:
    results = []
    for i in [comb_num_seq_counting, comb_choice]:
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


def generate_combination(num_samples_to_generate: int = 1000):
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
