import streamlit as st
import pandas as pd
import plotly.express as px
import os
from src.ai import generate_insight

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="AI Sales Dashboard", layout="wide")

st.title("🚀 AI Sales Intelligence Dashboard")

# =====================
# LOAD DATA SAFE
# =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "sales.csv")

def load_data():
    if not os.path.exists(DATA_PATH):
        st.error("❌ Missing data/sales.csv")
        return pd.DataFrame()

    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# =====================
# DEBUG DATA (QUAN TRỌNG)
# =====================
st.subheader("📦 RAW DATA")
st.dataframe(df)

if df.empty:
    st.warning("⚠️ No data loaded")
    st.stop()

# =====================
# FILTER
# =====================
st.sidebar.title("⚙️ Filters")

filtered_df = df.copy()

if "region" in df.columns:
    region = st.sidebar.selectbox("Region", ["All"] + list(df["region"].dropna().unique()))
    if region != "All":
        filtered_df = filtered_df[filtered_df["region"] == region]

if "product" in df.columns:
    product = st.sidebar.selectbox("Product", ["All"] + list(df["product"].dropna().unique()))
    if product != "All":
        filtered_df = filtered_df[filtered_df["product"] == product]

# =====================
# DEBUG FILTERED
# =====================
st.subheader("📊 FILTERED DATA")
st.dataframe(filtered_df)

if filtered_df.empty:
    st.warning("⚠️ No data after filter")
    st.stop()

# =====================
# KPI
# =====================
st.subheader("📊 KPI")

col1, col2, col3 = st.columns(3)

sales = filtered_df["sales"].sum() if "sales" in filtered_df else 0
profit = filtered_df["profit"].sum() if "profit" in filtered_df else 0
orders = len(filtered_df)

col1.metric("💰 Sales", f"{sales:,.0f}")
col2.metric("📈 Profit", f"{profit:,.0f}")
col3.metric("🧾 Orders", orders)

# =====================
# CHART
# =====================
st.subheader("📈 Sales Trend")

if "date" in filtered_df.columns and "sales" in filtered_df.columns:
    chart = filtered_df.groupby("date")["sales"].sum().reset_index()

    if not chart.empty:
        fig = px.line(chart, x="date", y="sales", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No chart data")
else:
    st.warning("Missing date or sales column")

# =====================
# AI INSIGHT
# =====================
st.subheader("🤖 AI Insight")

if st.button("Generate Insight"):

    with st.spinner("AI analyzing..."):
        result = generate_insight(filtered_df)
        st.success("Done")
        st.write(result)
