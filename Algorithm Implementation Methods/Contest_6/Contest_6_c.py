from collections import deque

SYMBOLS = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890"
MAX_SIZE = 111

board_grid = [["" for _ in range(MAX_SIZE)] for _ in range(MAX_SIZE)]
result_grid = [["" for _ in range(MAX_SIZE)] for _ in range(MAX_SIZE)]

def process(rows, cols, chickens):
    global board_grid, result_grid

    for row in range(1, rows + 1):
        line = input().strip()
        for col in range(1, cols + 1):
            board_grid[row][col] = line[col - 1]

    traverse_left_to_right = True
    cell_positions = []

    for row in range(1, rows + 1):
        if traverse_left_to_right:
            for col in range(1, cols + 1):
                cell_positions.append((row, col))
        else:
            for col in range(cols, 0, -1):
                cell_positions.append((row, col))
        traverse_left_to_right = not traverse_left_to_right

    total_rice = sum(1 for row in range(1, rows + 1) for col in range(1, cols + 1) if board_grid[row][col] == 'R')
    average_rice = total_rice // chickens
    additional_rice = 1 if total_rice % chickens != 0 else 0

    cell_positions = deque(cell_positions)

    for chicken_index in range(chickens):
        rice_count = 0
        while True:
            current_row, current_col = cell_positions.popleft()
            result_grid[current_row][current_col] = SYMBOLS[chicken_index]
            if board_grid[current_row][current_col] == 'R':
                total_rice -= 1
                rice_count += 1

            if rice_count < average_rice:
                continue
            if average_rice * (chickens - chicken_index - 1) <= total_rice <= (average_rice + additional_rice) * (chickens - chicken_index - 1):
                break

    while cell_positions:
        current_row, current_col = cell_positions.popleft()
        result_grid[current_row][current_col] = SYMBOLS[chickens - 1]

    for row in range(1, rows + 1):
        print(''.join(result_grid[row][1:cols + 1]))

if __name__ == "__main__":
    test_cases = int(input())
    for _ in range(test_cases):
        rows, cols, chickens = map(int, input().split())
        process(rows, cols, chickens)