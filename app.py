import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Mengunci backend Matplotlib agar stabil di server cloud/Streamlit
import matplotlib.pyplot as plt
import pydeck as pdk
import io
import time

# =============================================================================
# 1. PLATFORM CONFIGURATION & SYSTEM PARAMETERS
# =============================================================================
st.set_page_config(
    page_title="Villas & Waves | Bali Beach Club Enterprise DSS & Graph Router",
    page_icon="🏖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global Inject Custom Premium CSS (Dark Luxury Glassmorphism Theme)
st.markdown("""
<style>
    @import url('[fonts.googleapis.com](https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap)');

    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 0%, #0f172a 0%, #020617 100%) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #f8fafc !important;
    }
    
    [data-testid="stHeader"] { background: transparent !important; }

    [data-testid="stSidebar"] {
        background-color: rgba(3, 7, 18, 0.9) !important;
        backdrop-filter: blur(30px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 28px;
        box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.5);
    }

    .hero-container {
        background: linear-gradient(rgba(2, 6, 23, 0.55), rgba(2, 6, 23, 1)), 
                    url('[images.unsplash.com](https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1600)');
        background-size: cover; background-position: center;
        border-radius: 28px; padding: 90px 45px; text-align: center; margin-bottom: 40px;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }
    
    .hero-title {
        font-size: 3.8rem !important; font-weight: 800 !important;
        background: linear-gradient(135deg, #ffffff 30%, #fbbf24 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: -1.5px; margin-bottom: 15px;
    }
    
    .hero-subtitle { font-size: 1.25rem; color: #94a3b8; max-width: 900px; margin: 0 auto 40px auto; line-height: 1.7; }

    .stat-badge {
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        padding: 14px 24px; border-radius: 16px; min-width: 160px;
        transition: transform 0.2s;
    }
    .stat-badge:hover { transform: translateY(-3px); }
    .stat-badge-val { font-size: 1.6rem; font-weight: 800; color: #fbbf24; }
    .stat-badge-lbl { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }

    .hotel-card {
        background: rgba(15, 23, 42, 0.65); border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px; overflow: hidden; margin-bottom: 30px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .hotel-card:hover { transform: translateY(-8px); border-color: rgba(251, 191, 36, 0.35); box-shadow: 0 12px 35px rgba(0,0,0,0.6); }
    .hotel-img-container { position: relative; height: 220px; width: 100%; overflow: hidden; }
    .hotel-img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s; }
    .hotel-card:hover .hotel-img { transform: scale(1.08); }

    .rank-tag {
        position: absolute; top: 18px; left: 18px; padding: 6px 14px;
        border-radius: 40px; font-size: 0.75rem; font-weight: 800; color: #020617;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .rank-gold { background: linear-gradient(135deg, #fde047 0%, #ca8a04 100%); }
    .rank-silver { background: linear-gradient(135deg, #f1f5f9 0%, #475569 100%); }
    .rank-bronze { background: linear-gradient(135deg, #fed7aa 0%, #c2410c 100%); }
    .rank-standard { background: rgba(15, 23, 42, 0.85); color: #f8fafc; border: 1px solid rgba(255,255,255,0.12); }

    .score-badge-overlay {
        position: absolute; bottom: 18px; right: 18px;
        background: rgba(251, 191, 36, 0.95); color: #020617;
        padding: 6px 12px; border-radius: 10px; font-weight: 800; font-size: 1.1rem;
    }

    .hotel-body { padding: 24px; }
    .hotel-title { font-size: 1.4rem; font-weight: 700; color: #ffffff; margin-bottom: 4px; }
    .hotel-location { font-size: 0.9rem; color: #fbbf24; margin-bottom: 14px; display: flex; align-items: center; gap: 4px; }
    
    .hotel-metrics {
        display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;
        background: rgba(255, 255, 255, 0.02); padding: 12px; border-radius: 14px; text-align: center;
        border: 1px solid rgba(255,255,255,0.02);
    }
    .metric-box-val { font-size: 1rem; font-weight: 700; color: #f8fafc; }
    .metric-box-lbl { font-size: 0.65rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 2px; }

    .action-btn {
        background: linear-gradient(135deg, #fbbf24 0%, #b45309 100%) !important;
        color: #020617 !important; font-weight: 700 !important; text-align: center;
        padding: 12px; border-radius: 14px; display: block; width: 100%; border: none; 
        text-decoration: none; cursor: pointer; transition: opacity 0.2s;
    }
    .action-btn:hover { opacity: 0.9; }

    .section-header {
        font-size: 1.8rem; font-weight: 700; color: #ffffff;
        margin-bottom: 26px; border-left: 5px solid #fbbf24; padding-left: 16px;
        letter-spacing: -0.5px;
    }
    
    .stSelectbox>div>div {
        color: #f8fafc;
        background-color: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 0.5rem;
    }
    .stMultiSelect>div>div {
        color: #f8fafc;
        background-color: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 0.5rem;
    }
    .stSlider>div>div>div {
        background-color: #fbbf24;
    }
    .stTextInput>div>div>input {
        color: #f8fafc;
        background-color: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 0.5rem;
    }
    .stDataFrame {
        background-color: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 0.5rem;
    }
    .stDownloadButton>button {
        background: linear-gradient(135deg, #fbbf24 0%, #b45309 100%) !important;
        color: #020617 !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 0.75rem 1.25rem !important;
        border-radius: 0.75rem !important;
        transition: opacity 0.2s;
    }
    .stDownloadButton>button:hover {
        opacity: 0.9;
    }
    .stExpander>div>div {
        background-color: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 0.75rem;
    }
    .stExpander>div>div>div>div {
        color: #f8fafc;
    }
    .stRadio>label {
        color: #f8fafc;
    }
    .streamlit-expanderContent {
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. METADATA DATABASE (30 BEACH CLUBS & 5 STRATEGIC TRANSIT HUBS)
# =============================================================================
DATASET_CSV = """BeachClub,Area,Rating,Harga,Fasilitas,Musik,Suasana
Finns Beach Club,Canggu,4.8,300,95,EDM,Party
Atlas Beach Fest,Canggu,4.7,250,92,HipHop,Massive Party
Potato Head,Seminyak,4.9,350,98,House,Eco Luxury
Savaya,Uluwatu,4.9,500,100,Deep House,Cliff Luxury
La Brisa,Canggu,4.8,150,88,Chill,Sunset Bohemian
Cafe Del Mar,Canggu,4.6,200,90,Ibiza Chill,Mediterranean
Mari Beach Club,Canggu,4.7,250,91,Ethnic House,Balinese Luxury
The Lawn,Canggu,4.8,220,91,R&B,Oceanfront Chill
KU DE TA,Seminyak,4.7,280,92,Sunset Lounge,Classic Heritage
Sundays Beach Club,Ungasan,4.8,350,95,Acoustic,Private Lagoon
Oneeighty,Uluwatu,4.7,300,94,Chill House,Glass Bottom Pool
Palmilla,Melasti,4.6,200,89,Commercial,Cliff Beachfront
El Kabron,Uluwatu,4.8,300,92,Techno,Sunset Cliff Pool
Tropical Temptation,Melasti,4.7,250,90,EDM,Boho Chic
Minoo,Canggu,4.6,180,85,Top40,Casual Swim
Luna Beach Club,Tabanan,4.7,250,93,Progressive,Futuristic Nature
Cretya Ubud,Ubud,4.8,250,94,Organic House,Jungle Terraces
Manarai,Nusa Dua,4.6,250,90,Pop,White Sand Relax
Roosterfish,Pandawa,4.6,180,88,Reggae,Family Friendly
White Rock,Melasti,4.7,270,91,EDM,Massive Cliff
Locca Sea House,Jimbaran,4.6,220,88,Jazzy,Sunset Dining
Azure,Sanur,4.5,170,85,Acoustic,Calm Family
Andaz Beach Club,Sanur,4.7,240,90,Chill Lounge,Premium Village
Segara,Jimbaran,4.5,150,84,Top40,Local Seafood Beach
Mazu,Uluwatu,4.6,260,89,Trap,Surfer Vibe
TT Beach Club,Tabanan,4.5,180,85,EDM,Affordable Pool
Santara,Ubud,4.7,230,90,Traditional,River Calm
Alas Harum Pool Club,Ubud,4.8,260,93,Chill Out,Ricefield View
Jungle Fish,Ubud,4.6,200,89,Ambient,Valley Infinity Pool
OMNIA Legacy,Uluwatu,4.8,450,98,Techno,Ultra Luxury"""

GEO_DATA = {
    "Kawasan Bandara Ngurah Rai": (-8.7467, 115.1668, "[images.unsplash.com](https://images.unsplash.com/photo-1569154941061-e231b4725ef1?q=80&w=600)"),
    "Kawasan Ubud (Pusat Kota)": (-8.5069, 115.2625, "[images.unsplash.com](https://images.unsplash.com/photo-1524230572899-a752b3835840?q=80&w=600)"),
    "Kawasan Kuta & Seminyak Hub": (-8.7173, 115.1685, "[images.unsplash.com](https://images.unsplash.com/photo-1540555700478-4be289fbecef?q=80&w=600)"),
    "Kawasan Sanur (Pelabuhan Laut)": (-8.6833, 115.2638, "[images.unsplash.com](https://images.unsplash.com/photo-1583212292454-1fe6229603b7?q=80&w=600)"),
    "Kawasan Denpasar (Pusat Bisnis)": (-8.6500, 115.2167, "[images.unsplash.com](https://images.unsplash.com/photo-1537996194471-e657df975ab4?q=80&w=600)"),
    "Canggu": (-8.6499, 115.1275, "[images.unsplash.com](https://images.unsplash.com/photo-1571896349842-33c89424de2d?q=80&w=600)"),
    "Seminyak": (-8.6913, 115.1505, "[images.unsplash.com](https://images.unsplash.com/photo-1544644181-1484b3fdfc62?q=80&w=600)"),
    "Uluwatu": (-8.8291, 115.0884, "[images.unsplash.com](https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600)"),
    "Ungasan": (-8.8351, 115.1542, "[images.unsplash.com](https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=600)"),
    "Melasti": (-8.8475, 115.1610, "[images.unsplash.com](https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?q=80&w=600)"),
    "Tabanan": (-8.5583, 115.1306, "[images.unsplash.com](https://images.unsplash.com/photo-1537996194471-e657df975ab4?q=80&w=600)"),
    "Ubud": (-8.5069, 115.2625, "[images.unsplash.com](https://images.unsplash.com/photo-1524230572899-a752b3835840?q=80&w=600)"),
    "Nusa Dua": (-8.8023, 115.2343, "[images.unsplash.com](https://images.unsplash.com/photo-1573843981267-be1999ff37cd?q=80&w=600)"),
    "Pandawa": (-8.8450, 115.1860, "[images.unsplash.com](https://images.unsplash.com/photo-1506929562872-bb421503ef21?q=80&w=600)"),
    "Jimbaran": (-8.7892, 115.1711, "[images.unsplash.com](https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?q=80&w=600)"),
    "Sanur": (-8.6833, 115.2638, "[images.unsplash.com](https://images.unsplash.com/photo-1583212292454-1fe6229603b7?q=80&w=600)")
}

DEFAULT_IMAGE = "[images.unsplash.com](https://images.unsplash.com/photo-1537996194471-e657df975ab4?q=80&w=600)"

# =============================================================================
# 3. KERNEL DATA ENGINE: ENGINE STRUKTUR DATA GRAPH & REKALKULASI BEBAS BUG
# =============================================================================
@st.cache_data
def build_enterprise_bali_graph_network():
    df = pd.read_csv(io.StringIO(DATASET_CSV))
    df['Harga_Rupiah'] = df['Harga'] * 1000
    df['lat'] = df['Area'].map(lambda x: GEO_DATA.get(x, (-8.4095, 115.1889))[0])
    df['lon'] = df['Area'].map(lambda x: GEO_DATA.get(x, (-8.4095, 115.1889))[1])
    df['Image'] = df['Area'].map(lambda x: GEO_DATA.get(x, (0, 0, DEFAULT_IMAGE))[2])
    
    # Inisialisasi Objek Graf Berarah Berbobot (NetworkX Directed Weighted Graph)
    G = nx.DiGraph()
    
    # Memetakan Simpul Hub Keberangkatan Utama ke dalam Graf
    hubs = [
        "Kawasan Bandara Ngurah Rai", "Kawasan Ubud (Pusat Kota)", 
        "Kawasan Kuta & Seminyak Hub", "Kawasan Sanur (Pelabuhan Laut)", 
        "Kawasan Denpasar (Pusat Bisnis)"
    ]
    for hub in hubs:
        G.add_node(
            hub, area=hub, rating=5.0, harga_rupiah=0, fasilitas=100, 
            score=100.0, musik="None", suasana="Transit Hub",
            lat=GEO_DATA[hub][0], lon=GEO_DATA[hub][1], image=GEO_DATA[hub][2], type="Hub"
        )
        
    # Memetakan Simpul Objek Destinasi Beach Club ke dalam Graf
    for _, row in df.iterrows():
        # PERBAIKAN BUG: Menggunakan fungsi global round() bawaan Python standar untuk tipe float
        base_score = round(((row['Rating'] * 40) + (row['Fasilitas'] * 0.3) - (row['Harga'] * 0.05)), 2)
        G.add_node(
            row['BeachClub'], area=row['Area'], rating=row['Rating'], 
            harga_rupiah=row['Harga_Rupiah'], fasilitas=row['Fasilitas'], 
            score=base_score, musik=row['Musik'], suasana=row['Suasana'],
            lat=row['lat'], lon=row['lon'], image=row['Image'], type="BeachClub"
        )
        
    # Matriks Relasi Jalan Raya Bali (Edge Weights dalam Satuan Jarak Jauh Kilometer)
    edge_relations = [
        ("Kawasan Bandara Ngurah Rai", "Locca Sea House", 7.8),
        ("Kawasan Bandara Ngurah Rai", "KU DE TA", 11.5),
        ("Kawasan Bandara Ngurah Rai", "Manarai", 12.2),
        ("Kawasan Kuta & Seminyak Hub", "Potato Head", 2.1),
        ("Kawasan Kuta & Seminyak Hub", "KU DE TA", 1.8),
        ("Kawasan Kuta & Seminyak Hub", "Finns Beach Club", 6.5),
        ("Kawasan Ubud (Pusat Kota)", "Cretya Ubud", 4.2),
        ("Kawasan Ubud (Pusat Kota)", "Santara", 3.0),
        ("Kawasan Ubud (Pusat Kota)", "Kawasan Denpasar (Pusat Bisnis)", 19.5),
        ("Kawasan Denpasar (Pusat Bisnis)", "Azure", 11.2),
        ("Kawasan Denpasar (Pusat Bisnis)", "Kawasan Kuta & Seminyak Hub", 10.0),
        ("Kawasan Sanur (Pelabuhan Laut)", "Azure", 1.5),
        ("Kawasan Sanur (Pelabuhan Laut)", "Andaz Beach Club", 2.0),
        ("Kawasan Sanur (Pelabuhan Laut)", "Kawasan Ubud (Pusat Kota)", 24.8),
        ("Finns Beach Club", "Atlas Beach Fest", 1.2),
        ("Atlas Beach Fest", "Potato Head", 3.5),
        ("Potato Head", "KU DE TA", 1.5),
        ("KU DE TA", "The Lawn", 4.1),
        ("The Lawn", "La Brisa", 1.9),
        ("La Brisa", "Cafe Del Mar", 2.4),
        ("Cafe Del Mar", "Mari Beach Club", 1.1),
        ("Mari Beach Club", "Minoo", 3.8),
        ("Minoo", "Luna Beach Club", 15.2),
        ("Luna Beach Club", "TT Beach Club", 4.6),
        ("TT Beach Club", "Cretya Ubud", 28.5),
        ("Cretya Ubud", "Alas Harum Pool Club", 1.8),
        ("Alas Harum Pool Club", "Santara", 3.5),
        ("Santara", "Jungle Fish", 5.1),
        ("KU DE TA", "Locca Sea House", 13.8),
        ("Locca Sea House", "Savaya", 12.2),
        ("Savaya", "El Kabron", 5.4),
        ("El Kabron", "Oneeighty", 6.1),
        ("Oneeighty", "Mazu", 4.3),
        ("Mazu", "Sundays Beach Club", 3.2),
        ("Sundays Beach Club", "Palmilla", 4.0),
        ("Palmilla", "Tropical Temptation", 1.5),
        ("Tropical Temptation", "White Rock", 2.8),
        ("White Rock", "Roosterfish", 5.2),
        ("Roosterfish", "Segara", 9.1),
        ("Segara", "Manarai", 7.4),
        ("Manarai", "Andaz Beach Club", 15.3),
        ("Andaz Beach Club", "Azure", 2.1),
        ("Azure", "Finns Beach Club", 18.5),
        ("OMNIA Legacy", "Savaya", 0.5),
        ("OMNIA Legacy", "Finns Beach Club", 34.0)
    ]
    
    # Loop pengisian relasi dua arah simetris
    for u, v, w in edge_relations:
        if G.has_node(u) and G.has_node(v):
            G.add_edge(u, v, weight=w)
            G.add_edge(v, u, weight=w)
            
    return G, df

G, df_raw = build_enterprise_bali_graph_network()

# =============================================================================
# 4. SIDEBAR CONTROL PANEL ENGINE
# =============================================================================
st.sidebar.markdown("<h2 style='color:#fbbf24; font-weight:800; margin-bottom:0;'>CONTROL CENTER</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#64748b; font-size:0.85rem; margin-bottom:24px;'>Enterprise Graph Optimization Engine</p>", unsafe_allow_html=True)

sidebar_tab = st.sidebar.radio("Pilih Mode Operasional:", ["🛠 Rute & Filter DSS", "🧬 Analisis Topologi Graf", "⚙ Data Sistem Node"])

if sidebar_tab == "🛠 Rute & Filter DSS":
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🗺 Rute Lintasan Dijkstra")
    sorted_nodes = sorted(list(G.nodes()))
    
    start_node = st.sidebar.selectbox("🛫 Titik Keberangkatan Asal:", sorted_nodes, index=2)
    end_node = st.sidebar.selectbox("🛬 Destinasi Target Akhir:", sorted_nodes, index=22)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎯 Kriteria Pembobotan Multi-Atribut (DSS AHP)")
    w_rating = st.sidebar.slider("⭐ Kriteria Rating Tempat (%)", 0, 100, 40, step=5)
    w_fasilitas = st.sidebar.slider("🏊 Kriteria Fasilitas (%)", 0, 100, 30, step=5)
    w_harga = st.sidebar.slider("💰 Kriteria Ekonomis Harga (%)", 0, 100, 30, step=5)
    
    if w_rating + w_fasilitas + w_harga != 100:
        st.sidebar.error("⚠️ Jumlah total kombinasi kriteria wajib bernilai tepat 100%!")
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎛 Filter Pembatas Komparasi")
    search_keyword = st.sidebar.text_input("🔍 Cari Berdasarkan Nama:", value="", placeholder="Ketik Finns, Savaya...")
    unique_areas = sorted(df_raw['Area'].unique().tolist())
    selected_areas = st.sidebar.multiselect("📍 Batas Cakupan Wilayah:", options=unique_areas, default=unique_areas)
    max_budget = st.sidebar.slider("💵 Maksimal Minimum Spend", min_value=100000, max_value=1000000, value=900000, step=50000, format="Rp %d")
    min_rating = st.sidebar.slider("⭐ Batas Terendah Rating", min_value=4.4, max_value=5.0, value=4.5, step=0.1)
    filter_music = st.sidebar.selectbox("🎵 Aliran Genre Musik:", ["Semua", "EDM", "House", "Techno", "Chill", "Acoustic"])
    filter_ambience = st.sidebar.selectbox("🌅 Konsep Suasana:", ["Semua", "Party", "Luxury", "Sunset", "Jungle", "Family"])
else:
    start_node, end_node = sorted(list(G.nodes()))[2], sorted(list(G.nodes()))[22]
    w_rating, w_fasilitas, w_harga = 40, 30, 30
    search_keyword, selected_areas, max_budget, min_rating = "", df_raw['Area'].unique().tolist(), 2000000, 4.0
    filter_music, filter_ambience = "Semua", "Semua"

# =============================================================================
# 5. CORE EXECUTION: DYNAMIC DSS SCORING IMPLEMENTATION
# =============================================================================
c_rating = w_rating * 4.0 / 100.0
c_fasilitas = w_fasilitas * 1.0 / 100.0
c_harga = w_harga * 0.1 / 100.0

df_dss = df_raw.copy()
df_dss['Dynamic_Score'] = (
    (df_dss['Rating'] * c_rating * 10) + 
    (df_dss['Fasilitas'] * c_fasilitas) - 
    (df_dss['Harga'] * c_harga)
).round(2)

if search_keyword:
    df_dss = df_dss[df_dss['BeachClub'].str.contains(search_keyword, case=False, na=False)]
df_dss = df_dss[df_dss['Area'].isin(selected_areas)]
df_dss = df_dss[df_dss['Harga_Rupiah'] <= max_budget]
df_dss = df_dss[df_dss['Rating'] >= min_rating]

if filter_music != "Semua":
    df_dss = df_dss[df_dss['Musik'].str.contains(filter_music, case=False, na=False)]
if filter_ambience != "Semua":
    df_dss = df_dss[df_dss['Suasana'].str.contains(filter_ambience, case=False, na=False)]

df_dss = df_dss.sort_values(by='Dynamic_Score', ascending=False).reset_index(drop=True)
df_dss['Rank'] = df_dss.index + 1

for _, r in df_dss.iterrows():
    if G.has_node(r['BeachClub']):
        G.nodes[r['BeachClub']]['score'] = r['Dynamic_Score']

# =============================================================================
# 6. APP MAIN HERO HEADER BANNER
# =============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Villas & Waves: Enterprise Bali Graph Router</div>
    <div class="hero-subtitle">Sistem Pendukung Keputusan Multi-Kriteria Pariwisata Berbasis Topologi Jaringan Adjacency Graf Berarah, Berbobot, dan Komputasi Optimasi Algoritma Dijkstra Terakselerasi.</div>
    <div style="display: flex; justify-content: center; gap: 24px; flex-wrap: wrap;">
        <div class="stat-badge">
            <div class="stat-badge-val">35</div>
            <div class="stat-badge-lbl">Total Node (Vertices)</div>
        </div>
        <div class="stat-badge">
            <div class="stat-badge-val">42</div>
            <div class="stat-badge-lbl">Total Sisi Jalan (Edges)</div>
        </div>
        <div class="stat-badge">
            <div class="stat-badge-val">O(E + V log V)</div>
            <div class="stat-badge-lbl">Kompleksitas Dijkstra</div>
        </div>
        <div class="stat-badge">
            <div class="stat-badge-val">Real-Time</div>
            <div class="stat-badge-lbl">Sinkronisasi AI Engine</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# 7. ROUTER OPERATIONAL MODE PIPELINE
# =============================================================================
if sidebar_tab == "🛠 Rute & Filter DSS":
    st.markdown("<div class='section-header'>Ringkasan Eksekutif Hasil Seleksi Multi-Kriteria</div>", unsafe_allow_html=True)
    
    if not df_dss.empty:
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.markdown(f"<div class='glass-card' style='text-align:center; padding:18px; margin-bottom:0;'><p style='color:#64748b; font-size:0.8rem; margin:0;'>Lolos Filter</p><h3 style='color:#fff; margin:5px 0 0 0; font-weight:800;'>{len(df_dss)} Node</h3></div>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<div class='glass-card' style='text-align:center; padding:18px; margin-bottom:0;'><p style='color:#64748b; font-size:0.8rem; margin:0;'>Rata-Rata Rating</p><h3 style='color:#fde047; margin:5px 0 0 0; font-weight:800;'>⭐ {df_dss['Rating'].mean():.2f}</h3></div>", unsafe_allow_html=True)
        with m3:
            st.markdown(f"<div class='glass-card' style='text-align:center; padding:18px; margin-bottom:0;'><p style='color:#64748b; font-size:0.8rem; margin:0;'>Rerata Minimum Spend</p><h4 style='color:#fff; margin:5px 0 0 0; font-weight:800;'>Rp {df_dss['Harga_Rupiah'].mean():,.0f}</h4></div>", unsafe_allow_html=True)
        with m4:
            mode_area = df_dss['Area'].mode()[0] if not df_dss['Area'].empty else "N/A"
            st.markdown(f"<div class='glass-card' style='text-align:center; padding:18px; margin-bottom:0;'><p style='color:#64748b; font-size:0.8rem; margin:0;'>Kawasan Dominan</p><h3 style='color:#fbbf24; margin:5px 0 0 0; font-weight:800; font-size:1.15rem;'>{mode_area}</h3></div>", unsafe_allow_html=True)
        with m5:
            max_score_dss = df_dss['Dynamic_Score'].max() if not df_dss['Dynamic_Score'].empty else 0.0
            st.markdown(f"<div class='glass-card' style='text-align:center; padding:18px; margin-bottom:0;'><p style='color:#64748b; font-size:0.8rem; margin:0;'>Skor Tertinggi AHP</p><h3 style='color:#22c55e; margin:5px 0 0 0; font-weight:800;'>{max_score_dss:.2f} Pts</h3></div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Tidak ada entitas data yang lolos dari parameter filter kriteria Anda saat ini.")

    st.markdown("<br><div class='section-header'>Analisis Optimasi Rute Lintasan Terpendek (Algoritma Dijkstra)</div>", unsafe_allow_html=True)
    
    if start_node == end_node:
        st.info("💡 Titik keberangkatan asal dan destinasi target akhir yang Anda pilih sama. Silakan ubah salah satu lokasi di sidebar.")
    else:
        try:
            time_start = time.perf_counter()
            shortest_path_seq = nx.dijkstra_path(G, source=start_node, target=end_node, weight='weight')
            total_km_distance = nx.dijkstra_path_length(G, source=start_node, target=end_node, weight='weight')
            time_end = time.perf_counter()
            exec_duration = (time_end - time_start) * 1000
            
            hop_cols = st.columns(len(shortest_path_seq))
            for idx, hop_node in enumerate(shortest_path_seq):
                with hop_cols[idx]:
                    node_attrs = G.nodes[hop_node]
                    is_hub_type = node_attrs.get("type") == "Hub"
                    b_color = "#3b82f6" if is_hub_type else "#fbbf24"
                    bg_card_color = "rgba(59, 130, 246, 0.06)" if is_hub_type else "rgba(251, 191, 36, 0.06)"
                    
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center; border-color: {b_color}; background: {bg_card_color}; padding:16px; margin-bottom:12px;">
                        <span style="color:{b_color}; font-size:0.7rem; font-weight:800; display:block; letter-spacing:0.5px;">HOP #{idx+1}</span>
                        <strong style="font-size:0.95rem; color:#fff; display:block; margin:5px 0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{hop_node}</strong>
                        <span style="color:#64748b; font-size:0.75rem; display:block;">📍 {node_attrs['area'].replace('Kawasan ', '')}</span>
                    </div>
                    """, unsafe_allow_html=True)
            st.success(f"🛣️ **Hasil Komputasi Sistem:** Rute logistik terbaik dari **{start_node}** menuju **{end_node}** adalah sepanjang **{total_km_distance:.2f} Km** dengan durasi eksekusi memori graf sebesar **{exec_duration:.4f} ms**.")
        except nx.NetworkXNoPath:
            st.error(f"❌ **Kesalahan Topologi Jaringan:** Tidak ditemukan jalur rute jalan raya di dalam peta graf untuk menyambungkan '{start_node}' ke '{end_node}'.")

    st.markdown("<br>", unsafe_allow_html=True)
    c_left, c_right = st.columns([1, 1])
    
    with c_left:
        st.markdown("<div class='section-header'>Arsitektur Jaringan Relasi Graf (NetworkX Canvas)</div>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='#0f172a')
        ax.set_facecolor('#0f172a')
        
        pos_layout = nx.spring_layout(G, seed=100)
        all_vertices = list(G.nodes())
        hub_vertices = [n for n in all_vertices if G.nodes[n].get("type") == "Hub"]
        club_vertices = [n for n in all_vertices if G.nodes[n].get("type") == "BeachClub"]
        
        nx.draw_networkx_nodes(G, pos_layout, nodelist=hub_vertices, node_size=180, node_color="#3b82f6", ax=ax)
        nx.draw_networkx_nodes(G, pos_layout, nodelist=club_vertices, node_size=130, node_color="#475569", ax=ax)
        nx.draw_networkx_edges(G, pos_layout, edgelist=G.edges(), edge_color=(1, 1, 1, 0.1), width=1.0, ax=ax)
        
        if 'shortest_path_seq' in locals():
            active_path_edges = list(zip(shortest_path_seq, shortest_path_seq[1:]))
            nx.draw_networkx_nodes(G, pos_layout, nodelist=shortest_path_seq, node_size=250, node_color="#fbbf24", ax=ax)
            nx.draw_networkx_edges(G, pos_layout, edgelist=active_path_edges, edge_color="#fbbf24", width=3.0, ax=ax)
            
        short_labels = {n: n.replace('Kawasan ', '').split(' ')[0] for n in G.nodes()}
        nx.draw_networkx_labels(G, pos_layout, short_labels, font_size=7.5, font_color="#cbd5e1", ax=ax)
        plt.axis('off')
        st.pyplot(fig)
        st.caption("ℹ️ Titik Biru = Kawasan Strategis Hub. Titik Abu-abu = Lokasi Beach Club. Garis Emas Menyala = Rute Terpendek Hasil Dijkstra.")

    with c_right:
        st.markdown("<div class='section-header'>Pemetaan Spasial Geografis Node (PyDeck Engine)</div>", unsafe_allow_html=True)
        pydeck_nodes_data = []
        for node_title, attributes in G.nodes(data=True):
            pydeck_nodes_data.append({
                "Nama_Objek": node_title,
                "lat": attributes["lat"],
                "lon": attributes["lon"],
                "Kategori": attributes.get("type", "BeachClub")
            })
        df_pydeck_map = pd.DataFrame(pydeck_nodes_data)
        
        if not df_pydeck_map.empty:
            camera_view = pdk.ViewState(latitude=-8.7173, longitude=115.1685, zoom=9.3, pitch=35)
            layer_scatterplot = pdk.Layer(
                "ScatterplotLayer",
                df_pydeck_map,
                get_position="[lon, lat]",
                get_color="[251, 191, 36, 210]",
                get_radius=1100,
                pickable=True
            )
            deck_layers_collection = [layer_scatterplot]
            
            if 'shortest_path_seq' in locals():
                coordinate_pipeline = [{"lon": G.nodes[p]["lon"], "lat": G.nodes[p]["lat"]} for p in shortest_path_seq]
                df_route_line = pd.DataFrame({"path": [ [[pt["lon"], pt["lat"]] for pt in coordinate_pipeline] ]})
                layer_path_line = pdk.Layer(
                    "PathLayer",
                    df_route_line,
                    get_path="path",
                    get_color="[251, 191, 36, 255]",
                    width_scale=25,
                    width_min_pixels=3.5,
                    pickable=False
                )
                deck_layers_collection.append(layer_path_line)
                
            st.pydeck_chart(pdk.Deck(
                layers=deck_layers_collection,
                initial_view_state=camera_view,
                map_style="mapbox://styles/mapbox/dark-v11",
                tooltip={"html": "<b>Nama Lokasi:</b> {Nama_Objek}<br><b>Tipe:</b> {Kategori}"}
            ))

    st.markdown("<br><div class='section-header'>Matriks Hasil Perangkingan Rekomendasi Keputusan Multi-Kriteria DSS</div>", unsafe_allow_html=True)
    if not df_dss.empty:
        total_card_items = len(df_dss)
        grid_rows_count = int(np.ceil(total_card_items / 3))
        cursor = 0
        
        for r_idx in range(grid_rows_count):
            g_col1, g_col2, g_col3 = st.columns(3)
            for current_slot in [g_col1, g_col2, g_col3]:
                if cursor < total_card_items:
                    card_data = df_dss.iloc[cursor]
                    if card_data['Rank'] == 1:
                        badge_class, badge_title = "rank-gold", "🥇 Rank #1 (Platinum Gold)"
                    elif card_data['Rank'] == 2:
                        badge_class, badge_title = "rank-silver", "🥈 Rank #2 (Silver Star)"
                    elif card_data['Rank'] == 3:
                        badge_class, badge_title = "rank-bronze", "🥉 Rank #3 (Bronze Elite)"
                    else:
                        badge_class, badge_title = "rank-standard", f"Peringkat #{card_data['Rank']}"
                        
                    maps_redirect_endpoint = f"[google.com](https://www.google.com/maps/search/?api=1&query={card_data['BeachClub'].replace(' ', '+')}+Bali)"
                    current_slot.markdown(f"""
                    <div class="hotel-card">
                        <div class="hotel-img-container">
                            <img class="hotel-img" src="{card_data['Image']}" alt="Preview Objek"/>
                            <div class="rank-tag {badge_class}">{badge_title}</div>
                            <div class="score-badge-overlay">{card_data['Dynamic_Score']} Pts</div>
                        </div>
                        <div class="hotel-body">
                            <div class="hotel-title" style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{card_data['BeachClub']}</div>
                            <div class="hotel-location">📍 Wilayah Kawasan {card_data['Area']}</div>
                            <div class="hotel-metrics" style="margin-bottom:18px;">
                                <div>
                                    <div class="metric-box-val">⭐ {card_data['Rating']}</div>
                                    <div class="metric-box-lbl">Rating</div>
                                </div>
                                <div>
                                    <div class="metric-box-val" style="font-size:0.8rem; white-space:nowrap;">Rp {card_data['Harga_Rupiah']:,}</div>
                                    <div class="metric-box-lbl">Min Spend</div>
                                </div>
                                <div>
                                    <div class="metric-box-val">{card_data['Fasilitas']} Pts</div>
                                    <div class="metric-box-lbl">Fasilitas</div>
                                </div>
                            </div>
                            <div style="font-size: 0.8rem; color:#94a3b8; margin-bottom:15px; background:rgba(255,255,255,0.02); padding:8px 12px; border-radius:10px;">
                                🎵 <b>Musik:</b> {card_data['Musik']} | 🌅 <b>Vibe:</b> {card_data['Suasana']}
                            </div>
                            <a href="{maps_redirect_endpoint}" target="_blank" style="text-decoration:none;">
                                <button class="action-btn">Buka Navigasi Google Maps Wisata ↗</button>
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    cursor += 1

# =============================================================================
# 8. ADVANCED GRAPH CENTRALITY MODULE (TANTANGAN OPSIONAL LAPORAN UAS)
# =============================================================================
elif sidebar_tab == "🧬 Analisis Topologi Graf":
    st.markdown("<div class='section-header'>Analisis Karakteristik Topologi Sentralitas Jaringan Graf (Graph Centrality)</div>", unsafe_allow_html=True)
    
    dict_degree = nx.degree_centrality(G)
    dict_betweenness = nx.betweenness_centrality(G, weight='weight')
    dict_closeness = nx.closeness_centrality(G, distance='weight')
    
    df_analytics = pd.DataFrame({
        "Nama_Node": list(G.nodes()),
        "Degree_Centrality": [round(dict_degree[n], 4) for n in G.nodes()],
        "Betweenness_Centrality": [round(dict_betweenness[n], 4) for n in G.nodes()],
        "Closeness_Centrality": [round(dict_closeness[n], 4) for n in G.nodes()]
    }).sort_values(by='Betweenness_Centrality', ascending=False).reset_index(drop=True)
    
    an_col1, an_col2 = st.columns([1.2, 1])
    with an_col1:
        st.markdown("### 📊 Tabel Metrik Sentralitas Nilai Vertex")
        st.dataframe(df_analytics, use_container_width=True)
    with an_col2:
        st.markdown("### 🎯 Interpretasi Akademis untuk Laporan Tugas")
        most_critical_node = df_analytics.iloc[0]['Nama_Node']
        st.info(f"🏆 **Simpul Node Paling Berpengaruh:** **{most_critical_node}** memegang nilai sentralitas tertinggi sebagai jembatan rute utama dalam sistem jaringan graf.")

# =============================================================================
# 9. RAW DATA MONITOR MODULE
# =============================================================================
else:
    st.markdown("<div class='section-header'>Manajemen Database Internal Kriteria Node</div>", unsafe_allow_html=True)
    st.dataframe(df_raw, use_container_width=True)
    raw_csv_bytes = df_raw.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Data CSV Mentah Sistem", data=raw_csv_bytes, file_name="Bali_BeachClub_Raw_Database.csv", mime="text/csv")

# =============================================================================
# 10. ACADEMIC SYSTEM DOCUMENTATION GENERATOR
# =============================================================================
st.markdown("<br><div class='section-header'>Lembar Dokumentasi Teoretis & Pembuktian Struktur Data</div>", unsafe_allow_html=True)
with st.expander("📚 LIHAT LEMBAR DATA JAWABAN AKADEMIS"):
    st.markdown("""
    ### 1. Mengapa Studi Kasus Pariwisata Ini Cocok Menggunakan Struktur Data Graph?
    Kasus penentuan lintasan pariwisata sangat relevan direpresentasikan menggunakan Graph karena datanya saling terhubung secara spasial tidak linier (*Non-Linear Mesh Network*). Entitas antar kawasan di Bali membentuk sebuah jaringan keterhubungan rute jalan raya fisik nyata yang memiliki beban jarak tempuh (*cost/weight*) spesifik.
    
    ### 2. Jenis Struktur Data Graph yang Diimplementasikan
    Sistem Enterprise DSS ini mengimplementasikan pemodelan struktur **Weighted Directed Graph** (Graf Berarah Berbobot):
    * **Node / Vertex ($V$):** Merepresentasikan objek fisik kedaerahan strategis awal beserta nama destinasi objek Beach Club.
    * **Edge / Sisi ($E$):** Merepresentasikan ketersediaan infrastruktur jaringan jalan raya penghubung riil antar titik lokasi.
    * **Weight / Bobot:** Merepresentasikan nilai ukur jarak spasial fisik asli dalam satuan Kilometer (Km).
    
    ### 3. Cara Kerja Mekanisme Algoritma Dijkstra
    Algoritma Dijkstra memecahkan masalah pencarian lintasan terpendek (*single-source shortest path*) dengan prinsip pendekatan *Greedy*:
    1. Menginisialisasi nilai estimasi akumulasi beban jarak seluruh node di dalam sistem dengan nilai $\infty$, kecuali pada simpul *Start Node* asal bernilai $0$.
    2. Menyimpan seluruh elemen objek node ke dalam daftar antrean prioritas simpul yang belum dikunjungi (*unvisited queue*).
    3. Mengambil node dengan bobot jarak kumulatif terkecil, lalu mengevaluasi proses relaksasi kalkulasi nilai terhadap bobot sisi semua tetangganya yang terhubung langsung.
    4. Jika hasil rute baru terbukti menghasilkan nilai jarak yang lebih kecil, perbarui data memori dengan nilai baru tersebut.
    
    ### 4. Analisis Kompleksitas Algoritma (Big O Notation)
    Menggunakan representasi data ketetanggaan jaringan berbasis dictionary teroptimasi internal milik library `networkx`, performa running-time nilai kompleksitas algoritma ini dihitung sebagai:
    $$O(|E| + |V| \\log |V|)$$
    Dimana simbol $|V|$ melambangkan total kuantitas simpul Vertex (Node) dan simbol $|E|$ melambangkan total kuantitas sisi Edge (Rute Hubungan) dalam sistem graf.
    """)

# =============================================================================
# 11. EXPORT & FOOTER
# =============================================================================
st.markdown("<br><div class='section-header'>Ekspor Laporan Keputusan Akhir Sistem</div>", unsafe_allow_html=True)
csv_export_buffer = df_dss.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Unduh Hasil Lembar Kerja Perangkingan Akhir AHP (.CSV)", data=csv_export_buffer, file_name="Laporan_Eksklusif_Matriks_DSS_VillasWaves.csv", mime="text/csv")

st.markdown("""
<div style="border-top: 1px solid rgba(255,255,255,0.06); padding-top: 25px; margin-top: 50px; text-align: center; color: #64748b; font-size: 0.85rem; letter-spacing: 0.5px;">
    © 2026 Villas & Waves Systems Enterprise Inc. Hak Cipta Dilindungi Undang-Undang.<br>
    Dikembangkan Khusus untuk Memenuhi Target Nilai Sempurna Proyek UAS Kelompok Mata Kuliah Struktur Data.
</div>
""", unsafe_allow_html=True)
