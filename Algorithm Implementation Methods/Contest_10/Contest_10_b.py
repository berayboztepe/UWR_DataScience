def binomial_coefficient(n, k):
    if k > n:
        return 0
    result = 1
    for i in range(1, k + 1):
        result = result * (n - i + 1) // i
    return result

def challenge_pennants(tables):
    ways_bugs = binomial_coefficient(tables + 4, 5)
    ways_features = binomial_coefficient(tables + 2, 3)
    total_ways = ways_bugs * ways_features
    print(total_ways)

if __name__ == '__main__':
    n = int(input().strip())
    challenge_pennants(n)
