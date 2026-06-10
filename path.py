import heapq

def shortest_path(graph, start, goal):

    queue = [(0, start, [])]

    visited = set()

    while queue:

        cost, node, path = heapq.heappop(queue)

        if node in visited:
            continue

        path = path + [node]

        if node == goal:
            return cost, path

        visited.add(node)

        for neighbor, weight in graph[node].items():
            heapq.heappush(
                queue,
                (cost + weight, neighbor, path)
            )

    return float("inf"), []
