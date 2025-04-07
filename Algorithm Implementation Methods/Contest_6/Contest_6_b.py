def FridgeLockers(n, m, weights):
    n = len(weights)
    if n == 2:
        print(-1)
        return
    
    total_cost = 0
    chains = []
    
    for i in range(n):
        u = i + 1
        v = (i + 1) % n + 1
        total_cost += weights[i] + weights[(i + 1) % n]
        chains.append((u, v))
    
    if m < n:
        print(-1)
        return
    
    print(total_cost)
    for u, v in chains:
        print(u, v)


if __name__ == '__main__':
    T = int(input())
    for i in range(T):
        n, m = map(int, input().split())
        weights = list(map(int, input().split()))
        FridgeLockers(n, m, weights)