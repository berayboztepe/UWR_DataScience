def IceSkating(coordinates, n):
    graph = [[] for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            if coordinates[i][0] == coordinates[j][0] or coordinates[i][1] == coordinates[j][1]:
                graph[i].append(j)
                graph[j].append(i)
    
    visited = [False] * n
    components = 0

    def bfs(start):
        queue = [start]
        while queue:
            current = queue.pop(0)
            for neighbor in graph[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)

    for i in range(n):
        if not visited[i]:
            components += 1
            visited[i] = True
            bfs(i)
    
    return components - 1

if __name__ == '__main__':
    n = int(input())
    coordinates = []
    for _ in range(n):
        x_i, y_i = map(int, input().split())
        coordinates.append((x_i, y_i))
    print(IceSkating(coordinates, n))
