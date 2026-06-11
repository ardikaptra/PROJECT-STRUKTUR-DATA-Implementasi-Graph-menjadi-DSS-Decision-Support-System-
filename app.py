import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as o
import pydeck as pdk
import io

st.set_page_config(
    page_title="Villas & Waves | Bali Beach Club DSS Dashboard",
    page_icon="🏖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATASET_CSV = """BeachClub,Area,Rating,Harga,Fasilitas,Jarak
Finns Beach Club,Canggu,4.8,300,95,5
Atlas Beach Fest,Canggu,4.7,250,92,4
Potato Head,Seminyak,4.9,350,98,7
Savaya,Uluwatu,4.9,500,100,15
La Brisa,Canggu,4.8,150,88,3
Cafe Del Mar,Canggu,4.6,200,90,6
Mari Beach Club,Canggu,4.7,250,91,5
The Lawn,Canggu,4.8,220,91,4
KU DE TA,Seminyak,4.7,280,92,8
Sundays Beach Club,Ungasan,4.8,350,95,14
Oneeighty,Uluwatu,4.7,300,94,13
Palmilla,Melasti,4.6,200,89,11
El Kabron,Uluwatu,4.8,300,92,12
Tropical Temptation,Melasti,4.7,250,90,12
Minoo,Canggu,4.6,180,85,5
Luna Beach Club,Tabanan,4.7,250,93,18
Cretya Ubud,Ubud,4.8,250,94,20
Manarai,Nusa Dua,4.6,250,90,16
Roosterfish,Pandawa,4.6,180,88,17
White Rock,Melasti,4.7,270,91,12
Locca Sea House,Jimbaran,4.6,220,88,14
Azure,Sanur,4.5,170,85,19
Andaz Beach Club,Sanur,4.7,240,90,18
Segara,Jimbaran,4.5,150,84,15
Mazu,Uluwatu,4.6,260,89,13
TT Beach Club,Tabanan,4.5,180,85,21
Santara,Ubud,4.7,230,90,22
Alas Harum Pool Club,Ubud,4.8,260,93,21
Jungle Fish,Ubud,4.6,200,89,23
OMNIA Legacy,Uluwatu,4.8,450,98,14"""


GEO_DATA = {
    "Canggu": (-8.6499, 115.1275, "https://images.unsplash.com/photo-1571896349842-33c89424de2d?q=80&w=600&auto=format&fit=crop"),
    "Seminyak": (-8.6913, 115.1505, "https://images.unsplash.com/photo-1540555700478-4be289fbecef?q=80&w=600&auto=format&fit=crop"),
    "Uluwatu": (-8.8291, 115.0884, "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=600&auto=format&fit=crop"),
    "Ungasan": (-8.8351, 115.1542, "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?q=80&w=600&auto=format&fit=crop"),
    "Melasti": (-8.8475, 115.1610, "https://images.unsplash.com/photo-1519046904884-53103b34b206?q=80&w=600&auto=format&fit=crop"),
    "Tabanan": (-8.5583, 115.1306, "https://images.unsplash.com/photo-1537996194471-e657df975ab4?q=80&w=600&auto=format&fit=crop"),
    "Ubud": (-8.5069, 115.2625, "https://images.unsplash.com/photo-1524230572899-a752b3835840?q=80&w=600&auto=format&fit=crop"),
    "Nusa Dua": (-8.8023, 115.2343, "https://images.unsplash.com/photo-1573843981267-be1999ff37cd?q=80&w=600&auto=format&fit=crop"),
    "Pandawa": (-8.8450, 115.1860, "https://images.unsplash.com/photo-1506929562872-bb421503ef21?q=80&w=600&auto=format&fit=crop"),
    "Jimbaran": (-8.7892, 115.1711, "https://images.unsplash.com/photo-1510414842594-a61c69b5ae57?q=80&w=600&auto=format&fit=crop"),
    "Sanur": (-8.6833, 115.2638, "https://images.unsplash.com/photo-1583212292454-1fe6229603b7?q=80&w=600&auto=format&fit=crop"),
}

DEFAULT_IMAGE = "https://images.unsplash.com/photo-1537996194471-e657df975ab4?q=80&w=600&auto=format&fit=crop"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 0%, #151a30 0%, #0b0c10 100%) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #f1f5f9 !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stSidebar"] {
        background-color: rgba(15, 22, 42, 0.75) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    [data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] .stSlider, [data-testid="stSidebar"] .stTextInput {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        border-color: rgba(212, 175, 55, 0.4);
        box-shadow: 0 12px 40px 0 rgba(212, 175, 55, 0.15);
    }

    .hero-container {
        position: relative;
        background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(11, 12, 16, 1)), 
                    url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?q=80&w=1600&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        border-radius: 24px;
        padding: 80px 40px;
        text-align: center;
        margin-bottom: 40px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    
    .hero-title {
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ffffff 30%, #d4af37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin-bottom: 10px;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #94a3b8;
        font-weight: 400;
        max-width: 700px;
        margin: 0 auto 40px auto;
    }

    .stat-row {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    
    .stat-badge {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 12px 24px;
        border-radius: 14px;
        min-width: 150px;
    }
    
    .stat-badge-val {
        font-size: 1.5rem;
        font-weight: 700;
        color: #d4af37;
    }
    
    .stat-badge-lbl {
        font-size: 0.8rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }

    .hotel-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px;
        overflow: hidden;
        margin-bottom: 30px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    .hotel-card:hover {
        transform: translateY(-8px);
        border-color: rgba(212, 175, 55, 0.5);
        box-shadow: 0 15px 35px rgba(212,175,55,0.15);
    }
    
    .hotel-img-container {
        position: relative;
        height: 220px;
        width: 100%;
        overflow: hidden;
    }
    
    .hotel-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s ease;
    }
    
    .hotel-card:hover .hotel-img {
        transform: scale(1.08);
    }

    .rank-tag {
        position: absolute;
        top: 15px;
        left: 15px;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        color: #000;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    .rank-gold { background: linear-gradient(135deg, #ffe066 0%, #f5a623 100%); }
    .rank-silver { background: linear-gradient(135deg, #e2e8f0 0%, #94a3b8 100%); }
    .rank-bronze { background: linear-gradient(135deg, #fbd38d 0%, #b7791f 100%); }
    .rank-standard { background: rgba(15, 23, 42, 0.8); color: #fff; border: 1px solid rgba(255,255,255,0.2); }

    .score-badge-overlay {
        position: absolute;
        bottom: 15px;
        right: 15px;
        background: rgba(212, 175, 55, 0.95);
        color: #0b0c10;
        padding: 6px 12px;
        border-radius: 10px;
        font-weight: 800;
        font-size: 1.1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .hotel-body {
        padding: 20px;
    }
    
    .hotel-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #fff;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .hotel-location {
        font-size: 0.85rem;
        color: #d4af37;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    
    .hotel-metrics {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        background: rgba(255, 255, 255, 0.03);
        padding: 10px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 16px;
        text-align: center;
    }
    
    .metric-box-val {
        font-size: 0.95rem;
        font-weight: 700;
        color: #f1f5f9;
    }
    
    .metric-box-lbl {
        font-size: 0.7rem;
        color: #64748b;
        text-transform: uppercase;
        margin-top: 2px;
    }

    .action-btn-anchor {
        text-decoration: none !important;
    }
    
    .action-btn {
        background: linear-gradient(135deg, #d4af37 0%, #aa841c 100%) !important;
        color: #0b0c10 !important;
        font-weight: 700 !important;
        text-align: center;
        padding: 10px 16px;
        border-radius: 12px;
        display: block;
        transition: all 0.2s ease;
        border: none;
        cursor: pointer;
    }
    
    .action-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(212,175,55,0.3);
    }

    .top-rec-banner {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 2px solid #d4af37;
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 40px;
        box-shadow: 0 10px 40px rgba(212,175,55,0.1);
    }

    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 25px;
        border-left: 4px solid #d4af37;
        padding-left: 15px;
    }
    
    .footer-container {
        border-top: 1px solid rgba(255,255,255,0.08);
        padding-top: 40px;
        margin-top: 60px;
        padding-bottom: 20px;
        color: #64748b;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_initialize_data():
    df = pd.read_csv(io.StringIO(DATASET_CSV))
    
    # Mapping Data Geospasial & Gambar
    df['lat'] = df['Area'].map(lambda x: GEO_DATA.get(x, (-8.4095, 115.1889))[0])
    df['lon'] = df['Area'].map(lambda x: GEO_DATA.get(x, (-8.4095, 115.1889))[1])
    df['Image'] = df['Area'].map(lambda x: GEO_DATA.get(x, (0,0, DEFAULT_IMAGE))[2])
    
    # Konversi Nilai Skala Menjadi Rupiah Riil (Dikali 1000)
    df['Harga_Rupiah'] = df['Harga'] * 1000
    return df

def execute_dss_engine(df):
    """
    Rumus DSS Utama:
    Score = (Rating * 40) + (Fasilitas * 0.3) - (Harga * 0.05) - (Jarak * 0.2)
    """
    df_calc = df.copy()
    df_calc['Score'] = (
        (df_calc['Rating'] * 40) + 
        (df_calc['Fasilitas'] * 0.3) - 
        (df_calc['Harga'] * 0.05) - 
        (df_calc['Jarak'] * 0.2)
    )
    df_calc['Score'] = df_calc['Score'].round(2)
    df_ranked = df_calc.sort_values(by='Score', ascending=False).reset_index(drop=True)
    df_ranked['Rank'] = df_ranked.index + 1
    return df_ranked

def format_rupiah(val):
    return f"Rp {val:,.0f}".replace(",", ".")

# Jalankan Pipeline Data
df_raw = load_and_initialize_data()
df_scored = execute_dss_engine(df_raw)

st.sidebar.markdown("<h2 style='color:#d4af37; font-weight:800; margin-bottom:0;'>EKSPLORASI BALI</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#64748b; font-size:0.85rem; margin-bottom:24px;'>Sistem Pendukung Keputusan Premium</p>", unsafe_allow_html=True)

search_query = st.sidebar.text_input("🔍 Cari Beach Club", value="", placeholder="Contoh: Savaya, Finns...")

all_areas = sorted(df_scored['Area'].unique().tolist())
selected_areas = st.sidebar.multiselect("📍 Filter Wilayah / Area", options=all_areas, default=all_areas)


budget_limit = st.sidebar.slider(
    "💰 Batas Budget Maksimal (Minimum Spend)", 
    min_value=50000, 
    max_value=5000000, 
    value=1500000, 
    step=50000,
    format="Rp %d"
)

min_rating = st.sidebar.slider("⭐ Rating Minimum", min_value=4.0, max_value=5.0, value=4.5, step=0.1)

sort_option = st.sidebar.selectbox(
    "📊 Urutan Prioritas Utama", 
    options=["Skor Rekomendasi DSS", "Rating Tertinggi", "Harga Terendah (Paling Hemat)", "Jarak Terdekat"]
)

df_filtered = df_scored.copy()

if search_query:
    df_filtered = df_filtered[df_filtered['BeachClub'].str.contains(search_query, case=False, na=False)]

df_filtered = df_filtered[df_filtered['Area'].isin(selected_areas)]
df_filtered = df_filtered[df_filtered['Harga_Rupiah'] <= budget_limit]
df_filtered = df_filtered[df_filtered['Rating'] >= min_rating]

if sort_option == "Skor Rekomendasi DSS":
    df_filtered = df_filtered.sort_values(by='Score', ascending=False)
elif sort_option == "Rating Tertinggi":
    df_filtered = df_filtered.sort_values(by='Rating', ascending=False)
elif sort_option == "Harga Terendah (Paling Hemat)":
    df_filtered = df_filtered.sort_values(by='Harga_Rupiah', ascending=True)
elif sort_option == "Jarak Terdekat":
    df_filtered = df_filtered.sort_values(by='Jarak', ascending=True)


st.markdown(f"""
<div class="hero-container">
    <div class="hero-title">Temukan Eksotisme Terbaik di Bali</div>
    <div class="hero-subtitle">Sistem Pengambil Keputusan Analitis Multi-Kriteria (MCDA) yang dikalibrasi khusus untuk memetakan Beach Club premium sesuai preferensi eksklusif Anda.</div>
    <div class="stat-row">
        <div class="stat-badge">
            <div class="stat-badge-val">{len(df_scored)}</div>
            <div class="stat-badge-lbl">Beach Club Terverifikasi</div>
        </div>
        <div class="stat-badge">
            <div class="stat-badge-val">⭐ {df_scored['Rating'].mean():.2f}</div>
            <div class="stat-badge-lbl">Rata-rata Rating</div>
        </div>
        <div class="stat-badge">
            <div class="stat-badge-val">{format_rupiah(df_scored['Harga_Rupiah'].mean())}</div>
            <div class="stat-badge-lbl">Rata-rata Minimum Spend</div>
        </div>
        <div class="stat-badge">
            <div class="stat-badge-val">{df_scored['Area'].nunique()}</div>
            <div class="stat-badge-lbl">Kawasan Hub Elit</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("<div class='section-header'>Ringkasan Dashboard Hasil Filter Analitis</div>", unsafe_allow_html=True)

if not df_filtered.empty:
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; margin: 0;">Sesuai Filter</p>
            <h2 style="color: #fff; margin: 10px 0 0 0; font-weight:800;">{len(df_filtered)} Destinasi</h2>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; margin: 0;">Rerata Rating</p>
            <h2 style="color: #ffe066; margin: 10px 0 0 0; font-weight:800;">⭐ {df_filtered['Rating'].mean():.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; margin: 0;">Rerata Biaya</p>
            <h2 style="color: #fff; margin: 10px 0 0 0; font-weight:800; font-size:1.2rem; padding-top:4px;">{format_rupiah(df_filtered['Harga_Rupiah'].mean())}</h2>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        top_area_val = df_filtered['Area'].mode()[0] if not df_filtered['Area'].empty else "N/A"
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; margin: 0;">Wilayah Dominan</p>
            <h2 style="color: #d4af37; margin: 10px 0 0 0; font-weight:800; font-size:1.4rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{top_area_val}</h2>
        </div>
        """, unsafe_allow_html=True)
    with m5:
        max_score_val = df_filtered['Score'].max() if not df_filtered['Score'].empty else 0.0
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; margin: 0;">Skor DSS Tertinggi</p>
            <h2 style="color: #22c55e; margin: 10px 0 0 0; font-weight:800;">{max_score_val:.1f} Pts</h2>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("Tidak ada destinasi yang cocok dengan kombinasi kriteria filter Anda. Silakan sesuaikan slider di panel kiri.")

st.markdown("<br>", unsafe_allow_html=True)

if not df_filtered.empty:
    top_recommendation = df_filtered.iloc[0]
    maps_url_top = f"https://www.google.com/maps/search/?api=1&query={top_recommendation['BeachClub'].replace(' ', '+')}+Bali"
    
    st.markdown(f"""
    <div class="top-rec-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
            <div>
                <span style="background: #d4af37; color: #000; padding: 4px 12px; border-radius: 8px; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">
                    🏆 REKOMENDASI UTAMA (SKOR TERTINGGI)
                </span>
                <h1 style="color: #fff; margin: 10px 0 5px 0; font-weight: 800;">{top_recommendation['BeachClub']}</h1>
                <p style="color: #94a3b8; margin: 0; font-size: 1.1rem;">
                    Pilihan peringkat #1 berdasarkan perhitungan algoritma DSS multi-kriteria dengan bobot skor agregat sebesar 
                    <strong style="color: #d4af37;">{top_recommendation['Score']} Poin</strong>
                </p>
                <div style="display: flex; gap: 20px; margin-top: 20px; flex-wrap: wrap;">
                    <div style="color:#fff;">📍 <strong>Wilayah:</strong> {top_recommendation['Area']}</div>
                    <div style="color:#ffe066;">⭐ <strong>Rating:</strong> {top_recommendation['Rating']} / 5.0</div>
                    <div style="color:#fff;">💰 <strong>Minimum Spend:</strong> {format_rupiah(top_recommendation['Harga_Rupiah'])}</div>
                    <div style="color:#fff;">⚡ <strong>Indeks Fasilitas:</strong> {top_recommendation['Fasilitas']} Poin</div>
                    <div style="color:#fff;">🚗 <strong>Jarak Pusat:</strong> {top_recommendation['Jarak']} Km</div>
                </div>
            </div>
            <div>
                <a class="action-btn-anchor" href="{maps_url_top}" target="_blank">
                    <button class="action-btn" style="padding: 16px 32px; font-size: 1rem;">Rute Navigasi Utama</button>
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


layout_col1, layout_col2 = st.columns([1, 1])

with layout_col1:
    st.markdown("<div class='section-header'>Peta Kepadatan Geospasial Bali</div>", unsafe_allow_html=True)
    
    if not df_filtered.empty:
        view_state = pdk.ViewState(
            latitude=df_filtered['lat'].mean(),
            longitude=df_filtered['lon'].mean(),
            zoom=9.8,
            pitch=45
        )
        
        layer = pdk.Layer(
            "ScatterplotLayer",
            df_filtered,
            get_position="[lon, lat]",
            get_color="[212, 175, 55, 200]",
            get_radius=800,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=1,
            radius_min_pixels=8,
            radius_max_pixels=30,
            line_width_min_pixels=1,
            get_line_color=[255, 255, 255, 255]
        )
        
        deck_map = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style="mapbox://styles/mapbox/dark-v11",
            tooltip={
                "html": """
                    <div style='background: rgba(15,23,42,0.95); color: white; padding: 12px; border-radius: 10px; border: 1px solid rgba(212,175,55,0.4); font-family: "Plus Jakarta Sans", sans-serif;'>
                        <b style='font-size: 1.1rem; color: #d4af37;'>{BeachClub}</b><br/>
                        <b>Wilayah:</b> {Area}<br/>
                        <b>Skor DSS:</b> {Score} Poin<br/>
                        <b>Rating:</b> ⭐ {Rating}<br/>
                        <b>Jarak:</b> {Jarak} km
                    </div>
                """,
                "style": {"backgroundColor": "transparent", "color": "white", "zIndex": "10000"}
            }
        )
        st.pydeck_chart(deck_map)
    else:
        st.info("Peta tidak dapat dimuat karena tidak ada data yang lolos filter.")

with layout_col2:
    st.markdown("<div class='section-header'>Galeri Eksklusif Bergaya Airbnb</div>", unsafe_allow_html=True)
    
    if not df_filtered.empty:
        row_count = int(np.ceil(len(df_filtered) / 2))
        data_idx = 0
        
        for r in range(row_count):
            g_col1, g_col2 = st.columns(2)
            
            for col in [g_col1, g_col2]:
                if data_idx < len(df_filtered):
                    row = df_filtered.iloc[data_idx]
                    
                    if row['Rank'] == 1:
                        badge_cls, rank_lbl = "rank-gold", "Gold Tier"
                    elif row['Rank'] == 2:
                        badge_cls, rank_lbl = "rank-silver", "Silver Tier"
                    elif row['Rank'] == 3:
                        badge_cls, rank_lbl = "rank-bronze", "Bronze Tier"
                    else:
                        badge_cls, rank_lbl = "rank-standard", f"Peringkat #{row['Rank']}"
                        
                    maps_url = f"https://www.google.com/maps/search/?api=1&query={row['BeachClub'].replace(' ', '+')}+Bali"
                    
                    col.markdown(f"""
                    <div class="hotel-card">
                        <div class="hotel-img-container">
                            <img class="hotel-img" src="{row['Image']}" alt="Foto Beach Club"/>
                            <div class="rank-tag {badge_cls}">{rank_lbl}</div>
                            <div class="score-badge-overlay">{row['Score']}</div>
                        </div>
                        <div class="hotel-body">
                            <div class="hotel-title">{row['BeachClub']}</div>
                            <div class="hotel-location">📍 {row['Area']} • {row['Jarak']} km dari Pusat</div>
                            <div class="hotel-metrics">
                                <div>
                                    <div class="metric-box-val">⭐ {row['Rating']}</div>
                                    <div class="metric-box-lbl">Rating</div>
                                </div>
                                <div>
                                    <div class="metric-box-val" style="font-size:0.75rem; white-space:nowrap;">{format_rupiah(row['Harga_Rupiah'])}</div>
                                    <div class="metric-box-lbl">Min Spend</div>
                                </div>
                                <div>
                                    <div class="metric-box-val">{row['Fasilitas']}</div>
                                    <div class="metric-box-lbl">Fasilitas</div>
                                </div>
                            </div>
                            <a class="action-btn-anchor" href="{maps_url}" target="_blank">
                                <div class="action-btn">Buka Google Maps ↗</div>
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    data_idx += 1
    else:
        st.info("Galeri kosong karena tidak ada aset yang sesuai kriteria.")


st.markdown("<br><div class='section-header'>Inspeksi Detil & Komparasi Kriteria Aset</div>", unsafe_allow_html=True)
if not df_filtered.empty:
    selected_club_name = st.selectbox("🎯 Pilih Beach Club untuk analisis mendalam:", options=df_filtered['BeachClub'].tolist())
    club_meta = df_filtered[df_filtered['BeachClub'] == selected_club_name].iloc[0]
    maps_url_detail = f"https://www.google.com/maps/search/?api=1&query={club_meta['BeachClub'].replace(' ', '+')}+Bali"
    
    det_col1, det_col2 = st.columns([1.2, 2])
    with det_col1:
        st.markdown(f"""
        <div style="border-radius: 24px; overflow: hidden; height: 340px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1);">
            <img src="{club_meta['Image']}" style="width:100%; height:100%; object-fit:cover;" alt="Isolate View Target"/>
        </div>
        """, unsafe_allow_html=True)
    with det_col2:
        st.markdown(f"""
        <div class="glass-card" style="height: 340px; display: flex; flex-direction: column; justify-content: space-between; margin-bottom: 0;">
            <div>
                <h2 style="color: #fff; margin: 0 0 5px 0; font-weight:800;">Analisis Kuantitatif {club_meta['BeachClub']}</h2>
                <p style="color: #d4af37; font-size: 1.1rem; margin-bottom: 20px;">Skor Indeks DSS Akhir: {club_meta['Score']} Poin</p>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                    <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #64748b; font-size: 0.8rem; display: block; text-transform: uppercase;">Klaster Wilayah</span>
                        <strong style="font-size: 1.1rem; color: #fff;">{club_meta['Area']}</strong>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #64748b; font-size: 0.8rem; display: block; text-transform: uppercase;">Skala Kepuasan Pengunjung</span>
                        <strong style="font-size: 1.1rem; color: #ffe066;">⭐ {club_meta['Rating']} / 5.0</strong>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #64748b; font-size: 0.8rem; display: block; text-transform: uppercase;">Minimum Spend (Rupiah)</span>
                        <strong style="font-size: 1.1rem; color: #fff;">{format_rupiah(club_meta['Harga_Rupiah'])}</strong>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #64748b; font-size: 0.8rem; display: block; text-transform: uppercase;">Kapasitas Bobot Fasilitas</span>
                        <strong style="font-size: 1.1rem; color: #fff;">{club_meta['Fasilitas']} / 100 Poin</strong>
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 15px; align-items: center;">
                <span style="color: #64748b; font-size: 0.85rem;">Faktor Jarak Tempuh: {club_meta['Jarak']} km menuju pusat destinasi utama.</span>
                <a class="action-btn-anchor" style="margin-left: auto;" href="{maps_url_detail}" target="_blank">
                    <button class="action-btn" style="padding: 10px 24px;">Buka di Google Maps ↗</button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)


st.markdown("<br><div class='section-header'>Metrik Visualisasi Data & Diagram Keputusan</div>", unsafe_allow_html=True)

if not df_filtered.empty:
    c_col1, c_col2, c_col3 = st.columns([1.2, 1, 1])
    
    with c_col1:
        st.markdown("<p style='color: #94a3b8; font-weight: 600; margin-bottom: 10px;'>Peringkat Efektivitas Skor DSS</p>", unsafe_allow_html=True)
        fig_rank = px.bar(
            df_filtered, 
            x='Score', 
            y='BeachClub', 
            orientation='h',
            color='Score',
            color_continuous_scale='YlOrRd',
            template='plotly_dark'
        )
        fig_rank.update_layout(
            margin=dict(l=20, r=20, t=10, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Skor Rekomendasi DSS",
            yaxis_title=None,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_rank, use_container_width=True)
        
    with c_col2:
        st.markdown("<p style='color: #94a3b8; font-weight: 600; margin-bottom: 10px;'>Korelasi Biaya Minimum vs Kualitas Rating</p>", unsafe_allow_html=True)
        fig_scatter = px.scatter(
            df_filtered,
            x='Harga_Rupiah',
            y='Rating',
            size='Fasilitas',
            color='Area',
            hover_name='BeachClub',
            template='plotly_dark'
        )
        fig_scatter.update_layout(
            margin=dict(l=20, r=20, t=10, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Minimum Spend (IDR)",
            yaxis_title="Skala Rating Bintang"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with c_col3:
        st.markdown("<p style='color: #94a3b8; font-weight: 600; margin-bottom: 10px;'>Distribusi Dominasi Area Berdasarkan Bobot</p>", unsafe_allow_html=True)
        fig_pie = px.pie(
            df_filtered,
            names='Area',
            values='Score',
            hole=0.4,
            template='plotly_dark'
        )
        fig_pie.update_layout(
            margin=dict(l=20, r=20, t=10, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)


st.markdown("<br><div class='section-header'>Ekspor Data Hasil Perhitungan</div>", unsafe_allow_html=True)
st.markdown("Anda dapat mengunduh data matriks hasil perangkingan terfilter di atas untuk keperluan analisis lanjutan.")

@st.cache_data
def transform_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data_buffer = transform_df_to_csv(df_filtered)

st.download_button(
    label="📥 Unduh File Matriks Keputusan (.CSV)",
    data=csv_data_buffer,
    file_name="Peringkat_Beach_Club_Bali_DSS.csv",
    mime="text/csv"
)


st.markdown(f"""
<div class="footer-container">
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 30px;">
        <div style="max-width: 450px;">
            <h4 style="color: #fff; margin: 0 0 10px 0; font-weight: 700; font-size:1.1rem;">Platform Portofolio Villas & Waves DSS</h4>
            <p style="line-height: 1.6;">Sebuah aplikasi tingkat *production portfolio* yang mendemonstrasikan integrasi logika analitis *Decision Support System* dengan antarmuka premium terinspirasi dari portal wisata global terkemuka.</p>
        </div>
        <div>
            <h4 style="color: #fff; margin: 0 0 10px 0; font-weight: 700; font-size:1.1rem;">Teknologi & Framework Stack</h4>
            <p style="margin: 4px 0;">💻 Bahasa Pemrograman Python Core</p>
            <p style="margin: 4px 0;">⚡ Arsitektur Mikro-Sistem Streamlit</p>
            <p style="margin: 4px 0;">📊 Manipulasi Data & Chart via Pandas & Plotly</p>
            <p style="margin: 4px 0;">🎨 Injeksi Gaya Desain Custom Glassmorphism UI</p>
        </div>
        <div>
            <h4 style="color: #fff; margin: 0 0 10px 0; font-weight: 700; font-size:1.1rem;">Rumus Keputusan Multi-Kriteria</h4>
            <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); color:#ffe066; font-family: monospace;">
                Skor = (Rating * 40) + (Fasilitas * 0.3) - (Harga * 0.05) - (Jarak * 0.2)
            </div>
            <p style="font-size: 0.75rem; color:#64748b; margin-top:6px;">Bobot dirancang untuk memaksimalkan kepuasan kualitas internal sambil menekan hambatan jarak geografis & biaya logistik minimum spend.</p>
        </div>
    </div>
    <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.03); font-size: 0.8rem;">
        © 2026 Villas & Waves Systems Enterprise Inc. Dibuat Khusus untuk Portofolio Data Science Kelas Profesional.
    </div>
</div>
""", unsafe_allow_html=True)
