def ChangeVolume(a, b):
    diff = abs(b - a)
    
    presses = 0
    for step in [5, 2, 1]:
        presses += diff // step
        diff %= step
    
    print(presses)

if __name__ == '__main__':
    T = int(input())
    for i in range(T):
        a, b = map(int, input().split())
        ChangeVolume(a, b)