import streamlit as st
from matcher import get_embedding
from db import init_db, insert_item, fetch_all
import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
import base64

# ---- Page config ----
st.set_page_config(page_title="Lost & Found AI", layout="wide")
init_db()

# ---- CSS ----
st.markdown("""
<style>
body {background-color: #fffafa; font-family: 'Segoe UI', sans-serif; color: #900000;}
h1, h2, h3 {color: #900000;}
.card {background-color: white; border-radius: 15px; padding: 15px; margin: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); transition: transform 0.2s;}
.card:hover {transform: scale(1.02);}
.badge {padding: 5px 10px; border-radius: 12px; color: white; font-weight: bold; font-size: 14px;}
.high { background-color: #28a745; }  
.medium { background-color: #ffc107; } 
.low { background-color: #dc3545; }    
.item-img {width: 100%; height: auto; border-radius: 10px; margin-bottom: 10px;}
.grid-container {display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); grid-gap: 20px;}
</style>
""", unsafe_allow_html=True)

st.title("🔍 Lost & Found AI Matcher")
st.write("Smart AI system connecting lost items with their rightful owners.")

# ---- Lost Item Submission ----
with st.expander("📌 Report Lost Item", expanded=True):
    lost_name = st.text_input("Item Name", key="lost_name_input")
    lost_desc = st.text_area("Item Description", key="lost_desc_input")
    lost_image = st.file_uploader("Upload an image (optional)", type=["png","jpg","jpeg"], key="lost_image_input")

    if st.button("Submit Lost Item", key="lost_submit"):
        if lost_name and lost_desc:
            embed_lost = get_embedding(lost_desc)
            insert_item("lost_items", lost_name, lost_desc, embed_lost)
            st.success("Lost item reported successfully!")

            # Auto-match
            found_items = fetch_all("found_items")
            if found_items:
                st.write("### 🔎 AI Matching Results")
                cols = st.columns(min(3, len(found_items)))
                for i, found in enumerate(found_items):
                    lost_emb = np.array(embed_lost).reshape(1, -1)
                    found_emb = np.array(json.loads(found[3])).reshape(1, -1)
                    score = cosine_similarity(lost_emb, found_emb)[0][0]

                    badge = 'high' if score > 0.8 else 'medium' if score > 0.6 else 'low'
                    img_html = f'<img class="item-img" src="data:image/png;base64,{base64.b64encode(lost_image.getvalue()).decode("utf-8")}">' if lost_image else ""
                    
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div class="card">{img_html}
                            <h3>{found[1]}</h3>
                            <p>{found[2]}</p>
                            <span class="badge {badge}">Score: {score:.2f}</span>
                        </div>
                        """, unsafe_allow_html=True)

# ---- Found Item Submission ----
with st.expander("📦 Report Found Item", expanded=True):
    found_name = st.text_input("Found Item Name", key="found_name_input")
    found_desc = st.text_area("Found Item Description", key="found_desc_input")
    found_image = st.file_uploader("Upload an image (optional)", type=["png","jpg","jpeg"], key="found_image_input")

    if st.button("Submit Found Item", key="found_submit"):
        if found_name and found_desc:
            embed_found = get_embedding(found_desc)
            insert_item("found_items", found_name, found_desc, embed_found)
            st.success("Found item submitted successfully!")

            # Auto-match
            lost_items = fetch_all("lost_items")
            if lost_items:
                st.write("### 🔎 AI Matching Results")
                cols = st.columns(min(3, len(lost_items)))
                for i, lost in enumerate(lost_items):
                    found_emb = np.array(embed_found).reshape(1, -1)
                    lost_emb = np.array(json.loads(lost[3])).reshape(1, -1)
                    score = cosine_similarity(lost_emb, found_emb)[0][0]

                    badge = 'high' if score > 0.8 else 'medium' if score > 0.6 else 'low'
                    img_html = f'<img class="item-img" src="data:image/png;base64,{base64.b64encode(found_image.getvalue()).decode("utf-8")}">' if found_image else ""
                    
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div class="card">{img_html}
                            <h3>{lost[1]}</h3>
                            <p>{lost[2]}</p>
                            <span class="badge {badge}">Score: {score:.2f}</span>
                        </div>
                        """, unsafe_allow_html=True)




















