def solve(left, right, arr, n):
    if left > arr[n - 1] or right < arr[0]:
        return 0
    result = 0
    l, r = 0, n - 1
    
    while r - l > 1:
        mid = (l + r) // 2
        if arr[mid] >= left:
            r = mid
        else:
            l = mid
    if arr[l] >= left:
        mid = l
    else:
        mid = r
    result = mid
    
    l, r = 0, n - 1
    
    while r - l > 1:
        mid = (l + r) // 2
        if arr[mid] <= right:
            l = mid
        else:
            r = mid
    if arr[r] <= right:
        mid = r
    else:
        mid = l
    
    return mid - result + 1


def main():
    n, x, k = map(int, input().split())
    arr = list(map(int, input().split()))
    arr.sort()
    ans = 0
    
    for i in range(n):
        y = arr[i] - 1
        y //= x
        left = max(x * (k + y), arr[i])
        right = x * (k + y + 1) - 1
        ans += solve(left, right, arr, n)
    
    print(ans)


if __name__ == "__main__":
    main()
