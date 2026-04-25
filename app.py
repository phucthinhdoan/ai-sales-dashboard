import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =====================
# AI MODULE IMPORT
# =====================
try:
    from src.ai import generate_insight
except ImportError:
    def generate_insight(df, msg):
        return "⚠️ Module src/ai.py not found."

# =====================
# PAGE CONFIGURATION
# =====================
st.set_page_config(page_title="AI Sales Dashboard", layout="wide")
st.title("🚀 AI Sales Intelligence Dashboard")

# =====================
# DATA LOADING (Safe Handling)
# =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "sales.csv") 

@st.cache_data 
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"❌ File not found: {DATA_PATH}")
        return pd.DataFrame()

    df = pd.read_csv(DATA_PATH)
    
    # 1. Column Normalization
    df.columns = df.columns.str.strip().str.lower() 
    
    # 2. Column Renaming for Logic Consistency
    mapping = {
        "order date": "date",
        "total revenue": "sales",
        "total profit": "profit"
    }
    df.rename(columns=mapping, inplace=True)
    
    # 3. Data Type Casting
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors='coerce')
    
    for col in ["sales", "profit"]:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    return df

df = load_data()

# =====================
# DATA VALIDATION
# =====================
with st.expander("📦 VIEW RAW DATA (Click to expand)"):
    st.dataframe(df.head(50))

if df.empty:
    st.warning("⚠️ Data is empty, please check your sales.csv file.")
    st.stop()

# =====================
# SIDEBAR FILTERS
# =====================
st.sidebar.title("⚙️ Filters")

filtered_df = df.copy()

if "region" in df.columns:
    regions = ["All"] + sorted(list(df["region"].dropna().unique()))
    selected_region = st.sidebar.selectbox("Select Region", regions)
    if selected_region != "All":
        filtered_df = filtered_df[filtered_df["region"] == selected_region]

item_col = "item type" if "item type" in df.columns else "product"
if item_col in df.columns:
    items = ["All"] + sorted(list(df[item_col].dropna().unique()))
    selected_item = st.sidebar.selectbox("Select Product", items)
    if selected_item != "All":
        filtered_df = filtered_df[filtered_df[item_col] == selected_item]

# =====================
# KPI & CHARTS
# =====================
st.subheader("📊 Key Performance Indicators (KPI)")
col1, col2, col3 = st.columns(3)

total_sales = filtered_df["sales"].sum() if "sales" in filtered_df.columns else 0
total_profit = filtered_df["profit"].sum() if "profit" in filtered_df.columns else 0
total_orders = len(filtered_df)

col1.metric("💰 Total Revenue", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("🧾 Total Orders", f"{total_orders:,}")

st.subheader("📈 Sales Trend")
if "date" in filtered_df.columns and "sales" in filtered_df.columns:
    trend_data = filtered_df.groupby("date")["sales"].sum().reset_index().sort_values("date")
    if not trend_data.empty:
        fig = px.line(trend_data, x="date", y="sales", markers=True, line_shape="linear")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insufficient data to generate trend chart.")
else:
    st.error("Warning: Missing 'date' or 'sales' columns.")

st.divider()

# =====================
# AI AGENT CHAT (INTERACTIVE)
# =====================
st.subheader("🤖 AI Analysis Assistant (Groq Powered)")
st.markdown("Ask questions based on the current KPI metrics (Apply filters on the left first).")

# Initialize Chat Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display Conversation History
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input UI
if user_prompt := st.chat_input("Ex: Can you evaluate the profit margin against revenue?"):
    
    # 1. Append and Display User Prompt
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 2. Process Assistant Response via Groq
    with st.chat_message("assistant"):
        with st.spinner("Agent is analyzing..."):
            # Pass filtered dataframe and user query to the AI logic
            ai_response = generate_insight(filtered_df, user_prompt)
            st.markdown(ai_response)
            
    # 3. Store AI Response in History
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
