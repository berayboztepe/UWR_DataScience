def balanced_ternary_string(str_list):
    count = [str_list.count(x) for x in [0, 1, 2]]

    for target in [0, 1]:
        for idx, val in enumerate(str_list):
            if count[target] < num // 3 and val > target and count[val] > num // 3:
                count[target], count[val], str_list[idx] = count[target] + 1, count[val] - 1, target


    for target in [2, 1]:
        for idx, val in reversed(list(enumerate(str_list))):
            if count[target] < num // 3 and val < target and count[val] > num // 3:
                count[target], count[val], str_list[idx] = count[target] + 1, count[val] - 1, target


    print(''.join([str(s) for s in str_list]))


if __name__ == '__main__':
    num = int(input())
    s = input().strip()
    str_list = list(map(int, s))
    balanced_ternary_string(str_list)
    