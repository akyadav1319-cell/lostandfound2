import streamlit as st
from matcher import get_embedding
from db import init_db, insert_item, fetch_all
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
import base64

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="TIET Lost & Found", layout="wide")

init_db()

# ---------------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------------
st.markdown("""
<style>

body {
    background: #fff7f7;
    font-family: 'Segoe UI', sans-serif;
}

.header {
    display: flex;
    align-items: center;
    padding: 15px 0;
}

.logo {
    background:#8b0015;
    color:white;
    padding:10px 16px;
    border-radius:12px;
    font-weight:700;
    font-size:18px;
    margin-right:12px;
}

.title {
    font-size:28px;
    font-weight:600;
    color:#8b0015;
}

.box-container {
    display:flex;
    justify-content:center;
    margin-top:40px;
    gap:50px;
}

.big-box {
    width:350px;
    height:220px;
    border-radius:25px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    cursor:pointer;
    font-size:28px;
    font-weight:600;
    transition:0.25s;
    box-shadow:0 4px 20px rgba(0,0,0,0.15);
}

.big-box:hover {
    transform:scale(1.03);
}

.red-box {
    background: #ffe1e1;
    color:#900000;
}

.green-box {
    background:#e4ffee;
    color:#065f28;
}

.modal {
    background:white;
    padding:30px;
    border-radius:20px;
    width:500px;
    margin:auto;
    box-shadow:0 5px 25px rgba(0,0,0,0.3);
}

input, textarea {
    border-radius:10px !important;
}

.submit-btn {
    width:100%;
    padding:12px;
    border-radius:12px;
    font-size:18px;
    font-weight:600;
    color:white;
    border:none;
}

.red-btn {
    background:#d40000;
}

.green-btn {
    background:#009944;
}

.card {
    background:white;
    border-radius:18px;
    padding:15px;
    margin:10px;
    box-shadow:0 4px 15px rgba(0,0,0,0.15);
}

.badge {
    padding:6px 12px;
    border-radius:10px;
    color:white;
    font-weight:600;
}

.high {background:#28a745;}
.medium {background:#ffc107;color:black;}
.low {background:#dc3545;}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown("""
<div class="header">
    <div class="logo">TI</div>
    <div class="title">TIET Lost & Found</div>
</div>
""", unsafe_allow_html=True)

st.write("---")

# ---------------------------------------------------------
# BIG BUTTONS
# ---------------------------------------------------------

left, right = st.columns(2)

with left:
    lost_clicked = st.button("❓ Lost", key="lost_main_btn",
                             help="Report a lost item",
                             use_container_width=True)

with right:
    found_clicked = st.button("✔️ Found", key="found_main_btn",
                              help="Report a found item",
                              use_container_width=True)

# ---------------------------------------------------------
# LOST ITEM MODAL
# ---------------------------------------------------------
if lost_clicked:
    with st.container():
        st.markdown('<div class="modal">', unsafe_allow_html=True)

        st.markdown("## Report Lost Item")

        lost_name = st.text_input("Item Title", placeholder="e.g. Blue Casio Calculator")
        lost_cat = st.selectbox("Category", ["Electronics", "Clothing", "Books", "Accessories"])
        lost_loc = st.text_input("Location", placeholder="e.g. G-Block")
        lost_desc = st.text_area("Description", placeholder="Provide details like color, brand, scratches…")
        lost_img = st.file_uploader("Upload Image (optional)", type=["png", "jpg", "jpeg"])

        if st.button("Post Lost Item", key="lost_submit_modal"):
            if lost_name and lost_desc:
                emb = get_embedding(lost_desc)
                insert_item("lost_items", lost_name, lost_desc, emb)
                st.success("Lost item posted!")

                # ---------- AUTO MATCH ----------
                matches = fetch_all("found_items")
                if matches:

                    st.subheader("🔎 Matching Found Items")
                    cols = st.columns(3)

                    for i, row in enumerate(matches):
                        found_emb = np.array(json.loads(row[3])).reshape(1, -1)
                        score = cosine_similarity(
                            np.array(emb).reshape(1, -1),
                            found_emb
                        )[0][0]

                        badge = "high" if score > 0.8 else "medium" if score > 0.6 else "low"

                        with cols[i % 3]:
                            st.markdown(f"""
                            <div class="card">
                                <h4>{row[1]}</h4>
                                <p>{row[2]}</p>
                                <span class="badge {badge}">Score: {score:.2f}</span>
                            </div>
                            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# FOUND ITEM MODAL
# ---------------------------------------------------------
if found_clicked:
    with st.container():
        st.markdown('<div class="modal">', unsafe_allow_html=True)

        st.markdown("## Report Found Item")

        found_name = st.text_input("Found Item Title", placeholder="e.g. Black Hoodie")
        found_cat = st.selectbox("Category", ["Electronics", "Clothing", "Books", "Accessories"])
        found_loc = st.text_input("Location", placeholder="e.g. G-Block")
        found_desc = st.text_area("Description", placeholder="Provide details like color, brand, scratches…")
        found_img = st.file_uploader("Upload Image (optional)", type=["png", "jpg", "jpeg"])

        if st.button("Post Found Item", key="found_submit_modal"):
            if found_name and found_desc:
                emb = get_embedding(found_desc)
                insert_item("found_items", found_name, found_desc, emb)
                st.success("Found item submitted!")

                # ---------- AUTO MATCH ----------
                matches = fetch_all("lost_items")
                if matches:

                    st.subheader("🔎 Matching Lost Items")
                    cols = st.columns(3)

                    for i, row in enumerate(matches):
                        lost_emb = np.array(json.loads(row[3])).reshape(1, -1)
                        score = cosine_similarity(
                            np.array(emb).reshape(1, -1),
                            lost_emb
                        )[0][0]

                        badge = "high" if score > 0.8 else "medium" if score > 0.6 else "low"

                        with cols[i % 3]:
                            st.markdown(f"""
                            <div class="card">
                                <h4>{row[1]}</h4>
                                <p>{row[2]}</p>
                                <span class="badge {badge}">Score: {score:.2f}</span>
                            </div>
                            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)



















