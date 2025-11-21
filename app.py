import streamlit as st
from matcher import get_embedding
from db import init_db, insert_item, fetch_all
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Lost & Found AI", layout="wide")
init_db()
SIMILARITY_THRESHOLD = 0.65

# ---- Custom CSS ----
st.markdown("""
<style>
/* General background */
.stApp {
    background-color: #fff8f8;
    color: #900000;
    font-family: 'Arial', sans-serif;
}
/* Card style */
.card {
    background-color: white;
    padding: 15px;
    margin: 10px 0;
    border-radius: 15px;
    border: 2px solid #900000;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
}
/* Buttons */
div.stButton > button:first-child {
    background-color: #900000;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🔍 Lost & Found AI Matcher")
st.write("Smart AI system connecting lost items with their rightful owners.")

# ---- Report Lost Item ----
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
                for found in found_items:
                    lost_emb = np.array(embed_lost).reshape(1, -1)
                    found_emb = np.array(json.loads(found[3])).reshape(1, -1)
                    score = cosine_similarity(lost_emb, found_emb)[0][0]

                    # Display card
                    st.markdown(f"""
                    <div class="card">
                        <h3>{found[1]}</h3>
                        <p>{found[2]}</p>
                        <p>🧠 Match Score: {score:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)

# ---- Report Found Item ----
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
                for lost in lost_items:
                    found_emb = np.array(embed_found).reshape(1, -1)
                    lost_emb = np.array(json.loads(lost[3])).reshape(1, -1)
                    score = cosine_similarity(lost_emb, found_emb)[0][0]

                    st.markdown(f"""
                    <div class="card">
                        <h3>{lost[1]}</h3>
                        <p>{lost[2]}</p>
                        <p>🧠 Match Score: {score:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)








