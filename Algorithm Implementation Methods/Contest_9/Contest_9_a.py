def CopyCopyCopyCopyCopy(a):
    print(len(set(a)))


if __name__ == '__main__':
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        CopyCopyCopyCopyCopy(a)