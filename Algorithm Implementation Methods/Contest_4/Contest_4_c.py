class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.special_count = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
                self.special_count[rootX] += self.special_count[rootY]
            elif self.rank[rootX] < self.rank[rootY]:
                self.parent[rootX] = rootY
                self.special_count[rootY] += self.special_count[rootX]
            else:
                self.parent[rootY] = rootX
                self.rank[rootX] += 1
                self.special_count[rootX] += self.special_count[rootY]
            return True
        return False

def main(n, m, k, special_vertices):
    dsu = DSU(n)
    for sv in special_vertices:
        dsu.special_count[sv] = 1

    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((w, u - 1, v - 1))

    edges.sort()

    max_edge_weight = 0

    for weight, u, v in edges:
        if dsu.union(u, v):
            max_edge_weight = weight
            root = dsu.find(u)
            if dsu.special_count[root] == k:
                break

    result = [max_edge_weight] * k
    print(" ".join(map(str, result)))


if __name__ == '__main__':
    n, m, k = map(int, input().split())
    special_vertices = list(map(lambda x: int(x) - 1, input().split()))
    main(n, m, k, special_vertices)
