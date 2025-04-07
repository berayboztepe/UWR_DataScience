n, m = map(int, input().split())
costs = list(map(int, input().split()))

graph = [[] for _ in range(n)]

# Read friendships and build the graph
for _ in range(m):
    x, y = map(int, input().split())
    graph[x-1].append(y-1)
    graph[y-1].append(x-1)

# Visited array to keep track of visited nodes (characters)
visited = [False] * n

# Total cost to spread the rumor
total_cost = 0

# DFS to find the minimum cost in each connected component
def dfs(node):
    stack = [node]
    min_cost = costs[node]
    visited[node] = True
    
    while stack:
        current = stack.pop()
        for neighbor in graph[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)
                min_cost = min(min_cost, costs[neighbor])
    
    return min_cost

# Iterate over all characters and calculate the minimum cost per component
for i in range(n):
    if not visited[i]:
        total_cost += dfs(i)

# Output the total minimum cost
print(total_cost)
