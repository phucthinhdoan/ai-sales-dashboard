import streamlit as st
import pandas as pd
import plotly.express as px
from src.ai import generate_insight

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="AI Sales Intelligence",
    page_icon="📊",
    layout="wide"
)

# -----------------------
# HERO SECTION (SAAS STYLE)
# -----------------------
st.markdown("""
# 🚀 AI Sales Intelligence Platform
### Turn raw data into business decisions in seconds
""")

col1, col2, col3 = st.columns(3)
col1.metric("⚡ System", "Live")
col2.metric("🧠 AI Engine", "Active")
col3.metric("📊 Mode", "SaaS Dashboard")

st.divider()

# -----------------------
# LOAD DATA
# -----------------------
@st.cache_data
def load_data():
    return pd.read_csv("sales.csv")

df = load_data()

# -----------------------
# SIDEBAR (CONTROL PANEL)
# -----------------------
st.sidebar.title("⚙️ Control Panel")

mode = st.sidebar.radio("Mode", ["📊 Dashboard", "🤖 AI Analyst"])

region = "All"
product = "All"

if "region" in df.columns:
    region = st.sidebar.selectbox("Region", ["All"] + list(df["region"].unique()))

if "product" in df.columns:
    product = st.sidebar.selectbox("Product", ["All"] + list(df["product"].unique()))

# FILTER DATA
filtered_df = df.copy()

if region != "All":
    filtered_df = filtered_df[filtered_df["region"] == region]

if product != "All":
    filtered_df = filtered_df[filtered_df["product"] == product]

# -----------------------
# MODE 1: DASHBOARD
# -----------------------
if mode == "📊 Dashboard":

    st.subheader("📊 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    sales = filtered_df["sales"].sum() if "sales" in df.columns else 0
    profit = filtered_df["profit"].sum() if "profit" in df.columns else 0
    orders = len(filtered_df)
    avg_order = sales / orders if orders else 0

    col1.metric("💰 Revenue", f"{sales:,.0f}")
    col2.metric("📈 Profit", f"{profit:,.0f}")
    col3.metric("🧾 Orders", orders)
    col4.metric("🏆 Avg Order", f"{avg_order:,.0f}")

    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 Sales Trend")

        if "date" in df.columns:
            chart = filtered_df.groupby("date")["sales"].sum().reset_index()
            fig = px.line(chart, x="date", y="sales", markers=True)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🏷 Top Products")

        if "product" in df.columns:
            top = filtered_df.groupby("product")["sales"].sum().sort_values(ascending=False).head(5)
            fig2 = px.bar(top, orientation="h")
            st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.subheader("🤖 AI Insight")

    if st.button("Generate Insight"):
        with st.spinner("Analyzing business data..."):
            insight = generate_insight(filtered_df)
            st.success("Analysis Complete")
            st.write(insight)

# -----------------------
# MODE 2: AI ANALYST CHAT
# -----------------------
elif mode == "🤖 AI Analyst":

    st.subheader("🤖 AI Business Analyst")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.text_input("Ask your business question...")

    if user_input:
        with st.spinner("Thinking like a senior analyst..."):
            response = generate_insight(filtered_df)
            st.session_state.chat.append(("You", user_input))
            st.session_state.chat.append(("AI", response))

    for role, msg in st.session_state.chat:
        if role == "You":
            st.markdown(f"🧑 **You:** {msg}")
        else:
            st.markdown(f"🤖 **AI:** {msg}")
