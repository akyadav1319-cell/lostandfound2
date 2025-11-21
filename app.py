import streamlit as st
from matcher import get_embedding
from db import init_db, insert_item, fetch_all
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Lost & Found AI", layout="centered")
st.title("🔍 Lost & Found AI System")

init_db()

st.write("A smart system that connects lost items with founders using AI similarity scoring.")

with st.expander("📌 Report Lost Item"):
    name = st.text_input("Item Name")
    desc = st.text_area("Describe the Item")

    if st.button("Submit Lost Item"):
        if name and desc:
            embed = get_embedding(desc)
            insert_item("lost_items", name, desc, embed)
            st.success("Lost item reported successfully!")

with st.expander("📦 Report Found Item"):
    name2 = st.text_input("Found Item Name")
    desc2 = st.text_area("Describe the Found Item")

    if st.button("Submit Found Item"):
        if name2 and desc2:
            embed2 = get_embedding(desc2)
            insert_item("found_items", name2, desc2, embed2)
            st.success("Found item submitted successfully!")

with st.expander("🎯 AI Match Finder"):
    lost_items = fetch_all("lost_items")
    found_items = fetch_all("found_items")

    if st.button("Run Matching"):
        if not lost_items or not found_items:
            st.warning("Need lost and found item entries first!")
        else:
            for lost in lost_items:
                lost_emb = np.array(json.loads(lost[3])).reshape(1, -1)
                best_match = None
                best_score = 0

                for found in found_items:
                    found_emb = np.array(json.loads(found[3])).reshape(1, -1)
                    score = cosine_similarity(lost_emb, found_emb)[0][0]

                    if score > best_score:
                        best_match = found
                        best_score = score
                
                if best_score > 0.65:
                    st.success(f"Match Found! 🎉\nLost: **{lost[1]}** → Found: **{best_match[1]}** (Score: `{best_score:.2f}`)")
                else:
                    st.write(f"No valid match found yet for: **{lost[1]}**")




