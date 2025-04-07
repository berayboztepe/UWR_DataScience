def main(k, array):
    a1 = array[0]
    ans = int(1e9)

    for v in range(1, a1 + 1):
        cm = v
        
        for i in range(n):
            p = min(k, array[i] // v if v != 0 else k)
            cm = max(cm, array[i] // p)
        
        ans = min(ans, cm - v)
        
    return ans

if __name__ == '__main__':
    n = int(input())
    for i in range(n):
        n, k = list(map(int, input().split()))
        array = list(map(int, input().split()))

        ans = main(k, array)
        print(ans)