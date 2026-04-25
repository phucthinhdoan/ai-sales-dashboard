import streamlit as st
import pandas as pd
import plotly.express as px
import os

# =====================
# IMPORT AI (Xử lý an toàn)
# =====================
try:
    from src.ai import generate_insight
except ImportError:
    # Nếu file src/ai.py bị lỗi hoặc chưa có, tạo hàm tạm để app không bị crash
    def generate_insight(df):
        return "⚠️ Chưa cấu hình xong module AI (src/ai.py)."

# =====================
# CONFIG
# =====================
st.set_page_config(page_title="AI Sales Dashboard", layout="wide")
st.title("🚀 AI Sales Intelligence Dashboard")

# =====================
# LOAD DATA SAFE
# =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Đã sửa lại đường dẫn trỏ thẳng ra file ở thư mục gốc
DATA_PATH = os.path.join(BASE_DIR, "sales.csv") 

@st.cache_data # Thêm cache giúp app load dữ liệu nhanh hơn, không bị giật lag
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error("❌ Missing sales.csv")
        return pd.DataFrame()

    df = pd.read_csv(DATA_PATH)
    
    # 1. Chuẩn hóa tên cột: Xóa khoảng trắng và đưa về chữ thường (để code luôn tìm được cột "sales", "profit")
    df.columns = df.columns.str.strip().str.lower() 
    
    # 2. Xử lý dữ liệu cột Sales: Xóa dấu $, dấu phẩy và ép về dạng số
    if "sales" in df.columns:
        if df['sales'].dtype == 'object':
            df['sales'] = df['sales'].astype(str).str.replace(r'[\$,]', '', regex=True)
        df['sales'] = pd.to_numeric(df['sales'], errors='coerce').fillna(0)
        
    # 3. Xử lý dữ liệu cột Profit
    if "profit" in df.columns:
        if df['profit'].dtype == 'object':
            df['profit'] = df['profit'].astype(str).str.replace(r'[\$,]', '', regex=True)
        df['profit'] = pd.to_numeric(df['profit'], errors='coerce').fillna(0)
        
    return df

df = load_data()

# =====================
# DEBUG DATA
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
# KPI
# =====================
st.subheader("📊 KPI")

col1, col2, col3 = st.columns(3)

# Kiểm tra đúng cú pháp in df.columns thay vì in df
sales = filtered_df["sales"].sum() if "sales" in filtered_df.columns else 0
profit = filtered_df["profit"].sum() if "profit" in filtered_df.columns else 0
orders = len(filtered_df)

col1.metric("💰 Sales", f"${sales:,.0f}")
col2.metric("📈 Profit", f"${profit:,.0f}")
col3.metric("🧾 Orders", orders)

# =====================
# CHART
# =====================
st.subheader("📈 Sales Trend")

if "date" in filtered_df.columns and "sales" in filtered_df.columns:
    # Gom nhóm theo ngày để vẽ biểu đồ
    chart = filtered_df.groupby("date")["sales"].sum().reset_index()

    if not chart.empty:
        fig = px.line(chart, x="date", y="sales", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No chart data")
else:
    st.warning("Missing 'date' or 'sales' column")

# =====================
# AI INSIGHT
# =====================
st.subheader("🤖 AI Insight")

if st.button("Generate Insight"):
    with st.spinner("AI analyzing..."):
        result = generate_insight(filtered_df)
        st.success("Done")
        st.write(result)
