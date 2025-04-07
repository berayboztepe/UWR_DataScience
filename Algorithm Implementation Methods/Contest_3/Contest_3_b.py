"""def main(stations, aj, bj):
    if not aj in stations or not bj in stations:
        return "NO"
    
    indices_aj = [i for i, x in enumerate(stations) if x == aj]

    for index in indices_aj:
        try:
            next_index_bj = stations.index(bj, index)
            if index < next_index_bj:
                return "YES"
        except ValueError:
            return "NO"

    return "NO"


if __name__ == "__main__":
    t = int(input())

    for i in range(t):
        _ = input()
        n, k = list(map(int, input().split()))
        stations = list(map(int, input().split()))
        for j in range(k):
            aj, bj = list(map(int, input().split()))
            ans = main(stations, aj, bj)
            print(ans)"""

"""def main(stations, aj, bj):
    first_aj = -1
    first_bj_after_aj = -1
    
    for i in range(len(stations)):
        if stations[i] == aj:
            first_aj = i
            break
    
    if first_aj == -1:
        return "NO"
    
    for i in range(first_aj, len(stations)):
        if stations[i] == bj:
            first_bj_after_aj = i
            break
    
    if first_bj_after_aj != -1:
        return "YES"
    else:
        return "NO"


if __name__ == "__main__":
    t = int(input())

    for i in range(t):
        _ = input()
        n, k = list(map(int, input().split()))
        stations = list(map(int, input().split()))
        for j in range(k):
            aj, bj = list(map(int, input().split()))
            ans = main(stations, aj, bj)
            print(ans)"""

"""def preprocess(stations):
    first_occurrence = {}
    last_occurrence = {}

    for i, station in enumerate(stations):
        if station not in first_occurrence:
            first_occurrence[station] = i
        last_occurrence[station] = i

    return first_occurrence, last_occurrence


def answer_query(first_occurrence, last_occurrence, aj, bj):
    if aj in first_occurrence and bj in last_occurrence:
        if first_occurrence[aj] <= last_occurrence[bj]:
            return "YES"
    return "NO"


if __name__ == "__main__":
    t = int(input())

    for _ in range(t):
        input()
        n, k = map(int, input().split())
        stations = list(map(int, input().split()))

        first_occurrence, last_occurrence = preprocess(stations)

        for _ in range(k):
            aj, bj = map(int, input().split())
            ans = answer_query(first_occurrence, last_occurrence, aj, bj)
            print(ans)"""


def main(stations, aj, bj):
    m = dict()
    for i in range(len(stations)):
        if stations[i] not in m:
            m[stations[i]] = [i, i]
        else:
            m[stations[i]][1] = i

    if aj not in m or bj not in m or m[aj][0] > m[bj][1]:
        print("NO")
    else:
        print("YES")

if __name__ == "__main__":
    t = int(input())

    for i in range(t):
        _ = input()
        n, k = list(map(int, input().split()))
        stations = list(map(int, input().split()))
        for j in range(k):
            aj, bj = list(map(int, input().split()))
            main(stations, aj, bj)