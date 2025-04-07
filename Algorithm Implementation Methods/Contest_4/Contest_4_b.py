class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.size[rootX] < self.size[rootY]:
                rootX, rootY = rootY, rootX
            self.parent[rootY] = rootX
            self.size[rootX] += self.size[rootY]

    def component_size(self, x):
        root = self.find(x)
        return self.size[root]


def main(n, m):
    dsu = DSU(n)
    for _ in range(m):
        group = list(map(int, input().split()))[1:]
        for i in range(1, len(group)):
            dsu.union(group[0] - 1, group[i] - 1)

    print(" ".join(str(dsu.component_size(i)) for i in range(n)))


if __name__ == '__main__':
    n, m = map(int, input().split())
    main(n, m)