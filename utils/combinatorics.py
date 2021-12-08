def num_permutations(n_l: list, r: int):
    """
    --------------------------------------------------------------------------------------------------------------------
    숫자 list 를 받아서, 그 중 중복선택하지 않고 중복하지 않고 만들 수 있는 r 자리 숫자 리스트를 반환
    :param n_l: [0, 1, 2, 1, 3]
    :param r: 2
    :return: [10, 12, 11, 13, 20, 21, 23, 30, 31, 32]
    --------------------------------------------------------------------------------------------------------------------
    하는 exec 가능한 코드 str 출력

    주의사항
    from itertools import permutation 함수는
    리스트에 중복된 객체가 존재하면, 값이 같아도 다른 객체로 판단하고 permutation 을 적용
    예)
    list(permutations([1,2,1,3], 2))
    -> [(1, 2), (1, 1), (1, 3), (2, 1), (2, 1), (2, 3), (1, 1), (1, 2), (1, 3), (3, 1), (3, 2), (3, 1)]
    (2, 1) 이 여러번 등장함
    """

    result = 'from itertools import permutations\n' \
             'result = []\n' \
             'for c in permutations({0}, {1}):\n' \
             '\tnum = int(\'\'.join(str(i) for i in c))\n' \
             '\tif len(str(num)) == {1} and num not in result:\n' \
             '\t\tresult.append(num)'

    return result.format(n_l, r)


def count_digit(n, m, l_n):
    # result = 0
    # for i in range(n, m+1):
    #     result += str(i).count(str(l))
    result = f'result = 0\n' \
             f'for i in range({n}, {m}):\n' \
             f'\tresult += str(i).count(str({l_n}))'
    return result


def filter_sum(tup_l, n):
    result = f'result = []\n' \
             f'for t in {tup_l}:\n' \
             f'\tif sum(t) == {n}:\n' \
             f'\t\tresult.append(t)\n'
    return result
