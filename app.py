import streamlit as st
from matcher import get_embedding
from db importimport streamlit as st
from model import get_embedding
from database import init_db, insert_item, fetch_all
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

# ---- Page Config ----
st.set_page_config(page_title="Lost & Found AI", layout="centered")
init_db()
SIMILARITY_THRESHOLD = 0.65

# ---- Red & White Theme ----
st.markdown(
    """
    <style>
    /* Background and main text */
    .stApp {
        background-color: #fff0f0;
        color: #900000;
        font-family: 'Arial', sans-serif;
    }
    /* Titles */
    .stTitle, h1, h2, h3 {
        color: #900000;
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
    /* Expander header */
    .stExpander > div:first-child {
        background-color: #ffdede;
        color: #900000;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- App Title ----
st.title("🔍 Lost & Found AI Matcher")
st.write("Smart AI system to connect lost items with their rightful owners.")

# ---- Lost Item Submission ----
with st.expander("📌 Report Lost Item", expanded=True):
    name_lost = st.text_input("Item Name", key="lost_name")
    desc_lost = st.text_area("Item Description", key="lost_desc")

    if st.button("Submit Lost Item"):
        if name_lost and desc_lost:
            embed_lost = get_embedding(desc_lost)
            insert_item("lost_items", name_lost, desc_lost, embed_lost)
            st.success("Lost item reported successfully!")

            # Auto-match with found items
            found_items = fetch_all("found_items")
            if not found_items:
                st.info("No found items in database yet.")
            else:
                st.write("### 🔎 AI Matching Results")
                for found in found_items:
                    lost_emb = np.array(embed_lost).reshape(1, -1)
                    found_emb = np.array(json.loads(found[3])).reshape(1, -1)
                    score = cosine_similarity(lost_emb, found_emb)[0][0]
                    if score > SIMILARITY_THRESHOLD:
                        st.success(f"Match Found! Lost: **{name_lost}** → Found: **{found[1]}** (Score: {score:.2f})")
                    else:
                        st.write(f"No match for Lost: **{name_lost}** with Found: **{found[1]}** yet.")

# ---- Found Item Submission ----
with st.expander("📦 Report Found Item", expanded=True):
    name_found = st.text_input("Found Item Name", key="found_name")
    desc_found = st.text_area("Found Item Description", key="found_desc")

    if st.button("Submit Found Item"):
        if name_found and desc_found:
            embed_found = get_embedding(desc_found)
            insert_item("found_items", name_found, desc_found, embed_found)
            st.success("Found item submitted successfully!")

            # Auto-match with lost items
            lost_items = fetch_all("lost_items")
            if not lost_items:
                st.info("No lost items in database yet.")
            else:
                st.write("### 🔎 AI Matching Results")
                for lost in lost_items:
                    found_emb = np.array(embed_found).reshape(1, -1)
                    lost_emb = np.array(json.loads(lost[3])).reshape(1, -1)
                    score = cosine_similarity(lost_emb, found_emb)[0][0]
                    if score > SIMILARITY_THRESHOLD:
                        st.success(f"Match Found! Lost: **{lost[1]}** → Found: **{name_found}** (Score: {score:.2f})")
                    else:
                        st.write(f"No match for Found: **{name_found}** with Lost: **{lost[1]}** yet.")






