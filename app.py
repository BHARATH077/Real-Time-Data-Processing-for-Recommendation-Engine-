import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# 1️⃣ Load processed data
# ----------------------------
purchases = pd.read_csv("data/purchases.csv")
recommendations = pd.read_csv("data/recommendations.csv") if "data/recommendations.csv" in locals() else None

st.set_page_config(page_title="Recommendation Dashboard", layout="wide")

st.title("🧠 Real-Time Recommendation Engine Dashboard")
st.markdown("Interactive dashboard displaying purchase trends and model outputs.")

# ----------------------------
# 2️⃣ Key Metrics
# ----------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Users", purchases["user_id"].nunique())
col2.metric("Total Items", purchases["item_id"].nunique())
col3.metric("Total Purchases", len(purchases))

# ----------------------------
# 3️⃣ Visualization Section
# ----------------------------
st.subheader("📊 Purchase Distribution")
st.image("visuals/purchase_amount_distribution.png")

st.subheader("🧩 User-Item Interaction Heatmap")
st.image("visuals/user_item_heatmap.png")

# ----------------------------
# 4️⃣ Recommendation Viewer
# ----------------------------
if recommendations is not None:
    st.subheader("🎯 Personalized Recommendations")
    selected_user = st.selectbox("Select User ID", recommendations["user_id"].unique())
    user_recs = recommendations[recommendations["user_id"] == selected_user]
    st.table(user_recs.head(10))
else:
    st.warning("No recommendation data found. Please run model training first.")
y
