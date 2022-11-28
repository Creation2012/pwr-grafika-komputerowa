parent = []

def find(i):
    while parent[i] != i:
        i = parent[i]

    return i

def union(i,j):
    a = find(i)
    b = find(j)
    parent[a] = b

def kruskalMST(cost, s):
    global parent
    parent = [i for i in range(s)]
    mincost = 0

    path = list()

    for i in range(s):
        parent[i] = i

    edge_count = 0

    while edge_count < s - 1:
        mini = 101 
        a = -1
        b = -1
        for i in range(s):
            for j in range(s):
                if find(i) != find(j) and cost[i][j] < mini and cost[i][j] != 0:
                    mini = cost[i][j]
                    a = i
                    b = j

        union(a,b)
        path.append((a,b))
        edge_count += 1
        mincost += mini


    return path
