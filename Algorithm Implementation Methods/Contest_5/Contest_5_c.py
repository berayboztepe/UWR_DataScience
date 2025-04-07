def main(m, x, y, grid):
    cost_white = [0] * m
    cost_black = [0] * m
    
    for col in range(m):
        for row in range(n):
            if grid[row][col] == '#':
                cost_white[col] += 1
            else:
                cost_black[col] += 1
    
    white_prefix = [0] * (m + 1)
    black_prefix = [0] * (m + 1)
    
    for col in range(m):
        white_prefix[col + 1] = white_prefix[col] + cost_white[col]
        black_prefix[col + 1] = black_prefix[col] + cost_black[col]
    
    inf = float('inf')
    dp = [[inf, inf] for _ in range(m + 1)]
    dp[0][0] = dp[0][1] = 0
    
    for i in range(1, m + 1):
        for k in range(x, y + 1):
            if i - k >= 0:
                dp[i][0] = min(dp[i][0], dp[i - k][1] + white_prefix[i] - white_prefix[i - k])
                dp[i][1] = min(dp[i][1], dp[i - k][0] + black_prefix[i] - black_prefix[i - k])
    
    result = min(dp[m][0], dp[m][1])
    print(result)

if __name__ == '__main__':
    n, m, x, y = map(int, input().strip().split())
    grid = [input().strip() for _ in range(n)]
    main(m, x, y, grid)
