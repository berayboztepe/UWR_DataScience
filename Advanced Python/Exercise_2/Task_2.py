import time

# fix larger ns
def sudan(n, x, y):
    if n == 0:
        return x + y
    elif y == 0:
        return x
    else:
        # F_{n}(F_{n+1}(x, y), F_{n+1}(x, y) + y + 1)
        previous = sudan(n, x, y - 1)
        return sudan(n - 1, previous, previous + y)
    
def sudan_memoized(n, x, y, memo=None):
    if memo is None:
        memo = {}
    
    if (n, x, y) in memo:
        return memo[(n, x, y)]
    
    if n == 0:
        result = x + y
    elif y == 0:
        result = x
    else:
        previous = sudan_memoized(n, x, y - 1, memo)
        result = sudan_memoized(n - 1, previous, previous + y, memo)
    
    memo[(n, x, y)] = result
    return result


if __name__ == "__main__":
    n = 1
    x = 4
    y = 5

    begin_time = time.time()
    print("Memoized version result:")
    print(sudan_memoized(n, x, y))
    
    print(f"Memoized version takes: {time.time() - begin_time}")
    

    begin_time = time.time()
    print("\nNon-memoized version result:")
    print(sudan(n, x, y))
    print(f"Non-memoized version takes: {time.time() - begin_time}")

