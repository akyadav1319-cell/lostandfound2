import streamlit as st
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from db import init_db, insert_item, fetch_all
from matcher import get_embedding

st.set_page_config(page_title="Lost & Found Portal", layout="wide")

# ---- CSS for dark theme + gradients ----
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1e293b, #4c1d95, #1e293b);
    color: white;
}
.card {
    background-color: rgba(255, 255, 255, 0.05);
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    transition: transform 0.2s;
}
.card:hover {
    transform: scale(1.02);
}
button {
    cursor: pointer;
}
h2 {
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔍 Lost & Found Portal")

# ---- Fetch items from DB ----
lost_items =init_db()
found_items = insert_item()

# ---- Columns for Lost and Found ----
col1, col2 = st.columns(2)

# ----- LOST ITEMS -----
with col1:
    st.subheader("😢 Lost Items")
    with st.form("lost_form"):
        lost_name = st.text_input("Item Name")
        lost_type = st.selectbox("Object Type", ["Laptop","Mobile","Charger","Bags","Water Bottle","Books","ID Card","Keys","Wallet","Headphones","Watch","Umbrella","Others"])
        lost_location = st.text_input("Last Seen Location")
        lost_description = st.text_area("Description")
        lost_contact = st.text_input("Contact Info")
        submit_lost = st.form_submit_button("Report Lost Item")
        if submit_lost:
            if not lost_name or not lost_type or not lost_location or not lost_contact:
                st.warning("Please fill in all required fields")
            else:
                insert_lost_item(lost_name, lost_type, lost_location, lost_description, lost_contact, datetime.now())
                st.success("Lost item reported successfully!")
                st.experimental_rerun()
    st.markdown("---")
    for item in lost_items:
        st.markdown(f"""
        <div class="card">
            <h4>{item['name']}</h4>
            <p>Type: {item['type']}</p>
            <p>Location: {item['location']}</p>
            <p>Date: {item['date']}</p>
            <p>Status: {item['status']}</p>
        </div>
        """, unsafe_allow_html=True)

# ----- FOUND ITEMS -----
with col2:
    st.subheader("🎉 Found Items")
    with st.form("found_form"):
        found_name = st.text_input("Item Name", key="found_name")
        found_type = st.selectbox("Object Type", ["Laptop","Mobile","Charger","Bags","Water Bottle","Books","ID Card","Keys","Wallet","Headphones","Watch","Umbrella","Others"], key="found_type")
        found_location = st.text_input("Found Location", key="found_location")
        found_description = st.text_area("Description", key="found_description")
        found_contact = st.text_input("Contact Info", key="found_contact")
        submit_found = st.form_submit_button("Report Found Item")
        if submit_found:
            if not found_name or not found_type or not found_location or not found_contact:
                st.warning("Please fill in all required fields")
            else:
                # Optionally, use AI verification
                verified = verify_owner(found_description, found_contact)  # replace with your AI logic
                insert_found_item(found_name, found_type, found_location, found_description, found_contact, datetime.now(), verified)
                st.success("Found item reported successfully!")
                st.experimental_rerun()
    st.markdown("---")
    for item in found_items:
        st.markdown(f"""
        <div class="card">
            <h4>{item['name']}</h4>
            <p>Type: {item['type']}</p>
            <p>Location: {item['location']}</p>
            <p>Date: {item['date']}</p>
        </div>
        """, unsafe_allow_html=True)




















