def main():
    n = int(input())
    s = input()

    x = [0] * (n + 1)
    y = [0] * (n + 1)

    position_x, position_y = 0, 0

    # whole path applied to Calvin
    for p in range(1, n + 1):
        if s[p - 1] == 'R':
            position_x += 1
        elif s[p - 1] == 'L':
            position_x -= 1
        elif s[p - 1] == 'U':
            position_y += 1
        elif s[p - 1] == 'D':
            position_y -= 1

        x[p] = position_x
        y[p] = position_y

    count = 0

    # we are checking if our starting point is the same after applying a contiguous substring
    for start in range(n):
        for finish in range(start + 1, n + 1):
            if x[start] == x[finish] and y[start] == y[finish]:
                count += 1

    print(count)

if __name__ == "__main__":
    main()
