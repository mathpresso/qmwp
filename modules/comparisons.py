# 크기 비교
from random import choice, choices, randint, sample

from ..utils.common import *
from ..utils.utils import get_answer, pick_e, postfix, postprocessing, _generate_number

SIMPLE_EOMIS = ['구하시오.', '구하세요.', '구하여라.', '쓰시오.',
    '알아보세요.', '알아보시오.', '알아보아라.']
EOMIS = ['입니까?', '인가요?', '인가?', '인지 구하시오.', '인지 구하세요.', '인지 구하여라.', '인지 쓰시오.',
    '인지 알아보세요.', '인지 알아보시오.', '인지 알아보아라.']


def _comparison():
    pass


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