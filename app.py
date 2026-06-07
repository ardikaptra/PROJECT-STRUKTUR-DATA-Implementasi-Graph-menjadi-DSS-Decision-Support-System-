import streamlit as st
import pandas as pd
import heapq

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="DSS Beach Club Bali",
    page_icon="🏖️",
    layout="wide"
)

# =====================================================
# DATA BEACH CLUB
# =====================================================

beach_clubs = {
    "Cafe Del Mar Bali": {
        "area": "Canggu",
        "price": 350000,
        "rating": 4.6
    },
    "Potato Head Beach Club": {
        "area": "Seminyak",
        "price": 400000,
        "rating": 4.8
    },
    "Atlas Beach Club": {
        "area": "Canggu",
        "price": 450000,
        "rating": 4.7
    },
    "Finns Beach Club": {
        "area": "Canggu",
        "price": 500000,
        "rating": 4.8
    },
    "Mari Beach Club": {
        "area": "Canggu",
        "price": 550000,
        "rating": 4.6
    },
    "La Brisa Bali": {
        "area": "Canggu",
        "price": 600000,
        "rating": 4.7
    },
    "Azul Beach Club": {
        "area": "Legian",
        "price": 650000,
        "rating": 4.5
    },
    "White Rock Beach Club": {
        "area": "Uluwatu",
        "price": 750000,
        "rating": 4.7
    },
    "Palmilla Bali": {
        "area": "Melasti",
        "price": 850000,
        "rating": 4.5
    },
    "Sundays Beach Club": {
        "area": "Uluwatu",
        "price": 1200000,
        "rating": 4.9
    }
}

# =====================================================
# GRAPH
# =====================================================

graph = {
    "User": {
        "Canggu": 5,
        "Seminyak": 8,
        "Legian": 10,
        "Melasti": 12,
        "Uluwatu": 15
    },

    "Canggu": {
        "Cafe Del Mar Bali": 2,
        "Atlas Beach Club": 3,
        "Finns Beach Club": 4,
        "Mari Beach Club": 5,
        "La Brisa Bali": 6
    },

    "Seminyak": {
        "Potato Head Beach Club": 2
    },

    "Legian": {
        "Azul Beach Club": 3
    },

    "Melasti": {
        "Palmilla Bali": 4
    },

    "Uluwatu": {
        "White Rock Beach Club": 3,
        "Sundays Beach Club": 2
    },

    "Cafe Del Mar Bali": {},
    "Atlas Beach Club": {},
    "Finns Beach Club": {},
    "Mari Beach Club": {},
    "La Brisa Bali": {},
    "Potato Head Beach Club": {},
    "Azul Beach Club": {},
    "Palmilla Bali": {},
    "White Rock Beach Club": {},
    "Sundays Beach Club": {}
}

# =====================================================
# DIJKSTRA
# =====================================================

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

# =====================================================
# HEADER
# =====================================================

st.title("🏖️ DSS Pemilihan Beach Club Terbaik di Bali")
st.caption("Decision Support System menggunakan Graph dan Algoritma Dijkstra")

# =====================================================
# DASHBOARD
# =====================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric("Beach Club", len(beach_clubs))
c2.metric("Area", len(set(x["area"] for x in beach_clubs.values())))
c3.metric("Budget Termurah", "Rp 350K")
c4.metric("Kelas Sultan", "Rp 1.2JT")

st.divider()

# =====================================================
# FILTER
# =====================================================

st.subheader("⚙️ Preferensi Pengguna")

col1, col2 = st.columns(2)

with col1:
    budget = st.slider(
        "Budget Maksimal (Rp)",
        300000,
        1500000,
        700000,
        50000
    )

with col2:
    min_rating = st.slider(
        "Minimum Rating",
        4.0,
        5.0,
        4.5,
        0.1
    )

# =====================================================
# DSS
# =====================================================

if st.button("🔍 Cari Rekomendasi", use_container_width=True):

    distances = dijkstra(graph, "User")

    candidates = []

    for club, data in beach_clubs.items():

        if (
            data["price"] <= budget and
            data["rating"] >= min_rating
        ):

            distance_score = distances[club]

            price_score = data["price"] / 100000

            rating_score = (5 - data["rating"]) * 10

            final_score = (
                distance_score * 0.4 +
                price_score * 0.3 +
                rating_score * 0.3
            )

            candidates.append({
                "Beach Club": club,
                "Area": data["area"],
                "Harga": data["price"],
                "Rating": data["rating"],
                "Bobot Dijkstra": distance_score,
                "Skor DSS": round(final_score, 2)
            })

    if candidates:

        df_result = pd.DataFrame(candidates)

        df_result = df_result.sort_values(
            by="Skor DSS",
            ascending=True
        )

        best = df_result.iloc[0]

        st.success(
            f"🏆 Rekomendasi Terbaik: {best['Beach Club']}"
        )

        st.dataframe(
            df_result,
            use_container_width=True
        )

    else:

        st.error(
            "Tidak ada beach club yang sesuai dengan kriteria."
        )

# =====================================================
# DATASET
# =====================================================

st.divider()

st.subheader("📋 Dataset Beach Club")

df = pd.DataFrame([
    {
        "Beach Club": club,
        "Area": data["area"],
        "Harga": data["price"],
        "Rating": data["rating"]
    }
    for club, data in beach_clubs.items()
])

st.dataframe(
    df,
    use_container_width=True
)

# =====================================================
# GRAPH
# =====================================================

st.divider()

st.subheader("🌐 Struktur Graph")

st.code("""
User
├── Canggu
│   ├── Cafe Del Mar Bali
│   ├── Atlas Beach Club
│   ├── Finns Beach Club
│   ├── Mari Beach Club
│   └── La Brisa Bali
│
├── Seminyak
│   └── Potato Head Beach Club
│
├── Legian
│   └── Azul Beach Club
│
├── Melasti
│   └── Palmilla Bali
│
└── Uluwatu
    ├── White Rock Beach Club
    └── Sundays Beach Club
""")

st.info(
    "Perankingan menggunakan kombinasi bobot Dijkstra, harga, dan rating untuk menghasilkan rekomendasi yang lebih realistis."
)
