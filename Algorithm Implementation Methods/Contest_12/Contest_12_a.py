def littlePony(m, n):
    expected_value = 0
    for i in range(1, m + 1):
        prob_i = (i / m) ** n
        prob_i_minus_1 = ((i - 1) / m) ** n if i > 1 else 0
        expected_value += i * (prob_i - prob_i_minus_1)

    print(expected_value)


if __name__ == '__main__':
    m, n = list(map(int, input().split()))
    littlePony(m, n)