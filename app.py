import streamlit as st
import pandas as pd
from dijkstra import BaliBeachClubGraph
from dataset import BEACH_CLUB_DATASET, GRAPH_EDGES
from streamlit_js_eval import get_geolocation

st.set_page_config(
    page_title="Bali Beach Club DSS Engine",
    page_icon="🏖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "dataset_club" not in st.session_state:
    st.session_state.dataset_club = BEACH_CLUB_DATASET.copy()

    st.session_state.dataset_club["Main Highway Hub"] = {
        "wilayah": "Infrastruktur Transit", "rating": 5.0, "min_spend": 0, "lat": -8.7471, "lon": 115.1954
    }
    st.session_state.dataset_club["Sanur Port Hub"] = {
        "wilayah": "Infrastruktur Transit", "rating": 5.0, "min_spend": 0, "lat": -8.6743, "lon": 115.2631
    }

if "graph_edges" not in st.session_state:
    st.session_state.graph_edges = GRAPH_EDGES.copy()

loc = get_geolocation()
user_node_name = "Posisi Riil Saya (GPS)"

user_lat = float(loc['coords']['latitude']) if loc else -8.7224
user_lon = float(loc['coords']['longitude']) if loc else 115.1771

st.session_state.dataset_club[user_node_name] = {
    "wilayah": "Lokasi Pasif User", 
    "rating": 5.0, 
    "min_spend": 0,
    "lat": float(user_lat),
    "lon": float(user_lon)
}

static_user_edges = [
    (user_node_name, "Main Highway Hub", 20),
    (user_node_name, "Potato Head Beach Club", 25),
    (user_node_name, "Finns Beach Club", 30),
    (user_node_name, "Savaya Bali", 35)
]

st.session_state.graph_edges = [edge for edge in st.session_state.graph_edges if edge[0] != user_node_name]
st.session_state.graph_edges.extend(static_user_edges)


def rebuild_graph():
    engine = BaliBeachClubGraph()
    for club_name, meta in st.session_state.dataset_club.items():
        engine.add_node(club_name, meta)
    
    for src, dest, w in st.session_state.graph_edges:
        engine.add_edge(src, dest, float(w))
    return engine

graph_system = rebuild_graph()

st.sidebar.title("💎 Bali Beach Club DSS")
if loc:
    st.sidebar.success(f"🛰️ GPS Riil Aktif!\nLat: {user_lat:.4f}\nLon: {user_lon:.4f}")
else:
    st.sidebar.warning("🛰️ Menggunakan koordinat default lokal.")

app_mode = st.sidebar.radio("Pilih Modul Sistem:", [
    "📋 Rekomendasi & Filter DSS", 
    "➕ Kelola Graf (Input Data)", 
    "⚡ Optimasi Rute (Dijkstra Engine)", 
    "📊 Inspeksi Struktur Data Graph"
])

if app_mode == "📋 Rekomendasi & Filter DSS":
    st.title("🏛️ Modul Pengambil Keputusan Alternatif Wisata")
    st.subheader("Menentukan rekomendasi Beach Club terbaik berdasarkan kriteria Anda")
    st.markdown("---")
    
    search_query = st.text_input("🔍 Cari Beach Club spesifik berdasarkan nama:", "")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        wilayah_options = ["Semua Wilayah"] + list(set(d["wilayah"] for d in st.session_state.dataset_club.values() if d["wilayah"] not in ["Lokasi Pasif User", "Infrastruktur Transit"]))
        selected_zone = st.selectbox("Batasan Wilayah Geografis:", wilayah_options)
    with c2:
        max_spend = st.slider("Maksimal Budget Minimum Spend (IDR):", 150000, 1500000, 1000000, step=50000)
    with c3:
        min_rating = st.slider("Peringkat Rating Minimum (Skala 5.0):", 4.0, 5.0, 4.4, step=0.1)

    filtered_res = []
    map_plots = []
    map_plots.append({"lat": float(user_lat), "lon": float(user_lon), "name": "Lokasi Saya"})

    for name, data in st.session_state.dataset_club.items():
        if name == user_node_name or data.get("wilayah") == "Infrastruktur Transit":
            continue
        if search_query and search_query.lower() not in name.lower():
            continue
        if selected_zone != "Semua Wilayah" and data.get("wilayah") != selected_zone:
            continue
        if data.get("min_spend", 0) > max_spend:
            continue
        if data.get("rating", 0.0) < min_rating:
            continue
        
        filtered_res.append((name, data))
        
        if data.get("lat") is not None and data.get("lon") is not None:
            map_plots.append({
                "lat": float(data["lat"]), 
                "lon": float(data["lon"]), 
                "name": name
            })

    col_map, col_table = st.columns([1, 1])
    
    with col_map:
        st.markdown("### 🗺️ Visualisasi Peta Destinasi Terfilter")
        if map_plots:
            df_map = pd.DataFrame(map_plots)
            df_map["lat"] = df_map["lat"].astype(float)
            df_map["lon"] = df_map["lon"].astype(float)
            st.map(df_map, size=50, color="#FF4B4B", use_container_width=True)
        else:
            st.warning("Tidak ada koordinat yang dapat ditampilkan di peta.")

    with col_table:
        st.markdown("### 🎯 Hasil Evaluasi Rekomendasi")
        if filtered_res:
            table_data = [{"Nama Beach Club": n, "Wilayah": d.get("wilayah", "Unknown"), "Rating": f"⭐ {d.get('rating', 0.0)}", "Minimum Spend": f"Rp {d.get('min_spend', 0):,}"} for n, d in filtered_res]
            st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
 
            st.markdown("#### 🤖 Rekomendasi Pintar AI (Custom Preference):")
            pref = st.radio("Apa prioritas utama Anda hari ini?", ["Seimbang (Value)", "Mengutamakan Rating Tinggi", "Mengutamakan Budget Hemat"], horizontal=True)
            
            if pref == "Mengutamakan Rating Tinggi":
                best_value_club = min(filtered_res, key=lambda x: (x[1].get("min_spend", 0) / (x[1].get("rating", 1) ** 4)))
            elif pref == "Mengutamakan Budget Hemat":
                best_value_club = min(filtered_res, key=lambda x: x[1].get("min_spend", 0))
            else:
                best_value_club = min(filtered_res, key=lambda x: (x[1].get("min_spend", 0) / (x[1].get("rating", 1) ** 2)))
                
            st.info(f"💡 **Rekomendasi Berbasis Preferensi:** Berdasarkan kriteria Anda, tempat terbaik yang disarankan adalah **{best_value_club[0]}** di daerah **{best_value_club[1].get('wilayah', 'Unknown')}**.")
        else:
            st.warning("⚠️ Tidak ada alternatif entitas tempat yang memenuhi seluruh kriteria filter Anda.")

elif app_mode == "➕ Kelola Graf (Input Data)":
    st.title("⚙️ Modul Input Data Struktur Graph")
    st.subheader("Kelola Node (Simpul Tempat) dan Edge (Jalan Penghubung) secara dinamis")
    st.markdown("---")
    t1, t2 = st.tabs(["🆕 Input Node Baru (Tempat)", "🔗 Input Edge Baru (Jalan/Rute)"])
    
    with t1:
        st.markdown("### Tambah Simpul Destinasi Baru")
        n_name = st.text_input("Nama Node / Tempat Baru:", placeholder="Contoh: New Beach Club Bali")
        n_zone = st.text_input("Wilayah / Lokasi Geografis:", placeholder="Contoh: Kuta")
        
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            n_rating = st.number_input("Rating Tempat (Skala 0.0 - 5.0):", 0.0, 5.0, 4.5, step=0.1)
            n_lat = st.number_input("Koordinat Garis Lintang (Latitude):", value=-8.7224, format="%.6f")
        with col_n2:
            n_spend = st.number_input("Minimum Spend Masuk (IDR):", min_value=0, value=250000, step=50000)
            n_lon = st.number_input("Koordinat Garis Bujur (Longitude):", value=115.1771, format="%.6f")
            
        if st.button("Simpan Node Baru ke Graf 📥", type="primary"):
            if not n_name.strip() or not n_zone.strip():
                st.error("Nama tempat dan wilayah tidak boleh kosong!")
            elif n_name in st.session_state.dataset_club:
                st.warning(f"Tempat dengan nama '{n_name}' sudah terdaftar dalam database.")
            else:
                st.session_state.dataset_club[n_name] = {
                    "wilayah": n_zone.strip(), 
                    "rating": float(n_rating), 
                    "min_spend": int(n_spend), 
                    "lat": float(n_lat), 
                    "lon": float(n_lon)
                }
                st.success(f"🎉 Sukses! Node '{n_name}' berhasil disimpan ke dalam struktur graf.")
                st.rerun()

    with t2:
        st.markdown("### Hubungkan Dua Simpul dengan Jalan Baru")
        nodes_list = sorted(list(st.session_state.dataset_club.keys()))
        
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            src = st.selectbox("Pilih Simpul Asal (Source Vertex):", nodes_list, key="src_select")
        with col_e2:
            dst = st.selectbox("Pilih Simpul Tujuan (Destination Vertex):", nodes_list, key="dst_select")
            
        w_time = st.number_input("Bobot Waktu Tempuh Perjalanan (Menit):", 1, 180, 15)
        
        if st.button("Hubungkan Jalur Edge Baru 🔗", type="primary"):
            if src == dst:
                st.error("Gagal! Simpul asal dan simpul tujuan tidak boleh sama.")
            else:
                duplicate = any(edge[0] == src and edge[1] == dst for edge in st.session_state.graph_edges)
                if duplicate:
                    st.warning(f"Jalur dari '{src}' menuju '{dst}' sudah ada sebelumnya.")
                else:
                    st.session_state.graph_edges.append((src, dst, float(w_time)))
                    st.success(f"🔗 Sukses menyambungkan jalan: {src} ➔ {dst} ({w_time} Menit)")
                    st.rerun()

elif app_mode == "⚡ Optimasi Rute (Dijkstra Engine)":
    st.title("🗺️ Modul Optimasi Pencarian Jalur Terpendek")
    st.subheader("Menghitung rute dengan bobot waktu perjalanan paling efisien via Algoritma Dijkstra")
    st.markdown("---")
    
    all_nodes = sorted(list(graph_system.adjacency_list.keys()))
    col_s, col_e = st.columns(2)
    with col_s:
        default_idx = all_nodes.index(user_node_name) if user_node_name in all_nodes else 0
        start_pt = st.selectbox("Titik Berangkat Asal (Mengunci GPS):", all_nodes, index=default_idx)
    with col_e:
        default_target = all_nodes.index("Savaya Bali") if "Savaya Bali" in all_nodes else 0
        end_pt = st.selectbox("Titik Tujuan Akhir:", all_nodes, index=default_target)

    if st.button("Hitung Rute Lintasan Terbaik ⚡", type="primary"):
        if start_pt == end_pt:
            st.error("Node asal dan tujuan tidak boleh bernilai sama!")
        else:
            path, total_w, log_calc = graph_system.compute_dijkstra(start_pt, end_pt)
            
            if total_w == float('inf') or len(path) == 0:
                st.error("❌ Rute tidak ditemukan! Sambungkan simpul jalan ini di menu Kelola Graf.")
            else:
                st.success("✅ Rute Sukses Dioptimalkan Berdasarkan Jaringan Graf!")
                
                m1, m2 = st.columns(2)
                m1.metric("Total Waktu Perjalanan Efektif", f"{total_w} Menit")
                m2.metric("Jumlah Titik Simpang Dilewati", f"{len(path)} Titik")
                
                path_plots = []
                for node in path:
                    node_meta = st.session_state.dataset_club.get(node)
                    if node_meta and node_meta.get("lat") is not None and node_meta.get("lon") is not None:
                        path_plots.append({
                            "lat": float(node_meta["lat"]), 
                            "lon": float(node_meta["lon"]), 
                            "name": node
                        })
                    else:
                        path_plots.append({
                            "lat": -8.7224, 
                            "lon": 115.1771, 
                            "name": f"{node} (Default Position)"
                        })
                
                st.markdown("### 📍 Peta Lintasan Rute Optimum")
                if path_plots:
                    df_path_map = pd.DataFrame(path_plots)
                    df_path_map["lat"] = df_path_map["lat"].astype(float)
                    df_path_map["lon"] = df_path_map["lon"].astype(float)
                    st.map(df_path_map, size=65, color="#0000FF", use_container_width=True)
                else:
                    st.warning("Gagal memproses titik koordinat lintasan rute.")

                st.markdown("### 🔀 Alur Urutan Lintasan:")
                st.info(" ➔ ".join([f"`{node}`" for node in path]))

                rute_summary = []
                for i, p_node in enumerate(path):
                    meta = st.session_state.dataset_club.get(p_node, {})
                    rute_summary.append({
                        "Urutan": i + 1,
                        "Nama Titik Jaringan": p_node,
                        "Wilayah Geografis": meta.get("wilayah", "Transit Hub"),
                        "Rating Destinasi": meta.get("rating", "-")
                    })
                df_download = pd.DataFrame(rute_summary)
                csv_data = df_download.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Unduh Laporan Rute (.CSV)",
                    data=csv_data,
                    file_name=f"Rute_DSS_{start_pt}_ke_{end_pt}.csv",
                    mime="text/csv",
                )

                with st.expander("Bongkar Langkah Per-Node", expanded=True):
                    for i in range(len(path) - 1):
                        curr, nxt = path[i], path[i+1]
                        try:
                            step_w = next(w for target, w in graph_system.adjacency_list.get(curr, []) if target == nxt)
                            st.write(f"🚶 Dari **{curr}** menuju **{nxt}** ⏱️ Memakan Waktu: `{step_w} menit`")
                        except StopIteration:
                            st.write(f"🚶 Dari **{curr}** menuju **{nxt}** ⏱️ Memakan Waktu: `N/A`")

elif app_mode == "📊 Inspeksi Struktur Data Graph":
    st.title("🗄️ Verifikasi dan Representasi Struktur Data")
    st.markdown("---")
    
    st.markdown("### 1. Representasi Adjacency Matrix (Matriks Ketetanggaan)")
    st.dataframe(graph_system.get_adjacency_matrix(), use_container_width=True)
    
    st.markdown("### 2. Representasi Adjacency List (Daftar Ketetanggaan)")
    list_data = []
    for node, edges in graph_system.adjacency_list.items():
        con_nodes = ", ".join([f"[{dst} | Bobot: {w} min]" for dst, w in edges]) if edges else "None (Sink Node)"
        list_data.append({"Simpul (Vertex)": node, "Daftar Hubungan Tetangga & Bobot Perjalanan (Edge, Weight)": con_nodes})
    st.dataframe(pd.DataFrame(list_data), use_container_width=True, hide_index=True)

    st.markdown("### 📈 3. Analisis Centrality (Sentralitas Jaringan Graf)")
    centrality_data = graph_system.compute_degree_centrality()
    sorted_centrality = sorted(centrality_data.items(), key=lambda x: x[1], reverse=True)
    
    df_centrality = pd.DataFrame(sorted_centrality, columns=["Nama Tempat / Node", "Skor Hubungan Koneksi (Degree Centrality)"])
    st.dataframe(df_centrality, use_container_width=True, hide_index=True)
    st.info("💡 **Analisis Teori Keputusan:** Node dengan skor Centrality tertinggi merepresentasikan hub utama atau lokasi yang paling strategis di dalam pemetaan transportasi Beach Club Bali.")
