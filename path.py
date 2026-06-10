import heapq

def shortest_path(graph,start,goal):

    queue = [(0,start,[start])]

    visited = set()

    while queue:

        cost,node,path = heapq.heappop(queue)

        if node == goal:
            return cost,path

        if node in visited:
            continue

        visited.add(node)

        for neighbor,weight in graph[node].items():

            heapq.heappush(
                queue,
                (
                    cost + weight,
                    neighbor,
                    path + [neighbor]
                )
            )

    return None,None
