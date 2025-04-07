def ohThesePalindroms(s):
    sorted_s = ''.join(sorted(s))
    print(sorted_s)


if __name__ == '__main__':
    n = int(input())
    s = input()
    ohThesePalindroms(s)