def hamming_distance_sum(a, b):

    n, m = len(a), len(b)
    prefix_zeros = [0] * (m + 1)
    prefix_ones = [0] * (m + 1)
    
    for i in range(m):
        prefix_zeros[i + 1] = prefix_zeros[i] + (1 if b[i] == '0' else 0)
        prefix_ones[i + 1] = prefix_ones[i] + (1 if b[i] == '1' else 0)
    
    total_hamming_distance = 0
    
    for i in range(n):
        if a[i] == '0':
            total_hamming_distance += prefix_ones[m - n + i + 1] - prefix_ones[i]
        else:
            total_hamming_distance += prefix_zeros[m - n + i + 1] - prefix_zeros[i]
    
    print(total_hamming_distance)


if __name__ == '__main__':
    first = input().strip()
    second = input().strip()
    hamming_distance_sum(first, second)
