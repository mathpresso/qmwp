# 도형 서술
from random import choice, randint, sample
from utils.utils import get_answer, postprocessing


Q_EOMIS = ['입니까?', '인가요?', '인가?', '인지 구하시오.', '인지 구하세요.', '인지 구하여라.', '인지 쓰시오.',
           '인지 알아보세요.', '인지 알아보시오.', '인지 알아보아라.']
SIMPLE_Q_EOMIS = ['구하시오.', '구하세요.', '구하여라.', '쓰시오.',
                  '알아보세요.', '알아보시오.', '알아보아라.']
EOMIS = ['다.', '습니다.', '어요.', '고', '고,']
METER_UNITS = ['cm', 'm', 'km']
SQUARED_METER_UNITS = {
    'cm': ['제곱센티미터', '㎠', '㎠(제곱센티미터)', '제곱센티미터(㎠)'],
    'm': ['제곱미터', '㎡', '㎡(제곱미터)', '제곱미터(㎡)'],
    'km': ['제곱킬로미터', '㎢', '㎢(제곱킬로미터)', '제곱킬로미터(㎢)'],
}
CUBED_METER_UNITS = {
    'cm': ['세제곱센티미터', '㎤', '㎤(세제곱센티미터)', '세제곱센티미터(㎤)'],
    'm': ['세제곱미터', '㎥', '㎥(세제곱미터)', '세제곱미터(㎥)'],
    'km': ['세제곱킬로미터', '㎦', '㎦(세제곱킬로미터)', '세제곱킬로미터(㎦)'],
}
PI_STRS = [
    # front
    [
        '원주율은 {pi}일 때,',
        '원주율은 {pi}라고 할 때,',
        '원주율이 {pi}일 때,',
        '원주율이 {pi}라고 할 때,',
        '원주율이 {pi}라고 하자.',
    ],
    # back
    [
        '(원주율: {pi})',
        '(원주율 : {pi})',
        '(원주율:{pi})',
        '(원주율 = {pi})',
        '(원주율={pi})',
        '(단, 원주율은 {pi}.)',
        '단, 원주율은 {pi}.',
    ],
]
PIS = ['3', '3.1', '3.14', '3.141', '3.1415']


def rectangle_circumference():
    """사(n)각형의 둘레의 길이를 묻는 유형

    Returns:
        List
    """
    results = []
    t_1_1 = [
        (
            '길이가 {total}{unit_s}인 철사로 직4각형을 만들었더니 철사가 남지도 모자라지도 않았{eomi} 직4각형의 가로 길이가 '
            '{width}{unit_s}일 때, 세로 길이는 몇 {unit}{q_eomi}',
            'n0 = {total}\nn1 = 4\nn2 = 4\nn3 = {width}\nt0 = n0 / 2\nanswer = t0 - n3'
        ),
        (
            '길이가 {total}{unit_s}인 철사를 모두 사용해서 직4각형을 만들었{eomi} 직4각형의 가로 길이가 {width}{unit_s}일 때, '
            '세로 길이는 몇 {unit}{q_eomi}',
            'n0 = {total}\nn1 = 4\nn2 = 4\nn3 = {width}\nt0 = n0 / 2\nanswer = t0 - n3'
        ),
        (
            '길이가 {total}{unit_s}인 철사로 직4각형을 만들었더니 철사가 남지도 모자라지도 않았{eomi} 직4각형의 세로 길이가 '
            '{width}{unit_s}일 때, 가로 길이는 몇 {unit}{q_eomi}',
            'n0 = {total}\nn1 = 4\nn2 = 4\nn3 = {width}\nt0 = n0 / 2\nanswer = t0 - n3'
        ),
        (
            '길이가 {total}{unit_s}인 철사를 모두 사용해서 직4각형을 만들었{eomi} 직4각형의 세로 길이가 {width}{unit_s}일 때, '
            '가로 길이는 몇 {unit}{q_eomi}',
            'n0 = {total}\nn1 = 4\nn2 = 4\nn3 = {width}\nt0 = n0 / 2\nanswer = t0 - n3'
        ),
        (
            '한 변의 길이가 {width_reg}{unit_s}인 정{n}각형과 둘레가 같은 정{m}각형이 있{eomi} '
            '이 정{m}각형의 한 변의 길이는 몇 {unit}{q_eomi}',
            'n0 = {width_reg}\nn1 = {n}\nn2 = {m}\nn3 = {m}\nt0 = n0 * n1\nanswer = t0 / n3'
        ),
        (
            '둘레가 {total}{unit_s}인 직4각형이 있습니다. 이 직4각형의 가로 길이가 세로 길이의 {mult}배일 때 가로는 몇 {unit_s}{q_eomi}',
            'n0 = {total}\nn1 = 4\nn2 = 4\nn3 = {mult}\nt0 = n0 / 2\nt1 = n3 + 1\nt2 = t0 / t1\nanswer = t2 * n3'
        ),
        (
            '한 변의 길이가 5cm인 정{n}각형의 둘레는 몇 {unit_s}{q_eomi}',
            'n0 = 5\nn1 = {n}\nanswer = n0 * n1'
        ),
    ]

    total = randint(4, 1000)
    width = randint(1, total//2)

    n = randint(3, 20)
    m = randint(3, 20)

    mult = randint(2, 10)

    q_eomi = choice(Q_EOMIS)
    eomi = choice(EOMIS)
    unit = choice(METER_UNITS)
    unit_s= choice(['', ' ']) + unit

    o_1_1 = choice(t_1_1)
    results.append(
        tuple(map(lambda x: x.format(
            total=total, width=width, q_eomi=q_eomi, width_reg=width, eomi=eomi, n=n, m=m, unit=unit,
            unit_s=unit_s, mult=mult,
        ), o_1_1))
    )
    return results


def _figure() -> list:
    """
    # 도형 서술 유형

    - 길이가 acm인 철사로 직4각형을 만들었더니 철사가 남지도 모자라지도 않았습니다. 직4각형의 가로 길이가 bcm일 때, 세로 길이는 몇 cm입니까?
    - 한 변의 길이가 acm인 정4각형과 둘레가 같은 정8각형이 있습니다. 이 정8각형의 한 변의 길이는 몇 cm입니까?
    - 둘레가 acm인 직4각형이 있습니다. 이 직4각형의 가로 길이가 세로 길이의 b배일 때 가로는 몇 cm입니까?
    - 3각형의 변의 개수와 4각형의 변의 개수의 합을 구하시오.
    - 철사로 한 모서리의 길이가 acm인 정6면체를 만들려고 합니다. 철사는 적어도 몇 cm가 필요합니까?
    - 한 변의 길이가 acm인 정3각형의 둘레는 몇 cm입니까?
    """
    results = []
    for i in [rectangle_circumference]:
        for question, model_output in i():
            try:
                code = postprocessing(model_output, question)
                answer = get_answer(code)
            except:
                print(question, model_output)
                raise Exception("something wrong")
            results.append((question, model_output, code, answer))
    return results


def figure(num_samples_to_generate: int = 1_000) -> list:
    """generate figure (도형서술 유형) questions

    Args:
        num_samples_to_generate (int, optional): Defaults to 1_000.

    Returns:
        list: list of (question, model output, code, answer)
    """
    results = []
    while num_samples_to_generate > 0:
        temp = _figure()
        if num_samples_to_generate < len(temp):
            return results + sample(temp, num_samples_to_generate)
        else:
            results += temp
            num_samples_to_generate -= len(temp)
    return results
