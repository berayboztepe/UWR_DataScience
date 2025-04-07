def bagOfMice(w, b):
    dp = [[-1 for _ in range(b + 1)] for _ in range(w + 1)]

    def solve(w, b):
        if w <= 0:
            return 0.0
        if b <= 0:
            return 1.0
        if dp[w][b] != -1:
            return dp[w][b]

        prob_princess = w / (w + b)
        prob_dragon = b / (w + b)

        temp_b = b - 1
        prob_dragon *= temp_b / (w + temp_b)
        temp_b -= 1

        if prob_dragon > 1e-10:
            b_mice = solve(w, temp_b - 1) * (temp_b / (w + temp_b))
            w_mice = solve(w - 1, temp_b) * (w / (w + temp_b))
            prob_princess += prob_dragon * (b_mice + w_mice)

        dp[w][b] = prob_princess
        return prob_princess

    result = solve(w, b)
    print(result)


if __name__ == '__main__':
    w, b = list(map(int, input().split()))
    bagOfMice(w, b)
