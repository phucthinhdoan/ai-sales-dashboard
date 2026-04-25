import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =====================
# IMPORT AI (Safe handling)
# =====================
try:
    from src.ai import generate_insight
except ImportError:
    # Fallback function if src/ai.py is missing or throws an error
    def generate_insight(df):
        return "⚠️ AI module in src/ai.py is not properly configured."

# =====================
# PAGE CONFIGURATION
# =====================
st.set_page_config(page_title="AI Sales Dashboard", layout="wide")
st.title("🚀 AI Sales Intelligence Dashboard")

# =====================
# FILE PATH (Updated based on your GitHub structure)
# =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "sales.csv") 

@st.cache_data 
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"❌ File not found: {DATA_PATH}")
        return pd.DataFrame()

    # Read data
    df = pd.read_csv(DATA_PATH)
    
    # 1. Normalize: Strip whitespace and convert to lowercase
    df.columns = df.columns.str.strip().str.lower() 
    
    # 2. RENAME COLUMNS (Crucial - based on your actual data structure)
    # Map actual column names from your CSV to the names used in the dashboard code
    mapping = {
        "order date": "date",
        "total revenue": "sales",
        "total profit": "profit"
    }
    df.rename(columns=mapping, inplace=True)
    
    # 3. Process date format
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors='coerce')
    
    # 4. Convert Sales and Profit to numeric (remove special characters if any)
    for col in ["sales", "profit"]:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    return df

df = load_data()

# =====================
# DEBUG DATA
# =====================
st.subheader("📦 RAW DATA")
st.dataframe(df.head(20)) # Show first 20 rows

if df.empty:
    st.warning("⚠️ Data is empty or sales.csv not found")
    st.stop()

# =====================
# SIDEBAR FILTERS
# =====================
st.sidebar.title("⚙️ Filters")

filtered_df = df.copy()

# Filter by Region
if "region" in df.columns:
    regions = ["All"] + sorted(list(df["region"].dropna().unique()))
    selected_region = st.sidebar.selectbox("Select Region", regions)
    if selected_region != "All":
        filtered_df = filtered_df[filtered_df["region"] == selected_region]

# Filter by Item Type
item_col = "item type" if "item type" in df.columns else "product"
if item_col in df.columns:
    items = ["All"] + sorted(list(df[item_col].dropna().unique()))
    selected_item = st.sidebar.selectbox("Select Product", items)
    if selected_item != "All":
        filtered_df = filtered_df[filtered_df[item_col] == selected_item]

# =====================
# DISPLAY KPI
# =====================
st.subheader("📊 Key Metrics (KPI)")

col1, col2, col3 = st.columns(3)

# Calculate metrics
total_sales = filtered_df["sales"].sum() if "sales" in filtered_df.columns else 0
total_profit = filtered_df["profit"].sum() if "profit" in filtered_df.columns else 0
total_orders = len(filtered_df)

col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("🧾 Total Orders", f"{total_orders:,}")

# =====================
# SALES TREND CHART
# =====================
st.subheader("📈 Sales Trend")

if "date" in filtered_df.columns and "sales" in filtered_df.columns:
    # Group by date for plotting
    trend_data = filtered_df.groupby("date")["sales"].sum().reset_index().sort_values("date")

    if not trend_data.empty:
        fig = px.line(trend_data, x="date", y="sales", 
                     title="Sales Over Time",
                     markers=True,
                     line_shape="linear")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No time data available to draw the chart.")
else:
    st.error("Warning: Missing 'order date' or 'total revenue' columns for the trend chart.")

# =====================
# AI INSIGHT
# =====================
st.subheader("🤖 AI Insight")

if st.button("Generate AI Insight"):
    with st.spinner("AI is analyzing data..."):
        # Send filtered data to AI
        result = generate_insight(filtered_df)
        st.success("Done")
        st.markdown(f"--- \n {result}")
