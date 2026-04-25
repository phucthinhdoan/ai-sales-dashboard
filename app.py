import streamlit as st
import pandas as pd
import plotly.express as px
import os
from src.ai import generate_insight

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Sales Dashboard", layout="wide")

st.title("🚀 AI Sales Intelligence Dashboard")

# ---------------- LOAD DATA (SAFE) ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales.csv")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except:
        return pd.DataFrame({
            "date": [],
            "product": [],
            "region": [],
            "sales": [],
            "profit": []
        })

df = load_data()

# ---------------- DEBUG (QUAN TRỌNG) ----------------
st.subheader("📦 Raw Data")
st.dataframe(df)

# ---------------- SIDEBAR FILTER ----------------
st.sidebar.title("⚙️ Filters")

region = "All"
product = "All"

if "region" in df.columns and len(df) > 0:
    region = st.sidebar.selectbox("Region", ["All"] + list(df["region"].dropna().unique()))

if "product" in df.columns and len(df) > 0:
    product = st.sidebar.selectbox("Product", ["All"] + list(df["product"].dropna().unique()))

filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[filtered_df["region"] == region]

if product != "All":
    filtered_df = filtered_df[filtered_df["product"] == product]

# ---------------- DEBUG FILTER ----------------
st.subheader("📊 Filtered Data")
st.dataframe(filtered_df)

# ---------------- KPI ----------------
st.subheader("📊 KPI")

col1, col2, col3 = st.columns(3)

sales = filtered_df["sales"].sum() if "sales" in filtered_df.columns else 0
profit = filtered_df["profit"].sum() if "profit" in filtered_df.columns else 0
orders = len(filtered_df)

col1.metric("💰 Sales", f"{sales:,.0f}")
col2.metric("📈 Profit", f"{profit:,.0f}")
col3.metric("🧾 Orders", orders)

st.divider()

# ---------------- CHART ----------------
st.subheader("📈 Sales Trend")

if "date" in filtered_df.columns and "sales" in filtered_df.columns and len(filtered_df) > 0:
    chart = filtered_df.groupby("date")["sales"].sum().reset_index()
    fig = px.line(chart, x="date", y="sales", markers=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data for chart")

# ---------------- AI INSIGHT ----------------
st.subheader("🤖 AI Insight")

if st.button("Generate Insight"):

    if len(filtered_df) == 0:
        st.error("No data to analyze")
    else:
        with st.spinner("AI analyzing..."):
            result = generate_insight(filtered_df)
            st.success("Done")
            st.write(result)
