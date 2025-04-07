def x_axis(xs):
    xs.sort()
    a = xs[1]
    result = abs(xs[0] - a) + abs(xs[1] - a) + abs(xs[2] - a)
    print(result)

if __name__ == "__main__":
    t = int(input())
    for i in range(t):
        xs = list(map(int, input().split()))
        x_axis(xs)
