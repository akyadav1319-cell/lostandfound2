import streamlit as st
from model import get_embedding
from database import init_db, insert_item, fetch_all
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

st.set_page_config(page_title="Lost & Found AI", layout="centered")

init_db()

st.title("🔍 Lost & Found with AI Matching")
st.write("Smart system to help connect lost items with their rightful owners.")


# ---- POPUPS ----
with st.expander("📌 Report Lost Item"):
    name = st.text_input("Item Name")
    desc = st.text_area("Item Description")

    if st.button("Submit Lost Item"):
        if name and desc:
            embed = get_embedding(desc)
            insert_item("lost_items", name, desc, embed)
            st.success("Lost item reported successfully.")


with st.expander("📦 Report Found Item"):
    name2 = st.text_input("Found Item Name")
    desc2 = st.text_area("Found Item Description")

    if st.button("Submit Found Item"):
        if name2 and desc2:
            embed2 = get_embedding(desc2)
            insert_item("found_items", name2, desc2, embed2)
            st.success("Found item submitted successfully.")


with st.expander("🎯 View Matches (AI Powered)"):
    lost_items = fetch_all("lost_items")
    found_items = fetch_all("found_items")

    if st.button("Run Matching"):
        if not lost_items or not found_items:
            st.warning("Not enough data to match.")
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
                
                if best_score > 0.60:  # threshold
                    st.success(f"Match Found!  
                               **Lost item:** {lost[1]}  
                               **Found item:** {best_match[1]}  
                               🧠 AI Match Score: `{best_score:.2f}`")
                else:
                    st.write(f"❌ No match found for: **{lost[1]}** yet.")
