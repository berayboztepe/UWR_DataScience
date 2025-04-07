def max_cookies(n, k, a, b):
    low, high = 0, 2 * 10**9
    result = 0

    while low <= high:
        mid = (low + high) // 2
        required_powder = 0

        for i in range(n):
            needed = mid * a[i] - b[i]
            if needed > 0:
                required_powder += needed
                if required_powder > k:
                    break

        if required_powder <= k:
            result = mid 
            low = mid + 1
        else:
            high = mid - 1

    return result


if __name__ == '__main__':
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    print(max_cookies(n, k, a, b))
