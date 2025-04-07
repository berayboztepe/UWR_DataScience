def get_diff_character(index, s1, s2):
    c = 'a'
    while c == s1[index] or c == s2[index]:
        c = chr(ord(c) + 1)
    return c

def solve(n, t, s1, s2):
    # Initialize s3 with '.' to denote empty characters
    s3 = ['.' for _ in range(n)]
    q = 0
    diff1 = 0  # Difference between s1 and s3
    diff2 = 0  # Difference between s2 and s3
    
    # Step 1: Copy identical characters between s1 and s2 into s3
    for i in range(n):
        if s1[i] == s2[i] and n - t - q > 0:
            s3[i] = s1[i]
            q += 1
    
    # Step 2: Copy n - t - q characters from s1 into s3
    z = n - t - q
    ind = 0
    while z > 0 and ind < n:
        if s3[ind] != '.':
            ind += 1
            continue
        s3[ind] = s1[ind]
        diff2 += 1
        z -= 1
        ind += 1

    # Step 3: Copy n - t - q characters from s2 into s3
    z = n - t - q
    ind = 0
    while z > 0 and ind < n:
        if s3[ind] != '.':
            ind += 1
            continue
        s3[ind] = s2[ind]
        diff1 += 1
        z -= 1
        ind += 1

    # Step 4: Fill remaining positions with characters different from both s1 and s2
    ans = []
    for i in range(n):
        if s3[i] == '.':
            s3[i] = get_diff_character(i, s1, s2)
            diff1 += 1
            diff2 += 1
        ans.append(s3[i])

    # Step 5: Check if both diff1 and diff2 are equal to t
    if diff1 != t or diff2 != t:
        return -1
    else:
        return ''.join(ans)

if __name__ == "__main__":
    n, t = map(int, input().split())
    s1 = input().strip()
    s2 = input().strip()
    
    result = solve(n, t, s1, s2)
    print(result)
