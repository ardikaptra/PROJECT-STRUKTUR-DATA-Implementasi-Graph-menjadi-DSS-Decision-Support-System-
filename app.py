import streamlit as st
import heapq

st.set_page_config(
    page_title="DSS Beach Club Bali",
    page_icon="🏖️",
    layout="centered"
)

graph = {
    "User": {
        "Canggu": 5,
        "Seminyak": 8,
        "Uluwatu": 15
    },

    "Canggu": {
        "Finns Beach Club": 2,
        "Atlas Beach Club": 3,
        "Cafe Del Mar Bali": 4
    },

    "Seminyak": {
        "Potato Head Beach Club": 2
    },

    "Uluwatu": {
        "Sundays Beach Club": 2
    },

    "Finns Beach Club": {},
    "Atlas Beach Club": {},
    "Cafe Del Mar Bali": {},
    "Potato Head Beach Club": {},
    "Sundays Beach Club": {}
}


def dijkstra(graph, start):
    distances = {node: float("inf") for node in graph}
    distances[start] = 0

    pq = [(0, start)]

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        for neighbor, weight in graph[current_node].items():

            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance

                heapq.heappush(
                    pq,
                    (distance, neighbor)
                )

    return distances


st.title("🏖️ DSS Pemilihan Beach Club Terbaik di Bali")

st.write(
    """
Sistem ini menggunakan:
- Weighted Graph
- Adjacency List
- Algoritma Dijkstra

untuk memberikan rekomendasi beach club terbaik.
"""
)

budget = st.slider(
    "Budget Maksimal (Rp)",
    200000,
    1000000,
    500000,
    50000
)

if st.button("Cari Rekomendasi"):

    result = dijkstra(graph, "User")

    beach_clubs = [
        "Finns Beach Club",
        "Atlas Beach Club",
        "Cafe Del Mar Bali",
        "Potato Head Beach Club",
        "Sundays Beach Club"
    ]

    ranking = []

    for club in beach_clubs:
        ranking.append(
            (club, result[club])
        )

    ranking.sort(key=lambda x: x[1])

    st.subheader("Hasil Rekomendasi")

    for i, (club, score) in enumerate(ranking, start=1):

        st.write(
            f"{i}. {club} | Total Bobot: {score}"
        )

    st.success(
        f"Rekomendasi Terbaik: {ranking[0][0]}"
    )

st.divider()

st.subheader("Struktur Graph")

st.code("""
User
├── Canggu
│   ├── Finns Beach Club
│   ├── Atlas Beach Club
│   └── Cafe Del Mar Bali
│
├── Seminyak
│   └── Potato Head Beach Club
│
└── Uluwatu
    └── Sundays Beach Club
""")
