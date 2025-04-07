def tell_your_world(y_coordinates, n):
    for i in range(1, n):
        belongs_to_first_line = [False] * n

        for j in range(n):
            if i * (y_coordinates[j] - y_coordinates[0]) == j * (y_coordinates[i] - y_coordinates[0]):
                belongs_to_first_line[j] = True

        first_other_point = -1
        valid_partition = True

        for j in range(n):
            if not belongs_to_first_line[j]:
                if first_other_point == -1:
                    first_other_point = j
                elif i * (y_coordinates[j] - y_coordinates[first_other_point]) != (j - first_other_point) * (y_coordinates[i] - y_coordinates[0]):
                    valid_partition = False
                    break

        if valid_partition and first_other_point != -1:
            return True

    return False

def check_two_parallel_lines(y_coordinates, n):
    result = tell_your_world(y_coordinates, n) or tell_your_world(y_coordinates[::-1], n)

    print("Yes" if result else "No")


if __name__ == "__main__":
    n = int(input().strip())
    y_coordinates = list(map(int, input().strip().split()))
    check_two_parallel_lines(y_coordinates, n)
    
    
