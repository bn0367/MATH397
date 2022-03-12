n = 5
grid = [0 for _ in range(n * n)]
neighbors = lambda x: [x - 1, x + 1, x - n, x + n, x - n - 1, x - n + 1, x + n - 1, x + n + 1]

DI = lambda e, x: 2 * x - sum(grid[i] for i in neighbors(x) if i >= 0 and i < len(grid) and i != e) <= 0

DO = lambda e, x: 