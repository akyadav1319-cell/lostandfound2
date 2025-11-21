import streamlit as st
from matcher import get_embedding
from db import init_db, insert_item, fetch_all
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

# ---- Page config ----
st.set_page_config(page_title="Lost & Found AI", layout="wide")
init_db()
SIMILARITY_THRESHOLD = 0.65

# ---- Modern Thapar/Portal CSS ----
st.markdown("""
<style>
body {
    background: radial-gradient(circle, #25253a 60%, #181820 100%);
    font-family: 'Segoe UI', sans-serif;
}
.header {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 20px 0 10px 0;
    margin-bottom: 10px;
}
.logo {
    background: #C91120;
    color: #fff;
    font-weight:700;
    font-size: 1.1rem;
    border-radius:50%;
    width: 52px;
    height: 52px;
    display: flex; justify-content: center; align-items:center;
    margin-right:15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.title-block h1 {
    color: #fff;
    font-size:2.2rem;
    font-weight:800;
    margin-bottom: 2px; margin-top:2px;
}
.title-block .subtitle {
    color:#b9b9d9;
    font-size:1.07rem;
    margin-top:-5px;
}

.top-actions {
    margin-left:auto;
    display:flex; gap:15px;
}

.icon-btn {
    background: #222;
    color:#fff;
    border-radius:100%;
    width:40px; height:40px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.2rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07);
    cursor:pointer;
    border: none;
}

.section-title {
    color:#fff;
    font-size:1.8rem;
    font-weight:bold;
    margin-bottom:16px;
    margin-top:22px;
}
.card-slot {
    background:#232336;
    border-radius:15px;
    box-shadow:0 2px 20px rgba(60, 0, 0, 0.13);
    padding:38px 25px 38px 25px;
    margin-bottom:30px;
    min-height:72px;
    display:flex; align-items:center; justify-content:center;
    position:relative;
}

.fab {
    position:absolute;
    right:30px; top:50%;
    transform:translateY(-50%);
    width:46px; height:46px;
    background:#C91120;
    color:#fff; border:none;
    border-radius:50%;
    font-size:2.1rem;
    box-shadow:0 2px 8px rgba(201,17,32,0.11);
    display:flex; align-items:center; justify-content:center;
    cursor:pointer;
    transition: background .2s;
    z-index:1;
}
.fab:hover { background:#FF3B43; }

.card {
    background:#262641;
    border-radius:14px;
    padding:22px 19px 17px 19px;
    margin-bottom:16px;
    color:#fff;
    box-shadow: 0 4px 15px rgba(0,0,0,0.09);
    transition: transform 0.2s;
}
.card:hover, .card:focus {
    transform: scale(1.018);
}
.badge {
    padding: 5px 12px;
    border-radius: 12px;
    color: white;
    font-weight: 600;
    font-size: 14px;
    margin-top:6px;display:inline-block;
}
.high { background-color: #28a745; }
.medium { background-color: #ffc107; color: #333; }
.low { background-color: #dc3545; }
.item-img {
    width: 100%;
    height: auto;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---- Top Bar ----
st.markdown("""
<div class="header">
    <div class="logo">TU</div>
    <div class="title-block">
        <h1>LOST and FOUND</h1>
        <div class="subtitle">Thapar University Portal</div>
    </div>
    <div class="top-actions">
        <div style="background:#333;color:#fff;border-radius:8px;padding:7px 24px;">abist_be25</div>
        <button class="icon-btn" title="Notifications"><span style="font-size:1.25rem;">🔔</span></button>
        <button class="icon-btn" title="Settings"><span style="font-size:1.15rem;">⚙️</span></button>
        <button class="icon-btn" title="Logout"><span style="font-size:1.1rem;">⤴️</span></button>
    </div>
</div>
""", unsafe_allow_html=True)

lost_items = fetch_all("lost_items") if fetch_all("lost_items") else []
found_items = fetch_all("found_items") if fetch_all("found_items") else []
show_lost_form = st.session_state.get("show_lost_form", False)
show_found_form = st.session_state.get("show_found_form", False)

# --- Lost Items Section ---
col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<div class="section-title">Lost Items</div>', unsafe_allow_html=True)
    if not lost_items:
        st.markdown(f"""
            <div class="card-slot">
                <div style="width:100%;text-align:center;font-size:1.2rem;color:#d9d9e7;">
                No lost items yet
                </div>
                <button class="fab" onclick="window.location.href='#lost-form'">+</button>
            </div>
        """, unsafe_allow_html=True)
    else:
        for item in lost_items:
            st.markdown(f"""
<div>
    <h3>{item[1]}</h3>
    <p>{item[2]}</p>
    <span class="badge {badge}">Score: {score:.2f}</span>
</div>
""", unsafe_allow_html=True)
















