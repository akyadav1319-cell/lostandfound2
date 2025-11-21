import streamlit as st
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from database import init_db, insert_item, fetch_all
from model import get_embedding

# ----- Setup -----
st.set_page_config(page_title="Lost & Found AI", layout="wide")
init_db()

# Theme colors similar to React code
bg_color = "#1a1a2e"
card_bg = "#162447"
accent_color = "#e43f5a"
text_color = "#ffffff"
success_color = "#28a745"

st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
    color: {text_color};
}}
.card {{
    background-color: {card_bg};
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    transition: transform 0.2s;
}}
.card:hover {{
    transform: scale(1.02);
}}
.button {{
    background-color: {accent_color};
    color: white;
    padding: 10px 15px;
    border-radius: 10px;
    font-weight: bold;
}}
</style>
""", unsafe_allow_html=True)

st.title("🔍 Lost & Found Portal")

# ----- Lost Item Submission -----
with st.expander("Report Lost Item"):
    lost_name = st.text_input("Item Name")
    lost_type = st.selectbox("Item Type", ["Laptop","Mobile","Bags","Books","Wallet","Keys","Others"])
    lost_location = st.text_input("Last Seen Location")
    lost_desc = st.text_area("Description")
    lost_contact = st.text_input("Contact Info")
    
    if st.button("Submit Lost Item"):
        if lost_name and lost_type and lost_location and lost_desc:
            lost_emb = get_embedding(lost_desc)
            insert_item("lost_items", lost_name, lost_desc, lost_emb.tolist(), lost_type, lost_location, lost_contact)
            st.success("Lost item reported successfully!")

# ----- Found Item Submission -----
with st.expander("Report Found Item"):
    found_name = st.text_input("Found Item Name")
    found_type = st.selectbox("Item Type Found", ["Laptop","Mobile","Bags","Books","Wallet","Keys","Others"])
    found_location = st.text_input("Found Location")
    found_desc = st.text_area("Description")
    found_contact = st.text_input("Contact Info")
    
    if st.button("Submit Found Item"):
        if found_name and found_type and found_location and found_desc:
            found_emb = get_embedding(found_desc)
            insert_item("found_items", found_name, found_desc, found_emb.tolist(), found_type, found_location, found_contact)
            st.success("Found item reported successfully!")

# ----- View Matches -----
st.subheader("🎯 AI Matches")
lost_items = fetch_all("lost_items")
found_items = fetch_all("found_items")

if lost_items and found_items:
    for lost in lost_items:
        lost_emb = np.array(json.loads(lost[3])).reshape(1,-1)  # embedding stored as JSON
        best_match = None
        best_score = 0
        
        for found in found_items:
            found_emb = np.array(json.loads(found[3])).reshape(1,-1)
            score = cosine_similarity(lost_emb, found_emb)[0][0]
            if score > best_score:
                best_score = score
                best_match = found
        
        if best_score > 0.6:
            st.markdown(f"""
            <div class="card">
            <strong>Lost Item:</strong> {lost[1]}<br>
            <strong>Found Item:</strong> {best_match[1]}<br>
            <strong>AI Match Score:</strong> {best_score:.2f}
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("No lost or found items available yet.")









