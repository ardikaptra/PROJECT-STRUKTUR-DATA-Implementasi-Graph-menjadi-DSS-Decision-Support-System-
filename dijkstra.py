# ==========================================================
# dijkstra.py
# DSS Beach Club Bali
# Algoritma Dijkstra dengan Tracking Langkah
# ==========================================================

import heapq


class Dijkstra:

    def __init__(self, graph):
        """
        graph format:

        {
            "A": {
                "B": 5,
                "C": 10
            }
        }
        """

        self.graph = graph

    # ======================================================
    # SHORTEST PATH
    # ======================================================

    def shortest_path(
        self,
        start,
        target
    ):
        """
        Mengembalikan:

        path
        total_cost
        steps
        """

        distances = {
            node: float("inf")
            for node in self.graph
        }

        previous = {
            node: None
            for node in self.graph
        }

        distances[start] = 0

        pq = [(0, start)]

        visited = set()

        steps = []

        while pq:

            current_distance, current_node = heapq.heappop(pq)

            if current_node in visited:
                continue

            visited.add(current_node)

            # ==========================================
            # SIMPAN LANGKAH
            # ==========================================

            steps.append({
                "current_node": current_node,
                "current_distance": current_distance,
                "visited": list(visited),
                "priority_queue": pq.copy(),
                "distances": distances.copy()
            })

            # ==========================================
            # TARGET DITEMUKAN
            # ==========================================

            if current_node == target:
                break

            # ==========================================
            # EKSPLORASI TETANGGA
            # ==========================================

            for neighbor, weight in self.graph[current_node].items():

                new_distance = (
                    current_distance + weight
                )

                if new_distance < distances[neighbor]:

                    distances[neighbor] = new_distance

                    previous[neighbor] = current_node

                    heapq.heappush(
                        pq,
                        (
                            new_distance,
                            neighbor
                        )
                    )

        # ==============================================
        # REKONSTRUKSI PATH
        # ==============================================

        path = []

        current = target

        while current is not None:

            path.append(current)

            current = previous[current]

        path.reverse()

        # ==============================================
        # CEK PATH VALID
        # ==============================================

        if path[0] != start:

            return {
                "path": [],
                "cost": float("inf"),
                "steps": steps
            }

        return {
            "path": path,
            "cost": distances[target],
            "steps": steps
        }

    # ======================================================
    # SEMUA JARAK
    # ======================================================

    def all_distances(self, start):

        distances = {
            node: float("inf")
            for node in self.graph
        }

        distances[start] = 0

        pq = [(0, start)]

        while pq:

            current_distance, current_node = heapq.heappop(pq)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node].items():

                new_distance = (
                    current_distance + weight
                )

                if new_distance < distances[neighbor]:

                    distances[neighbor] = new_distance

                    heapq.heappush(
                        pq,
                        (
                            new_distance,
                            neighbor
                        )
                    )

        return distances
