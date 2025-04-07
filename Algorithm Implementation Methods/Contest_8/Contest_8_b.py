def TableTennisWinner(n, k, a):
    current_winner = a[0]
    win_count = 0

    for i in range(1, n):
        if current_winner > a[i]:
            win_count += 1
        else:
            current_winner = a[i]
            win_count = 1

        if win_count == k:
            print(current_winner)
            return

    print(max(a))


if __name__ == '__main__':
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    TableTennisWinner(n, k, a)
