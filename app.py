import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as o
import pydeck as pdk
import io

# -----------------------------------------------------------------------------
# 1. STREAMLIT CONFIGURATION & APP INITIALIZATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Villas & Waves | Bali Beach Club DSS Dashboard",
    page_icon="🏖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. RAW DATA & COORDINATES MAP
# -----------------------------------------------------------------------------
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

# Map locations to mock structural visual links & geo coordinates to guarantee exact rendering
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

# -----------------------------------------------------------------------------
# 3. GLOBAL EXECUTIVE STYLING (DARK LUXURY GLASSMORPHISM)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global Body Overrides */
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 0%, #151a30 0%, #0b0c10 100%) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #f1f5f9 !important;
    }
    
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Sidebar Custom Glassmorphism Theme */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 22, 42, 0.75) !important;
        backdrop-filter: blur(25px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Target inputs/widgets inside Sidebar */
    [data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] .stSlider, [data-testid="stSidebar"] .stTextInput {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px;
    }

    /* Custom Premium Containers & Glassmorphism Design System */
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

    /* Luxury Traveloka-Airbnb Style Hero Section */
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

    /* Quick Stats Inline Engine */
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

    /* Airbnb/Tripadvisor Cards Layout UI Component */
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

    /* Badge Architecture */
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

    /* Call To Action Buttons custom look */
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

    /* Recommendation Standout Banner Section */
    .top-rec-banner {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 2px solid #d4af37;
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 40px;
        box-shadow: 0 10px 40px rgba(212,175,55,0.1);
    }

    /* Typography Utilities */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 25px;
        border-left: 4px solid #d4af37;
        padding-left: 15px;
    }
    
    /* Footer Custom Layout Styling */
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

# -----------------------------------------------------------------------------
# 4. BUSINESS LOGIC & DATA PIPELINE
# -----------------------------------------------------------------------------
@st.cache_data
def load_and_initialize_data():
    df = pd.read_csv(io.StringIO(DATASET_CSV))
    
    # Inject Geo-Coordinates and Image Visuals pipeline maps
    df['lat'] = df['Area'].map(lambda x: GEO_DATA.get(x, (-8.4095, 115.1889))[0])
    df['lon'] = df['Area'].map(lambda x: GEO_DATA.get(x, (-8.4095, 115.1889))[1])
    df['Image'] = df['Area'].map(lambda x: GEO_DATA.get(x, (0,0, DEFAULT_IMAGE))[2])
    
    return df

def execute_dss_engine(df):
    """
    Executes the analytical decision support scoring logic framework.
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
    # Perform strict computational ranking descending
    df_ranked = df_calc.sort_values(by='Score', ascending=False).reset_index(drop=True)
    df_ranked['Rank'] = df_ranked.index + 1
    return df_ranked

# Process Core Engine Collections Pipeline
df_raw = load_and_initialize_data()
df_scored = execute_dss_engine(df_raw)

# -----------------------------------------------------------------------------
# 5. SIDEBAR COMPLEX FILTERING SYSTEM ARCHITECTURE
# -----------------------------------------------------------------------------
st.sidebar.markdown("<h2 style='color:#d4af37; font-weight:800; margin-bottom:0;'>EXPLORE BALI</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#64748b; font-size:0.85rem; margin-bottom:24px;'>Premium Decision Workspace</p>", unsafe_allow_html=True)

search_query = st.sidebar.text_input("🔍 Search Beach Club", value="", placeholder="e.g. Savaya, Finns...")

all_areas = sorted(df_scored['Area'].unique().tolist())
selected_areas = st.sidebar.multiselect("📍 Filter by Area", options=all_areas, default=all_areas)

max_dataset_price = int(df_scored['Harga'].max())
budget_limit = st.sidebar.slider("💰 Maximum Budget (USD / Entry)", min_value=50, max_value=5000, value=1000, step=50)

min_rating = st.sidebar.slider("⭐ Minimum Rating Score", min_value=4.0, max_value=5.0, value=4.5, step=0.1)

sort_option = st.sidebar.selectbox(
    "📊 Primary Sort Sequence", 
    options=["DSS Recommendation Score", "Highest Rating", "Lowest Price (Value)", "Proximity (Nearest)"]
)

# Apply Complex Multi-tier Filters Matrix
df_filtered = df_scored.copy()

if search_query:
    df_filtered = df_filtered[df_filtered['BeachClub'].str.contains(search_query, case=False, na=False)]

df_filtered = df_filtered[df_filtered['Area'].isin(selected_areas)]
df_filtered = df_filtered[df_filtered['Harga'] <= budget_limit]
df_filtered = df_filtered[df_filtered['Rating'] >= min_rating]

# Re-sort data frames dynamically based on secondary filter specifications
if sort_option == "DSS Recommendation Score":
    df_filtered = df_filtered.sort_values(by='Score', ascending=False)
elif sort_option == "Highest Rating":
    df_filtered = df_filtered.sort_values(by='Rating', ascending=False)
elif sort_option == "Lowest Price (Value)":
    df_filtered = df_filtered.sort_values(by='Harga', ascending=True)
elif sort_option == "Proximity (Nearest)":
    df_filtered = df_filtered.sort_values(by='Jarak', ascending=True)

# -----------------------------------------------------------------------------
# 6. HERO DISPLAY BANNER (TRAVELOKA & AIRBNB INSPIRED LUXURY AESTHETIC)
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="hero-container">
    <div class="hero-title">Find the Ultimate Luxury Island Escape</div>
    <div class="hero-subtitle">An Elite Analytical Multi-Criteria Decision Engine providing custom calibrated recommendations for your premier Bali itinerary destinations.</div>
    <div class="stat-row">
        <div class="stat-badge">
            <div class="stat-badge-val">{len(df_scored)}</div>
            <div class="stat-badge-lbl">Verified Clubs</div>
        </div>
        <div class="stat-badge">
            <div class="stat-badge-val">⭐ {df_scored['Rating'].mean():.2f}</div>
            <div class="stat-badge-lbl">Average Rating</div>
        </div>
        <div class="stat-badge">
            <div class="stat-badge-val">${df_scored['Harga'].mean():.0f}</div>
            <div class="stat-badge-lbl">Avg Min Spend</div>
        </div>
        <div class="stat-badge">
            <div class="stat-badge-val">{df_scored['Area'].nunique()}</div>
            <div class="stat-badge-lbl">Elite Hub Areas</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. METRICS & EXECUTIVE DASHBOARD PANEL
# -----------------------------------------------------------------------------
st.markdown("<div class='section-header'>Live Analytics Workspace & Data Stream</div>", unsafe_allow_html=True)

if not df_filtered.empty:
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; margin: 0;">Matches Found</p>
            <h2 style="color: #fff; margin: 10px 0 0 0; font-weight:800;">{len(df_filtered)}</h2>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; margin: 0;">Avg Rating</p>
            <h2 style="color: #ffe066; margin: 10px 0 0 0; font-weight:800;">⭐ {df_filtered['Rating'].mean():.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; margin: 0;">Avg Entry Price</p>
            <h2 style="color: #fff; margin: 10px 0 0 0; font-weight:800;">${df_filtered['Harga'].mean():.1f}</h2>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        top_area_val = df_filtered['Area'].mode()[0] if not df_filtered['Area'].empty else "N/A"
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; margin: 0;">Top Dense Area</p>
            <h2 style="color: #d4af37; margin: 10px 0 0 0; font-weight:800; font-size:1.4rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{top_area_val}</h2>
        </div>
        """, unsafe_allow_html=True)
    with m5:
        max_score_val = df_filtered['Score'].max() if not df_filtered['Score'].empty else 0.0
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 15px;">
            <p style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; margin: 0;">Peak DSS Score</p>
            <h2 style="color: #22c55e; margin: 10px 0 0 0; font-weight:800;">{max_score_val:.1f}</h2>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("No destinations match your current filter parameters. Please adjust parameters in the workspace panel.")

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 8. THE GOLD STANDARD: TOP COMPUTED DSS RECOMMANDATION BANNER
# -----------------------------------------------------------------------------
if not df_filtered.empty:
    # Top absolute model selection across existing options
    top_recommendation = df_filtered.iloc[0]
    
    st.markdown(f"""
    <div class="top-rec-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
            <div>
                <span style="background: #d4af37; color: #000; padding: 4px 12px; border-radius: 8px; font-size: 0.75rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">
                    🏆 CRITERIA MATCH WINNER
                </span>
                <h1 style="color: #fff; margin: 10px 0 5px 0; font-weight: 800;">{top_recommendation['BeachClub']}</h1>
                <p style="color: #94a3b8; margin: 0; font-size: 1.1rem;">
                    Ranked #1 out of all matched clubs with an aggregated Decision Engine Score of 
                    <strong style="color: #d4af37;">{top_recommendation['Score']}</strong>
                </p>
                <div style="display: flex; gap: 20px; margin-top: 20px; flex-wrap: wrap;">
                    <div style="color:#fff;">📍 <strong>Area:</strong> {top_recommendation['Area']}</div>
                    <div style="color:#ffe066;">⭐ <strong>Rating:</strong> {top_recommendation['Rating']}/5.0</div>
                    <div style="color:#fff;">💰 <strong>Min Spend:</strong> ${top_recommendation['Harga']}</div>
                    <div style="color:#fff;">⚡ <strong>Facilities Score:</strong> {top_recommendation['Fasilitas']} pts</div>
                    <div style="color:#fff;">🚗 <strong>Distance Index:</strong> {top_recommendation['Jarak']} km</div>
                </div>
            </div>
            <div>
                <a class="action-btn-anchor" href="https://www.google.com/maps/search/?api=1&query={top_recommendation['BeachClub'].replace(' ', '+')}+Bali" target="_blank">
                    <button class="action-btn" style="padding: 16px 32px; font-size: 1rem;">Book Winner Destination</button>
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 9. TWO COLUMN INTERACTIVE DISPLAY LAYER: MAP VS GALLERY MATRIX
# -----------------------------------------------------------------------------
layout_col1, layout_col2 = st.columns([1, 1])

with layout_col1:
    st.markdown("<div class='section-header'>Geospatial Density Mapping Analysis</div>", unsafe_allow_html=True)
    
    if not df_filtered.empty:
        # Initialize pydeck map with spatial configuration matrix
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
                        <b>Area:</b> {Area}<br/>
                        <b>DSS Recommendation Score:</b> {Score}<br/>
                        <b>Rating:</b> ⭐ {Rating}<br/>
                        <b>Minimum Spend:</b> ${Harga}<br/>
                        <b>Distance to Center:</b> {Jarak} km
                    </div>
                """,
                "style": {"backgroundColor": "transparent", "color": "white", "zIndex": "10000"}
            }
        )
        st.pydeck_chart(deck_map)
    else:
        st.info("No spatial data coordinates available to plot based on structural filter parameters.")

with layout_col2:
    st.markdown("<div class='section-header'>Airbnb-Inspired Luxury Gallery Showcase</div>", unsafe_allow_html=True)
    
    if not df_filtered.empty:
        # Create an adaptive scroll responsive grid architecture matrix
        grid_container = st.container()
        
        # Paginate or structure display rows cleanly
        row_count = int(np.ceil(len(df_filtered) / 2))
        data_idx = 0
        
        for r in range(row_count):
            g_col1, g_col2 = st.columns(2)
            
            for col in [g_col1, g_col2]:
                if data_idx < len(df_filtered):
                    row = df_filtered.iloc[data_idx]
                    
                    # Define ranking tier styles badges
                    if row['Rank'] == 1:
                        badge_cls, rank_lbl = "rank-gold", "Gold Standard"
                    elif row['Rank'] == 2:
                        badge_cls, rank_lbl = "rank-silver", "Silver Choice"
                    elif row['Rank'] == 3:
                        badge_cls, rank_lbl = "rank-bronze", "Bronze Tier"
                    else:
                        badge_cls, rank_lbl = "rank-standard", f"Rank #{row['Rank']}"
                        
                    maps_url = f"https://www.google.com/maps/search/?api=1&query={row['BeachClub'].replace(' ', '+')}+Bali"
                    
                    col.markdown(f"""
                    <div class="hotel-card">
                        <div class="hotel-img-container">
                            <img class="hotel-img" src="{row['Image']}" alt="Bali Beach Club Luxury Image"/>
                            <div class="rank-tag {badge_cls}">{rank_lbl}</div>
                            <div class="score-badge-overlay">{row['Score']}</div>
                        </div>
                        <div class="hotel-body">
                            <div class="hotel-title">{row['BeachClub']}</div>
                            <div class="hotel-location">📍 {row['Area']} • {row['Jarak']} km away</div>
                            <div class="hotel-metrics">
                                <div>
                                    <div class="metric-box-val">⭐ {row['Rating']}</div>
                                    <div class="metric-box-lbl">Rating</div>
                                </div>
                                <div>
                                    <div class="metric-box-val">${row['Harga']}</div>
                                    <div class="metric-box-lbl">Spend</div>
                                </div>
                                <div>
                                    <div class="metric-box-val">{row['Fasilitas']}</div>
                                    <div class="metric-box-lbl">Facilities</div>
                                </div>
                            </div>
                            <a class="action-btn-anchor" href="{maps_url}" target="_blank">
                                <div class="action-btn">Navigate Location ↗</div>
                            </a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    data_idx += 1
    else:
        st.info("No destinations available to populate visual cards.")

# -----------------------------------------------------------------------------
# 10. DETAILED OBJECT COMPONENT CORRELATION INTERFACE VIEW
# -----------------------------------------------------------------------------
st.markdown("<br><div class='section-header'>Deep-Dive Destinational Matrix Viewer</div>", unsafe_allow_html=True)
if not df_filtered.empty:
    selected_club_name = st.selectbox("🎯 Select a Beach Club to isolate metrics", options=df_filtered['BeachClub'].tolist())
    club_meta = df_filtered[df_filtered['BeachClub'] == selected_club_name].iloc[0]
    
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
                <h2 style="color: #fff; margin: 0 0 5px 0; font-weight:800;">{club_meta['BeachClub']} Analysis Summary</h2>
                <p style="color: #d4af37; font-size: 1.1rem; margin-bottom: 20px;">Structured Score Index: {club_meta['Score']} Points</p>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                    <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #64748b; font-size: 0.8rem; display: block; text-transform: uppercase;">Zone Area Cluster</span>
                        <strong style="font-size: 1.1rem; color: #fff;">{club_meta['Area']}</strong>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #64748b; font-size: 0.8rem; display: block; text-transform: uppercase;">User Experience Score</span>
                        <strong style="font-size: 1.1rem; color: #ffe066;">⭐ {club_meta['Rating']} / 5.0</strong>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #64748b; font-size: 0.8rem; display: block; text-transform: uppercase;">Minimum Spend Index</span>
                        <strong style="font-size: 1.1rem; color: #fff;">${club_meta['Harga']} USD</strong>
                    </div>
                    <div style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #64748b; font-size: 0.8rem; display: block; text-transform: uppercase;">Facilities Capacity Vector</span>
                        <strong style="font-size: 1.1rem; color: #fff;">{club_meta['Fasilitas']} / 100 Points</strong>
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 15px; align-items: center;">
                <span style="color: #64748b; font-size: 0.85rem;">Distance Factor: {club_meta['Jarak']} km to core city limits</span>
                <a class="action-btn-anchor" style="margin-left: auto;" href="https://www.google.com/maps/search/?api=1&query={club_meta['BeachClub'].replace(' ', '+')}+Bali" target="_blank">
                    <button class="action-btn" style="padding: 10px 24px;">Launch Google Maps Engine ↗</button>
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Select items to trigger descriptive analytics metrics details.")

# -----------------------------------------------------------------------------
# 11. ADVANCED EMPIRICAL CHARTS & COMPARATIVE VISUALIZATIONS
# -----------------------------------------------------------------------------
st.markdown("<br><div class='section-header'>Analytical Charting Workspace</div>", unsafe_allow_html=True)

if not df_filtered.empty:
    c_col1, c_col2, c_col3 = st.columns([1.2, 1, 1])
    
    with c_col1:
        st.markdown("<p style='color: #94a3b8; font-weight: 600; margin-bottom: 10px;'>DSS Calculated Rank Performance</p>", unsafe_allow_html=True)
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
            xaxis_title="Decision Engine Score",
            yaxis_title=None,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_rank, use_container_width=True)
        
    with c_col2:
        st.markdown("<p style='color: #94a3b8; font-weight: 600; margin-bottom: 10px;'>Price vs. Quality Correlation Plot</p>", unsafe_allow_html=True)
        fig_scatter = px.scatter(
            df_filtered,
            x='Harga',
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
            xaxis_title="Entry Spend ($)",
            yaxis_title="Rating Standard"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    with c_col3:
        st.markdown("<p style='color: #94a3b8; font-weight: 600; margin-bottom: 10px;'>Regional Asset Density Share</p>", unsafe_allow_html=True)
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
else:
    st.info("Insufficient active dataset options populated to plot graphics.")

# -----------------------------------------------------------------------------
# 12. ENTERPRISE EXPORT MATRIX ENGINE LAYER
# -----------------------------------------------------------------------------
st.markdown("<br><div class='section-header'>Data Offboarding Framework</div>", unsafe_allow_html=True)
st.markdown("Download full quantitative multi-criteria scoring models configured mapping parameters for analytical reference outside workspace dashboard.")

@st.cache_data
def transform_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv_data_buffer = transform_df_to_csv(df_filtered)

st.download_button(
    label="📥 Download Structured Decision Matrix (.CSV)",
    data=csv_data_buffer,
    file_name="Bali_Beach_Club_DSS_Ranks.csv",
    mime="text/csv"
)

# -----------------------------------------------------------------------------
# 13. COMPREHENSIVE PRODUCTION SYSTEM FOOTER ARCHITECTURE
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="footer-container">
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 30px;">
        <div style="max-width: 450px;">
            <h4 style="color: #fff; margin: 0 0 10px 0; font-weight: 700; font-size:1.1rem;">Villas & Waves DSS Portfolio Platform</h4>
            <p style="line-height: 1.6;">An industrial production enterprise-grade application demonstrating advanced analytical Multi-Criteria Decision Analysis (MCDA) logic mapped dynamically over stylized modern layouts mimicking premier international hospitality portals.</p>
        </div>
        <div>
            <h4 style="color: #fff; margin: 0 0 10px 0; font-weight: 700; font-size:1.1rem;">Core Technology Stack Matrix</h4>
            <p style="margin: 4px 0;">💻 Python Engine Core</p>
            <p style="margin: 4px 0;">⚡ Streamlit Micro-Framework Architecture</p>
            <p style="margin: 4px 0;">📊 Pandas & Plotly Visual Pipeline</p>
            <p style="margin: 4px 0;">🎨 Glassmorphic Custom Style Injection Layers</p>
        </div>
        <div>
            <h4 style="color: #fff; margin: 0 0 10px 0; font-weight: 700; font-size:1.1rem;">Analytical Multi-Criteria Equation</h4>
            <div style="background: rgba(255,255,255,0.03); padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); color:#ffe066; font-family: monospace;">
                Score = (Rating * 40) + (Fasilitas * 0.3) - (Harga * 0.05) - (Jarak * 0.2)
            </div>
            <p style="font-size: 0.75rem; color:#64748b; margin-top:6px;">Calibrated explicitly to maximize quality indices while dampening distance & spend overhead barriers.</p>
        </div>
    </div>
    <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.03); font-size: 0.8rem;">
        &copy; 2026 Villas & Waves Systems Enterprise Inc. Developed for Executive High-Fidelity Data Science Asset Portfolios. Open Access License.
    </div>
</div>
""", unsafe_allow_html=True)
