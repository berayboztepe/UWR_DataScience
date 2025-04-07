def balancedArray(n):
    if (n // 2) % 2 != 0:
        print("NO")
        return
    
    print("YES")
    first_half, second_half = [], []
    
    for i in range(1, n // 2 + 1):
        first_half.append(2 * i)
    
    for i in range(1, n // 2):
        second_half.append(2 * i - 1)
    
    second_half.append(first_half[-1] + n // 2 - 1)
    
    print(" ".join(map(str, first_half + second_half)))


if __name__ == '__main__':
    t = int(input())
    for _ in range(t):
        n = int(input())
        balancedArray(n)