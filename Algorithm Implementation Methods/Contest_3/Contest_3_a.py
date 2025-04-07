def main(word):
    letters = set()
    count = 0

    for i in word:
        letters.add(i)

        if len(letters) == 4:
            count += 1
            letters = {i}

    if len(letters) != 0:
        count += 1

    return count

if __name__ == "__main__":
    n = int(input())
    for i in range(n):
        word = input()
        ans = main(word)
        print(ans)