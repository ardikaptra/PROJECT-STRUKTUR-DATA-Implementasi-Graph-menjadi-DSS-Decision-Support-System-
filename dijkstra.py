import heapq
import pandas as pd

class BaliBeachClubGraph:
    def __init__(self):
        self.adjacency_list = {}
        self.node_metadata = {}

    def add_node(self, node_name: str, metadata: dict = None):
        if node_name not in self.adjacency_list:
            self.adjacency_list[node_name] = []
        self.node_metadata[node_name] = metadata or {}

    def add_edge(self, source: str, destination: str, weight: float):
        self.add_node(source)
        self.add_node(destination)
        self.adjacency_list[source].append((destination, weight))

    def get_adjacency_matrix(self) -> pd.DataFrame:
        nodes = sorted(list(self.adjacency_list.keys()))
        matrix = {node: {target: 0 for target in nodes} for node in nodes}
        for source, edges in self.adjacency_list.items():
            for destination, weight in edges:
                if destination in matrix[source]:
                    matrix[source][destination] = weight
        return pd.DataFrame.from_dict(matrix, orient='index')

    def compute_dijkstra(self, start_node: str, end_node: str):
        if start_node not in self.adjacency_list or end_node not in self.adjacency_list:
            return [], float('inf'), {}
        distances = {node: float('inf') for node in self.adjacency_list}
        distances[start_node] = 0
        previous_nodes = {node: None for node in self.adjacency_list}
        priority_queue = [(0, start_node)]
        calculation_log = {} 

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            calculation_log[current_node] = current_distance
            if current_node == end_node:
                break
            if current_distance > distances[current_node]:
                continue
            for neighbor, weight in self.adjacency_list.get(current_node, []):
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        current = end_node
        while current is not None:
            path.insert(0, current)
            current = previous_nodes[current]
        return (path if distances[end_node] != float('inf') else [], distances[end_node], calculation_log)

    def compute_degree_centrality(self) -> dict:
        centrality = {node: 0 for node in self.adjacency_list}
        for source, edges in self.adjacency_list.items():
            centrality[source] += len(edges)  
            for destination, _ in edges:
                if destination in centrality:
                    centrality[destination] += 1  
        return centrality
