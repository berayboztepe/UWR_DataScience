from collections import defaultdict

def randomQuery(n, a):
    positions = defaultdict(list)
    for i, value in enumerate(a):
        positions[value].append(i + 1)

    total_probability = 0.0

    for indices in positions.values():
        indices = [0] + indices + [n + 1]
        no_occurrence_prob = 0.0

        for j in range(1, len(indices)):
            interval_length = indices[j] - indices[j - 1] - 1
            no_occurrence_prob += (interval_length * interval_length) / (n * n)

        prob_at_least_one = 1.0 - no_occurrence_prob
        total_probability += prob_at_least_one

    print(total_probability)


if __name__ == '__main__':
    n = int(input())
    a = list(map(int, input().split()))
    randomQuery(n, a)
