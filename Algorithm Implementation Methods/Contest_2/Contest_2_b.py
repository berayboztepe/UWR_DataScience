n, a, b, k = map(int, input().split())
h = list(map(int, input().split()))

# Process each monster's health
for i in range(n):
    h[i] %= a + b  # Modulo to determine remaining health after a full round of your and opponent's attacks
    if h[i] == 0:
        h[i] += a + b  # If monster's health is a multiple of (a + b), adjust to account for full round
    h[i] = ((h[i] + a - 1) // a) - 1  # Calculate how many extra hits you need after initial attack


h.sort()
ans = 0

for i in range(n):
    if k - h[i] < 0:
        break  # Stop if you can't use any more skips
    ans += 1
    k -= h[i]  # Decrease available skips by the skips used for this monster

print(ans)
