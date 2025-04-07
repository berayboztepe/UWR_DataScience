def muh_and_cube_walls(n, w, a, b):
    if w > n:
        print(0)
        return

    diff_a = [a[i + 1] - a[i] for i in range(n - 1)]
    diff_b = [b[i + 1] - b[i] for i in range(w - 1)]

    if len(diff_b) == 0:
        print(n)
        return
    
    def compute_kmp_table(pattern):
        m = len(pattern)
        ps = [0] * m
        p = 0
        for i in range(1, m):
            while p > 0 and pattern[i] != pattern[p]:
                p = ps[p - 1]
            if pattern[i] == pattern[p]:
                p += 1
                ps[i] = p
        return ps

    def kmp_search(text, pattern):
        n, m = len(text), len(pattern)
        if m == 0:
            return 0
        ps = compute_kmp_table(pattern)
        count, p = 0, 0
        for i in range(n):
            while p > 0 and text[i] != pattern[p]:
                p = ps[p - 1]
            if text[i] == pattern[p]:
                p += 1
            if p == m:
                count += 1
                p = ps[p - 1]
        return count

    result = kmp_search(diff_a, diff_b)
    print(result)


if __name__ == '__main__':
    n, w = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    muh_and_cube_walls(n, w, a, b)
