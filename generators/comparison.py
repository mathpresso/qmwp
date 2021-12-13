# 크기 비교
from random import choice, choices, randint, sample

from utils.common import *
from utils.utils import generate_number, get_answer, pick_e, postfix, postprocessing

SIMPLE_EOMIS = ['구하시오.', '구하세요.', '구하여라.', '쓰시오.',
                '알아보세요.', '알아보시오.', '알아보아라.']
EOMIS = ['입니까?', '인가요?', '인가?', '인지 구하시오.', '인지 구하세요.', '인지 구하여라.', '인지 쓰시오.',
         '인지 알아보세요.', '인지 알아보시오.', '인지 알아보아라.']


def toss_coin():
    if randint(0, 1) == 0:
        return True
    else:
        return False


def _comparison():
    """
    크기비교 유형.

    결국 모든 것은 `절대 비교`, `상대 비교`, `혼합형`으로 나뉜다.

    1-1 (절대 비교) [v]
    X는 x와 y를 모았습니다. Y는 z과 w을 모았습니다. 누가 모은 수가 더 큽니까?

    1-2 (상대 비교)
    ganada_seq x개의 상자가 있습니다. B 상자는 D 상자보다 큽니다.
    A 상자는 D 상자보다 작습니다. B 상자는 C 상자보다 작습니다. 크기가 가장 작은 상자는 무엇입니까?

    1-3 (절대 비교) [v]
    x개의 수 num_seq이 있습니다. 이 중에서 y보다 큰 수는 모두 몇 개입니까?

    2-1 (절대 비교)
    X는 obj를 x개 가지고 있습니다. Y는 obj를 X보다 y개 더 많이 가지고 있고
    Z는 Y보다 z개 더 적게 가지고 있습니다. obj를 가장 적게 가지고 있는 사람은 누구입니까?

    2-2 (절대 비교) [v]
    x_kr 수 A, B, C, D가 있습니다. A는 a입니다. B는 A보다 b 큰 수입니다.
    C는 B보다 c 작은 수입니다. D는 C의 d배인 수입니다. 가장 큰 수는 어느 것입니까?

    2-3 (상대 비교)
    X는 Y보다 무겁고 Z보다 가볍습니다. W는 Z보다 무겁습니다. x명 중 가장 가벼운 사람은 누구입니까?

    2-4 (절대 비교)
    X는 obj를 xl 마셨습니다. Y는 X보다 yl 더 적게 마셨습니다.
    Z는 zl 마셨고, W는 X보다 wl 더 많이 마셨습니다. obj를 가장 많이 마신 사람은 누구입니까?

    2-5 (혼합형) 가장 어려운 유형.
    people_seq x명이 있습니다. A는 나이가 가장 적습니다. B는 C에게는 동생이고 D에게는 형입니다.
    C는 y년 후에 z살이 되고, E는 올해 w살입니다. x명 중에서 나이가 k번째로 적은 사람은 누구입니까?

    Returns:
        list: [description]
    """
    results = []
    for i in (c_1_1, c_1_3, c_2_2):
        while True:
            try:
                question, model_output = i()
                code = postprocessing(model_output, question)
                answer = get_answer(code)
                break
            except:
                continue
        results.append((question, model_output, code, answer))
    return results


def c_1_1():
    """
    # 1-1
    X는 x와 y를 모았습니다. Y는 z과 w을 모았습니다. 누가 모은 수가 더 큽니까?
    """
    t_1_1 = [
        ('{AB} 누가 모은 수가 더 {big_eomi}',
         '{num_init}\nt0 = dict()\n{ops}\nanswer = max(t0, key=t0.get)'),
        ('{AB} 누가 모은 수가 더 {small_eomi}',
         '{num_init}\nt0 = dict()\n{ops}\nanswer = min(t0, key=t0.get)'),
    ]
    len_seq = 2
    seq = sample(PEOPLE_NAMES, len_seq)
    A, B = seq[0], seq[1]
    ops = []
    strings = []
    nums = []
    num12_init = ''
    comma_vs_wa = toss_coin()
    for i in range(len_seq):
        num_seq_len = randint(1, 5)
        num_seq = choices(range(100), k=num_seq_len)
        nums += [f"n{idx + len(nums)} = {elem}" for idx, elem in enumerate(num_seq)]
        if comma_vs_wa:
            strings.append(f"{pick_e(seq[i])}는 " + \
                           ' '.join([f'{postfix(str(j), "와(과)")}' for j in num_seq[:-1]]) + \
                           (' ' if len(num_seq) > 1 else '') + \
                           f"{postfix(str(num_seq[-1]), '을')} 모았습니다.")
        else:
            strings.append(f"{pick_e(seq[i])}는 " + \
                           ', '.join([str(j) for j in num_seq[:-1]]) + \
                           (', ' if len(num_seq) > 1 else '') + \
                           f"{postfix(str(num_seq[-1]), '을')} 모았습니다.")
        ops.append(f"t0['{seq[i]}'] = sum([{', '.join([f'n{len(nums) - j - 1}' for j in range(num_seq_len)[::-1]])}])")
        if i == 1:
            num12_init += '\n'.join(nums)

    eomi = choice(EOMIS)
    big_eomi = '큰' + eomi[1:] if not eomi.startswith('입') else '큽' + eomi[1:]
    small_eomi = '작은' + eomi[1:] if not eomi.startswith('입') else '작습' + eomi[1:]

    # 습니다. + 습니다. -> 고, + 습니다.
    tgt = choice(range(len(strings) - 1))
    strings[tgt] = strings[tgt].replace('습니다.', choice(['고,', '고']))

    o_1_1 = choice(t_1_1)
    return \
        tuple(map(lambda x: x.format(
            num_init='\n'.join(nums), AB=' '.join(strings[:2]),
            A=A, B=B, ops='\n'.join(ops),
            big_eomi=big_eomi, small_eomi=small_eomi, eomi=eomi,
        ), o_1_1))


def c_1_2():
    """
    # 1-2
    ganada_seq x개의 상자가 있습니다. B 상자는 D 상자보다 큽니다.
    A 상자는 D 상자보다 작습니다. B 상자는 C 상자보다 작습니다. 크기가 가장 작은 상자는 무엇입니까?
    """
    # TODO
    return []


def c_1_3():
    """
    # 1-3
    x개의 수 num_seq이 있습니다. 이 중에서 y보다 큰 수는 모두 몇 개입니까?
    """
    t_1_3 = [
        ('{len_seq}개의 수 {seq} 있습니다. 이 중에서 {num}보다 큰 수는 모두 몇 개{eomi}',
         '{n_init_str}\nl0 = [{seq_list}]\nresult = []\nfor i in l0:\n\tif i > {compare}:\n\t\tresult.append(i)\nanswer = len(result)'),
        ('{len_seq}개의 수 {seq} 있습니다. 이 중에서 {num}보다 작은 수는 모두 몇 개{eomi}',
         '{n_init_str}\nl0 = [{seq_list}]\nresult = []\nfor i in l0:\n\tif i < {compare}:\n\t\tresult.append(i)\nanswer = len(result)'),
    ]
    len_seq = randint(2, 7)
    seq = [generate_number() for _ in range(len_seq)]
    num = generate_number()

    n_init_str = "\n".join([f"n{idx} = {elem}" for idx, elem in enumerate([len_seq, *seq, num])])

    eomi = choice(EOMIS)
    simple_eomi = choice(SIMPLE_EOMIS)

    o_1_3 = choice(t_1_3)
    return \
        tuple(map(lambda x: x.format(
            len_seq=len_seq, seq=postfix(', '.join(seq), '이(가)'), seq_list=', '.join(seq),
            num=num, n_init_str=n_init_str, compare=f"n{len(seq) + 1}", eomi=eomi, simple_eomi=simple_eomi,
        ), o_1_3))


def c_2_1():
    """
    # 2-1 (절대 비교)
    X는 obj를 x개 가지고 있습니다. Y는 obj를 X보다 y개 더 많이 가지고 있고
    Z는 Y보다 z개 더 적게 가지고 있습니다. obj를 가장 적게 가지고 있는 사람은 누구입니까?
    """
    # TODO
    return []


def c_2_2():
    """
    # 2-2
    x_kr 수 A, B, C, D가 있습니다. A는 a입니다. B는 A보다 b 큰 수입니다.
    C는 B보다 c 작은 수입니다. D는 C의 d배인 수입니다. 가장 큰 수는 어느 것입니까?
    """
    t_2_2 = [
        ('{len_seq_kr} 수 {seq} 있습니다. {ABCs} 가장 큰 수는 어느 것{eomi}',
         "{n_init}\nt0 = dict()\n{ops}\nanswer = max(t0, key=t0.get)"),
        ('{len_seq_kr} 수 {seq} 있습니다. {ABCs} 가장 작은 수는 어느 것{eomi}',
         "{n_init}\nt0 = dict()\n{ops}\nanswer = min(t0, key=t0.get)"),
    ]
    possibilities = ['init']
    len_seq = randint(2, 7)
    len_seq_kr = KR_NUMS[len_seq]
    seq = VARIABLES[:len_seq]
    ops = []
    strings = []
    nums = []
    for i in range(len_seq):
        p = choice(possibilities)
        num = randint(0, 100)
        nums.append(num)
        if p == 'init':
            strings.append(f"{seq[i]}는 {num}입니다.")
            ops.append(f't0[\'{seq[i]}\'] = n{len(nums) - 1}')
        else:
            comp = choice([
                (f'보다 {num} 큰', '+'),
                (f'보다 {num} 작은', '-'),
                (f'의 {num}배인', '*')])
            strings.append(f"{seq[i]}는 {p}{comp[0]} 수입니다.")
            ops.append(f't0[\'{seq[i]}\'] = t0[\'{p}\'] {comp[1]} n{len(nums) - 1}')
        possibilities.append(seq[i])

    n_init = [f"n{idx} = {elem}" for idx, elem in enumerate(nums)]
    eomi = choice(EOMIS)
    simple_eomi = choice(SIMPLE_EOMIS)

    # 습니다. + 습니다. -> 고, + 습니다.
    tgt = choice(range(len(strings) - 1))
    strings[tgt] = strings[tgt].replace('입니다.', choice(['이고,', '이고']))

    o_2_2 = choice(t_2_2)
    return \
        tuple(map(lambda x: x.format(
            len_seq_kr=len_seq_kr, seq=', '.join(seq), ABCs=' '.join(strings), n_init='\n'.join(n_init),
            ops='\n'.join(ops), eomi=eomi, simple_eomi=simple_eomi,
        ), o_2_2))


def c_2_3():
    """
    # 2-3
    X는 Y보다 무겁고 Z보다 가볍습니다. W는 Z보다 무겁습니다. x명 중 가장 가벼운 사람은 누구입니까?
    1-2와 동치지만 박스 -> 사람 이름 & key로 group
    """
    # TODO
    return []


def c_2_4():
    """
    # 2-4
    지민이는 obj를 0.7l 마셨습니다. 은지는 지민이보다 1/10l 더 적게 마셨습니다.
    윤기는 4/5l 마셨고, 유나는 지민이보다 0.2l 더 많이 마셨습니다. obj를 가장 많이 마신 사람은 누구입니까?
    """
    # TODO
    return []


def c_2_5():
    """
    # 2-5
    people_seq x명이 있습니다. A는 나이가 가장 적습니다. B는 C에게는 동생이고 D에게는 형입니다.
    C는 y년 후에 z살이 되고, E는 올해 w살입니다. x명 중에서 나이가 k번째로 적은 사람은 누구입니까?
    유형: 상대 init (나이가 몇 번째). 상대 비교. 절대 init. 절대 비교.
    """
    # TODO
    return []


def generate_comparison(num_samples_to_generate: int = 1_000) -> list:
    """generate comparison (크기비교 유형) questions

    Args:
        num_samples_to_generate (int, optional): Defaults to 1_000.

    Returns:
        list: list of (question, model output, code, answer)
    """
    results = []
    while num_samples_to_generate > 0:
        temp = _comparison()
        if num_samples_to_generate < len(temp):
            return results + sample(temp, num_samples_to_generate)
        else:
            results += temp
            num_samples_to_generate -= len(temp)
    return results


if __name__ == "__main__":
    print(generate_comparison())
