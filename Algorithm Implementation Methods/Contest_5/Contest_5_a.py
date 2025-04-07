def main(s):
    s = list(s)
    n = len(s)
    
    for i in range(1, n):
        if s[i] == s[i - 1]:
            for replacement in 'abc':
                if replacement != s[i - 1] and (i + 1 == n or replacement != s[i + 1]):
                    s[i] = replacement
                    break
    
    print("".join(s))

if __name__ == '__main__':
    s = input().strip()
    main(s)
