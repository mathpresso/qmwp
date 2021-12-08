# 크기 비교
from random import choice, choices, randint, sample

from ..utils.common import *
from ..utils.utils import get_answer, pick_e, postfix, postprocessing, _generate_number

SIMPLE_EOMIS = ['구하시오.', '구하세요.', '구하여라.', '쓰시오.',
    '알아보세요.', '알아보시오.', '알아보아라.']
EOMIS = ['입니까?', '인가요?', '인가?', '인지 구하시오.', '인지 구하세요.', '인지 구하여라.', '인지 쓰시오.',
    '인지 알아보세요.', '인지 알아보시오.', '인지 알아보아라.']


def _comparison():
    """
    크기비교 유형.

    결국 모든 것은 `절대 비교`, `상대 비교`, `혼합형`으로 나뉜다.

    1-1 (절대 비교)
    X는 x와 y를 모았습니다. Y는 z과 w을 모았습니다. 누가 모은 수가 더 큽니까?

    1-2 (상대 비교)
    ganada_seq x개의 상자가 있습니다. B 상자는 D 상자보다 큽니다.
    A 상자는 D 상자보다 작습니다. B 상자는 C 상자보다 작습니다. 크기가 가장 작은 상자는 무엇입니까?

    1-3 (절대 비교)
    x개의 수 num_seq이 있습니다. 이 중에서 y보다 큰 수는 모두 몇 개입니까?

    2-1 (절대 비교)
    X는 obj를 x개 가지고 있습니다. Y는 obj를 X보다 y개 더 많이 가지고 있고
    Z는 Y보다 z개 더 적게 가지고 있습니다. obj를 가장 적게 가지고 있는 사람은 누구입니까?

    2-2 (절대 비교)
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
    for i in ():
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


def comparison(num_samples_to_generate: int = 1_000) -> list:
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
    print(comparison())