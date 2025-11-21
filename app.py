import streamlit as st
from matcher import get_embedding
from db import init_db, insert_item, fetch_all
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity

# --- IMPORT YOUR AI AND DATABASE FUNCTIONS ---
# from ai_module import process_item_description
# from db_module import add_lost_item, add_found_item, get_lost_items, get_found_items

# --- PAGE CONFIG ---
st.set_page_config(page_title="Lost & Found Portal", layout="wide")

# --- SESSION STATE ---
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "show_lost_modal" not in st.session_state:
    st.session_state.show_lost_modal = False
if "show_found_modal" not in st.session_state:
    st.session_state.show_found_modal = False

# --- THEME COLORS ---
def theme_colors():
    if st.session_state.theme == "dark":
        return {
            "bg": "#1e1e2f",
            "card_bg": "rgba(255,255,255,0.05)",
            "text": "#ffffff",
            "button": "linear-gradient(90deg, #f87171, #ec4899)"
        }
    else:
        return {
            "bg": "#f8fafc",
            "card_bg": "rgba(255,255,255,0.8)",
            "text": "#1f2937",
            "button": "linear-gradient(90deg, #34d399, #10b981)"
        }
colors = theme_colors()

# --- HEADER & THEME TOGGLE ---
st.markdown(
    f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
        <h1 style="color:{colors['text']};">🔍 Lost & Found Portal</h1>
    </div>
    """, unsafe_allow_html=True
)

if st.button("Toggle Theme"):
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
    st.experimental_rerun()

# --- FETCH DATA FROM DATABASE ---
# lost_items = get_lost_items()
# found_items = get_found_items()

# Sample demo data for design/testing
lost_items = [
    {"id": 1, "name": "Blue Backpack", "type": "Bags", "location": "Library", "date": "2024-11-20", "status": "lost"},
    {"id": 2, "name": "iPhone 13", "type": "Mobile", "location": "Cafeteria", "date": "2024-11-19", "status": "found"}
]
found_items = [
    {"id": 3, "name": "MacBook Pro", "type": "Laptop", "location": "Lab 201", "date": "2024-11-21"},
    {"id": 4, "name": "Black Wallet", "type": "Others", "location": "Gym", "date": "2024-11-20"}
]

# --- LAYOUT ---
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"<h2 style='color:{colors['text']}'>😢 Lost Items</h2>", unsafe_allow_html=True)
    if st.button("+ Report Lost Item"):
        st.session_state.show_lost_modal = True

    for item in lost_items:
        st.markdown(
            f"""
            <div style='background:{colors['card_bg']}; padding:15px; border-radius:12px; margin-bottom:10px;'>
                <b style='color:{colors['text']}'>{item['name']}</b><br>
                <small style='color:{colors['text']}; opacity:0.7'>Type: {item['type']}</small><br>
                <small style='color:{colors['text']}; opacity:0.7'>Location: {item['location']}</small><br>
                <small style='color:{colors['text']}; opacity:0.7'>Date: {item['date']}</small><br>
                {"<span style='color:#34d399;'>Found! ✨</span>" if item.get("status") == "found" else ""}
            </div>
            """, unsafe_allow_html=True
        )

with col2:
    st.markdown(f"<h2 style='color:{colors['text']}'>🎉 Found Items</h2>", unsafe_allow_html=True)
    if st.button("+ Report Found Item"):
        st.session_state.show_found_modal = True

    for item in found_items:
        st.markdown(
            f"""
            <div style='background:{colors['card_bg']}; padding:15px; border-radius:12px; margin-bottom:10px;'>
                <b style='color:{colors['text']}'>{item['name']}</b><br>
                <small style='color:{colors['text']}; opacity:0.7'>Type: {item['type']}</small><br>
                <small style='color:{colors['text']}; opacity:0.7'>Location: {item['location']}</small><br>
                <small style='color:{colors['text']}; opacity:0.7'>Date: {item['date']}</small><br>
            </div>
            """, unsafe_allow_html=True
        )

# --- LOST ITEM MODAL ---
if st.session_state.show_lost_modal:
    with st.expander("Report Lost Item", expanded=True):
        name = st.text_input("Item Name")
        type_ = st.selectbox("Type", ["Laptop", "Mobile", "Charger", "Bags", "Water Bottle", "Books", "ID Card", "Keys", "Wallet", "Headphones", "Watch", "Umbrella", "Others"])
        location = st.text_input("Last Seen Location")
        description = st.text_area("Description")
        contact = st.text_input("Contact Info")
        if st.button("Submit Lost Item"):
            # add_lost_item(name, type_, location, description, contact)
            # ai_result = process_item_description(description)
            st.success("Lost item submitted successfully!")
            st.session_state.show_lost_modal = False
            st.experimental_rerun()

# --- FOUND ITEM MODAL ---
if st.session_state.show_found_modal:
    with st.expander("Report Found Item", expanded=True):
        name = st.text_input("Item Name", key="found_name")
        type_ = st.selectbox("Type", ["Laptop", "Mobile", "Charger", "Bags", "Water Bottle", "Books", "ID Card", "Keys", "Wallet", "Headphones", "Watch", "Umbrella", "Others"], key="found_type")
        location = st.text_input("Found Location", key="found_loc")
        description = st.text_area("Description", key="found_desc")
        contact = st.text_input("Contact Info", key="found_contact")
        if st.button("Submit Found Item", key="submit_found"):
            # add_found_item(name, type_, location, description, contact)
            # ai_result = process_item_description(description)
            st.success("Found item submitted successfully!")
            st.session_state.show_found_modal = False
            st.experimental_rerun()












