import streamlit as st
from matcher import get_embedding
from db import init_db, insert_item, fetch_all
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
import time
with st.spinner("AI is analyzing and matching... 🧠"):
    time.sleep(2)  # simulate AI computation
st.success("AI Matching Complete!")

# ---- Page config ----
st.set_page_config(page_title="Lost & Found AI", layout="wide")
init_db()
SIMILARITY_THRESHOLD = 0.65



# ---- Modern red & white CSS ----
st.markdown("""
<style>
/* Fade-in + slide-up animation */
.card {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.5s forwards;
}

.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }
.card:nth-child(4) { animation-delay: 0.4s; }
/* add more nth-child if needed */

@keyframes fadeInUp {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

body {
    background-color: #fffafa;
    font-family: 'Segoe UI', sans-serif;
    color: #900000;
}
h1, h2, h3 {
    color: #900000;
}
.card {
    background-color: white;
    border-radius: 15px;
    padding: 15px;
    margin: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    transition: transform 0.2s;
}
.card:hover {
    transform: scale(1.02);
}
.badge {
    padding: 5px 10px;
    border-radius: 12px;
    color: white;
    font-weight: bold;
    font-size: 14px;
}
.high { background-color: #28a745; }  /* green */
.medium { background-color: #ffc107; } /* yellow */
.low { background-color: #dc3545; }    /* red */
.item-img {
    width: 100%;
    height: auto;
    border-radius: 10px;
    margin-bottom: 10px;
}
.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    grid-gap: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---- App title ----
st.title("🔍 Lost & Found AI Matcher")
st.write("Smart AI system connecting lost items with their rightful owners.")

# ---- Lost Item Submission ----
with st.expander("📌 Report Lost Item", expanded=True):
    name_lost = st.text_input("Item Name", key="lost_name")
    desc_lost = st.text_area("Item Description", key="lost_desc")
    image_lost = st.file_uploader("Upload an image (optional)", type=["png","jpg","jpeg"], key="lost_img")

    if st.button("Submit Lost Item"):
        if name_lost and desc_lost:
            embed_lost = get_embedding(desc_lost)
            insert_item("lost_items", name_lost, desc_lost, embed_lost)
            st.success("Lost item reported successfully!")

            # Auto-match
            found_items = fetch_all("found_items")
            if found_items:
                st.write("### 🔎 AI Matching Results")
                cols = st.columns(len(found_items))
                for i, found in enumerate(found_items):
                    lost_emb = np.array(embed_lost).reshape(1, -1)
                    found_emb = np.array(json.loads(found[3])).reshape(1, -1)
                    score = cosine_similarity(lost_emb, found_emb)[0][0]

                    # Determine badge color
                    if score > 0.8:
                        badge = 'high'
                    elif score > 0.6:
                        badge = 'medium'
                    else:
                        badge = 'low'

                    # Display card
                    with cols[i % 3]:
                        img_html = f'<img class="item-img" src="data:image/png;base64,{image_lost.getvalue().decode("utf-8")}">' if image_lost else ""
                        st.markdown(f"""
                        <div class="card">
                            {img_html}
                            <h3>{found[1]}</h3>
                            <p>{found[2]}</p>
                            <span class="badge {badge}">Score: {score:.2f}</span>
                        </div>
                        """, unsafe_allow_html=True)

# ---- Found Item Submission ----
with st.expander("📦 Report Found Item", expanded=True):
    name_found = st.text_input("Found Item Name", key="found_name")
    desc_found = st.text_area("Found Item Description", key="found_desc")
    image_found = st.file_uploader("Upload an image (optional)", type=["png","jpg","jpeg"], key="found_img")

    if st.button("Submit Found Item"):
        if name_found and desc_found:
            embed_found = get_embedding(desc_found)
            insert_item("found_items", name_found, desc_found, embed_found)
            st.success("Found item submitted successfully!")

            # Auto-match
            lost_items = fetch_all("lost_items")
            if lost_items:
                st.write("### 🔎 AI Matching Results")
                cols = st.columns(len(lost_items))
                for i, lost in enumerate(lost_items):
                    found_emb = np.array(embed_found).reshape(1, -1)
                    lost_emb = np.array(json.loads(lost[3])).reshape(1, -1)
                    score = cosine_similarity(lost_emb, found_emb)[0][0]

                    # Determine badge color
                    if score > 0.8:
                        badge = 'high'
                    elif score > 0.6:
                        badge = 'medium'
                    else:
                        badge = 'low'

                    with cols[i % 3]:
                        img_html = f'<img class="item-img" src="data:image/png;base64,{image_found.getvalue().decode("utf-8")}">' if image_found else ""
                        st.markdown(f"""
                        <div class="card">
                            {img_html}
                            <h3>{lost[1]}</h3>
                            <p>{lost[2]}</p>
                            <span class="badge {badge}">Score: {score:.2f}</span>
                        </div>
                        """, unsafe_allow_html=True)













