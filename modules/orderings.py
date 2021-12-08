# 순서정하기
import random
from ..utils.common import *
from ..utils.utils import get_answer, postprocessing, postfix, pick_e

SIMPLE_EOMIS = ['구하시오.', '구하세요.', '구하여라.', '쓰시오.',
    '알아보세요.', '알아보시오.', '알아보아라.']
EOMIS = ['입니까?', '인가요?', '인가?', '인지 구하시오.', '인지 구하세요.', '인지 구하여라.', '인지 쓰시오.',
    '인지 알아보세요.', '인지 알아보시오.', '인지 알아보아라.']

def _ordering():
    pass

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