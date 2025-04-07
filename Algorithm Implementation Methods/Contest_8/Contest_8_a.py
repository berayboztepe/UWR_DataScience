def MysticPermutation(n, ps):
    if n == 1:
        print(-1)
        return
    
    result = sorted(ps)
    
    for i in range(n):
        if result[i] == ps[i]:
            if i + 1 < n:
                result[i], result[i + 1] = result[i + 1], result[i]
            else:
                result[i], result[i - 1] = result[i - 1], result[i]

    print(' '.join(map(str, result)))



if __name__ == '__main__':
    t = int(input())
    for i in range(t):    
        n = int(input())
        ps = list(map(int, input().split()))
        MysticPermutation(n, ps)
