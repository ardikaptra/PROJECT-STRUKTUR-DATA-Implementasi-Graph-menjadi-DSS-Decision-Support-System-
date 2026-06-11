# ==========================================================
# graph_builder.py
# DSS Beach Club Bali
# Struktur Data Graph - Adjacency List Weighted Graph
# ==========================================================

class Graph:
    """
    Weighted Graph menggunakan representasi
    Adjacency List.

    Format:

    {
        "A": {
            "B": 5,
            "C": 10
        }
    }
    """

    def __init__(self):
        self.graph = {}

    # ======================================================
    # NODE OPERATION
    # ======================================================

    def add_node(self, node):
        """
        Menambahkan node baru
        """

        if node not in self.graph:
            self.graph[node] = {}

    def remove_node(self, node):
        """
        Menghapus node dan semua edge terkait
        """

        if node in self.graph:

            self.graph.pop(node)

            for source in self.graph:
                if node in self.graph[source]:
                    self.graph[source].pop(node)

    # ======================================================
    # EDGE OPERATION
    # ======================================================

    def add_edge(
        self,
        source,
        destination,
        weight,
        bidirectional=True
    ):
        """
        Menambahkan edge berbobot
        """

        self.add_node(source)
        self.add_node(destination)

        self.graph[source][destination] = weight

        if bidirectional:
            self.graph[destination][source] = weight

    def remove_edge(
        self,
        source,
        destination,
        bidirectional=True
    ):

        if source in self.graph:

            if destination in self.graph[source]:

                self.graph[source].pop(destination)

        if bidirectional:

            if destination in self.graph:

                if source in self.graph[destination]:

                    self.graph[destination].pop(source)

    # ======================================================
    # GETTERS
    # ======================================================

    def get_nodes(self):

        return list(self.graph.keys())

    def get_neighbors(self, node):

        if node in self.graph:
            return self.graph[node]

        return {}

    def get_edges(self):
        """
        Menghasilkan list edge
        """

        edges = []

        visited = set()

        for source in self.graph:

            for destination, weight in self.graph[source].items():

                edge_id = tuple(
                    sorted([source, destination])
                )

                if edge_id not in visited:

                    visited.add(edge_id)

                    edges.append(
                        (
                            source,
                            destination,
                            weight
                        )
                    )

        return edges

    # ======================================================
    # VISUALIZATION DATA
    # ======================================================

    def adjacency_list(self):
        """
        Representasi graph
        untuk laporan UAS
        """

        return self.graph

    def adjacency_matrix(self):

        nodes = self.get_nodes()

        matrix = []

        for source in nodes:

            row = []

            for destination in nodes:

                if destination in self.graph[source]:

                    row.append(
                        self.graph[source][destination]
                    )

                else:

                    row.append(0)

            matrix.append(row)

        return nodes, matrix

    # ======================================================
    # INFORMATION
    # ======================================================

    def total_nodes(self):

        return len(self.graph)

    def total_edges(self):

        return len(self.get_edges())

    def __str__(self):

        output = ""

        for node in self.graph:

            output += f"{node} -> {self.graph[node]}\n"

        return output
