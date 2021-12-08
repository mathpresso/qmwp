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


def num_permutations_partition_sub(n_l: list):
    """
    숫자 리스트를 반반으로 쪼개서 값의 차이들을 list of int 로 result에 선언하는 코드 str
    """
    # from itertools import permutations
    #
    # def is_val_str_int(s):
    #     return len(str(int(s))) == len(s)
    #
    # def n_seq_to_str(t):
    #     result = ''
    #     for i in t:
    #         result += str(i)
    #     return result
    #
    # result = []
    # n_len = len(n_l)
    # h_len = n_len // 2
    # tmp_num_l = list(permutations(n_l, n_len))
    # for tmp_tup in tmp_num_l:
    #     val_s1, val_s2 = n_seq_to_str(tmp_tup[:h_len]), n_seq_to_str(tmp_tup[h_len:])
    #     if is_val_str_int(val_s1) and is_val_str_int(val_s2):
    #         result.append(int(val_s1) - int(val_s2))
    # print(result)
    result = f'from itertools import permutations\n' \
             f'\n' \
             f'def is_val_str_int(s):\n' \
             f'\treturn len(str(int(s))) == len(s)\n' \
             f'\n' \
             f'def n_seq_to_str(t):\n' \
             f'\tresult = \'\'\n' \
             f'\tfor i in t:\n' \
             f'\t\tresult += str(i)\n' \
             f'\treturn result\n' \
             f'\n' \
             f'result = []\n' \
             f'n_len = len({n_l})\n' \
             f'h_len = n_len // 2\n' \
             f'tmp_num_l = list(permutations({n_l}, n_len))\n' \
             f'for tmp_tup in tmp_num_l:\n' \
             f'\tval_s1, val_s2 = n_seq_to_str(tmp_tup[:h_len]), n_seq_to_str(tmp_tup[h_len:])\n' \
             f'\tif is_val_str_int(val_s1) and is_val_str_int(val_s2):\n' \
             f'\t\tresult.append(int(val_s1) - int(val_s2))'
    return result


def num_mul_permutations(n_l: list):
    """
    :param n_l: [1,2,3,4,5]
    """
    # from itertools import permutations
    # result = set()
    # if not op_l:
    #     for c in permutations(n_l, 2):
    #         num = c[0] * c[1]
    #         result.add(num)
    # else:
    #     for c in permutations(n_l, sum(op_l)):
    #         num_1 = int(''.join(str(i) for i in c[:op_l[0]]))
    #         num_2 = int(''.join(str(i) for i in c[op_l[0]:]))
    #         if len(str(num_1)) == op_l[0] and len(str(num_2)) == op_l[1]:
    #             result.add(num_1 * num_2)
    # result = list(result)
    result = f'from itertools import permutations\n' \
             f'result = set()\n' \
             f'for c in permutations({n_l}, 2):\n' \
             f'\tnum = c[0] * c[1]\n' \
             f'\tresult.add(num)\n'
    return result


def num_permutations_filter_add(n_l, n):
    """
    n_l 중에서 두개를 골라 합이 n 인 list of tuple 반환
    중복 고려 x
    """
    # from itertools import permutations
    # result = []
    # for c in permutations(n_l, 2):
    #     if c[0] + c[1] == n:
    #         result.append((c[0], c[1]))
    result = f'from itertools import permutations\n' \
             f'result = []\n' \
             f'for c in permutations({n_l}, 2):\n' \
             f'\tif c[0] + c[1] == {n}:\n' \
             f'\t\tresult.append((c[0], c[1]))'
    return result
