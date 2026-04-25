import streamlit as st
import pandas as pd
import plotly.express as px
import os
from src.ai import generate_insight

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("""
# 🚀 AI Sales Intelligence Platform
### Turn raw data into business decisions using AI
""")

col1, col2, col3 = st.columns(3)
col1.metric("⚡ Status", "Live")
col2.metric("🧠 AI Engine", "Groq")
col3.metric("📊 Mode", "SaaS")

st.divider()

# ---------------- SAFE DATA LOAD ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales.csv")

@st.cache_data
def load_data():
    return pd.read_csv("sales.csv")

df = load_data()

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Control Panel")

mode = st.sidebar.radio("Mode", ["📊 Dashboard", "🤖 AI Analyst"])

region = "All"
product = "All"

if "region" in df.columns:
    region = st.sidebar.selectbox("Region", ["All"] + list(df["region"].unique()))

if "product" in df.columns:
    product = st.sidebar.selectbox("Product", ["All"] + list(df["product"].unique()))

filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[filtered_df["region"] == region]

if product != "All":
    filtered_df = filtered_df[filtered_df["product"] == product]

# ---------------- DASHBOARD MODE ----------------
if mode == "📊 Dashboard":

    st.subheader("📊 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    sales = filtered_df["sales"].sum() if "sales" in df.columns else 0
    profit = filtered_df["profit"].sum() if "profit" in df.columns else 0
    orders = len(filtered_df)
    avg = sales / orders if orders else 0

    col1.metric("💰 Revenue", f"{sales:,.0f}")
    col2.metric("📈 Profit", f"{profit:,.0f}")
    col3.metric("🧾 Orders", orders)
    col4.metric("🏆 Avg Order", f"{avg:,.0f}")

    st.divider()

    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("📈 Sales Trend")

        if "date" in df.columns:
            chart = filtered_df.groupby("date")["sales"].sum().reset_index()
            fig = px.line(chart, x="date", y="sales", markers=True)
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("🏷 Top Products")

        if "product" in df.columns:
            top = filtered_df.groupby("product")["sales"].sum().sort_values(ascending=False).head(5)
            fig2 = px.bar(top, orientation="h")
            st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("🤖 AI Insight")

    if st.button("Generate Insight"):
        with st.spinner("Analyzing..."):
            result = generate_insight(filtered_df)
            st.success("Done")
            st.write(result)

# ---------------- AI ANALYST MODE ----------------
elif mode == "🤖 AI Analyst":

    st.subheader("💬 AI Business Analyst")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("Ask anything about your data...")

    if user_input:
        with st.spinner("Thinking..."):
            answer = generate_insight(filtered_df)
            st.session_state.chat.append(("You", user_input))
            st.session_state.chat.append(("AI", answer))

    for role, msg in st.session_state.chat:
        if role == "You":
            st.markdown(f"🧑 **You:** {msg}")
        else:
            st.markdown(f"🤖 **AI:** {msg}")
