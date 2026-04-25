import streamlit as st
import matplotlib.pyplot as plt

from src.data import load_data, clean_data
from src.analysis import compute_kpis, monthly_trend, top_products
from src.ai import generate_insight

st.set_page_config(page_title="AI Sales Dashboard", layout="wide")

st.title("🚀 AI Sales Analytics Dashboard")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = load_data(uploaded_file)
    df = clean_data(df)

    # KPI
    kpis = compute_kpis(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Profit", f"{kpis['Total Profit']:,.0f}")
    col2.metric("Avg Profit", f"{kpis['Avg Profit']:,.0f}")
    col3.metric("Orders", kpis["Orders"])

    # Filter
    country = st.selectbox("Select Country", df["Country"].unique())
    df = df[df["Country"] == country]

    # Trend
    trend = monthly_trend(df)

    st.subheader("📈 Monthly Trend")
    fig, ax = plt.subplots()
    ax.plot(trend["Month"], trend["Total Profit"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Top products
    st.subheader("🏆 Top Products")
    st.write(top_products(df))

    # AI Button
    if st.button("🤖 Generate AI Insights"):
        with st.spinner("Thinking..."):
            insight = generate_insight(df)
            st.write(insight)