"""def magicGrid(n):
    grid = [[0] * n for _ in range(n)]
    num = 0
    
    for i in range(0, n, 4):
        for j in range(0, n, 4):
            for x in range(4):
                for y in range(4):
                    grid[i + x][j + y] = num
                    num += 1
    
    for row in grid:
        print(" ".join(map(str, row)))


if __name__ == '__main__':
    n = int(input())
    magicGrid(n)"""



def magicGrid(n):
    input_matrix = [
        [8, 9, 1, 13],
        [3, 12, 7, 5],
        [0, 2, 4, 11],
        [6, 10, 15, 14]
    ]

    if n == 4:
        for row in input_matrix:
            print(' '.join(map(str, row)))
        return
    
    final = [[0] * n for _ in range(n)]
    
    block_size = 4
    
    for i in range(0, n, block_size):
        for j in range(0, n, block_size):
            block_offset = ((i // block_size) * (n // block_size) + (j // block_size)) * 16

            for x in range(block_size):
                for y in range(block_size):
                    final[i + x][j + y] = input_matrix[x][y] + block_offset
    
    for row in final:
        print(' '.join(map(str, row)))

if __name__ == '__main__':
    n = int(input())
    magicGrid(n)

