def compute_cost(modulo, prefix_sums, total_numbers):
    total_cost = 0
    for index in range(1, total_numbers + 1):
        remainder = prefix_sums[index] % modulo
        total_cost += min(remainder, modulo - remainder)
    return total_cost

def take_it_Alice(total_numbers, array_values):
    prefix_sums = [0] * (total_numbers + 1)
    for index in range(1, total_numbers + 1):
        prefix_sums[index] = prefix_sums[index - 1] + array_values[index - 1]

    if prefix_sums[total_numbers] == 1:
        print(-1)
        return

    minimum_cost = float('inf')
    total_sum = prefix_sums[total_numbers]
    divisor = 2

    while divisor * divisor <= total_sum:
        if total_sum % divisor == 0:
            minimum_cost = min(minimum_cost, compute_cost(divisor, prefix_sums, total_numbers))
            while total_sum % divisor == 0:
                total_sum //= divisor
        divisor += 1

    if total_sum > 1:
        minimum_cost = min(minimum_cost, compute_cost(total_sum, prefix_sums, total_numbers))

    print(minimum_cost)

if __name__ == "__main__":
    total_numbers = int(input().strip())
    array_values = list(map(int, input().strip().split()))
    take_it_Alice(total_numbers, array_values)
