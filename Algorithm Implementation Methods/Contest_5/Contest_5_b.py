def main(a):
    max_val = max(a)
    count = [0] * (max_val + 1)
    
    for num in a:
        count[num] += 1
    
    dp = [0] * (max_val + 1)
    dp[1] = count[1] * 1
    
    for x in range(2, max_val + 1):
        dp[x] = max(dp[x - 1], dp[x - 2] + x * count[x])
    
    print(dp[max_val])

if __name__ == '__main__':
    n = int(input().strip())
    a = list(map(int, input().strip().split()))
    main(a)
