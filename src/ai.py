import os
import pandas as pd
from groq import Groq

# Initialize Groq client. It will automatically look for the GROQ_API_KEY environment variable.
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception:
    client = None

def generate_insight(df: pd.DataFrame, user_message: str) -> str:
    """
    Data Analysis Agent using Groq API.
    Applies Context Compression to prevent AI hallucinations.
    """
    if not client:
        return "⚠️ Error: GROQ_API_KEY not found. Please configure your environment variables."

    # 1. CONTEXT COMPRESSION
    # Pre-calculate data using Pandas to feed 100% accurate facts to the AI
    total_sales = df['sales'].sum() if 'sales' in df.columns else 0
    total_profit = df['profit'].sum() if 'profit' in df.columns else 0
    total_orders = len(df)
    
    # Identify Top 3 best-selling item types
    top_items = "No data available"
    if 'item type' in df.columns and 'sales' in df.columns:
        top_items_df = df.groupby('item type')['sales'].sum().nlargest(3)
        top_items = ", ".join([f"{idx} (${val:,.0f})" for idx, val in top_items_df.items()])

    # Package the compressed data into a string
    compressed_context = f"""
    [CURRENT CONTEXT DATA - FILTERED]
    - Total Orders: {total_orders}
    - Total Revenue: ${total_sales:,.2f}
    - Total Profit: ${total_profit:,.2f}
    - Top 3 Item Types by Revenue: {top_items}
    """

    # 2. DEFINE AGENT PERSONA & RULES
    system_prompt = f"""
    You are a 'Data Analyst Agent' - a high-level business intelligence expert.
    Your task is to advise the Executive based SOLELY on the 'Current Context Data' provided below.
    
    Strict Rules:
    1. Answer in English.
    2. DO NOT hallucinate or invent numbers. Only use the figures provided in the context.
    3. If a question requires data not available in the context, politely decline and state that you lack that information.
    4. Keep answers concise, professional, and use bullet points for readability.

    {compressed_context}
    """

    # 3. CALL GROQ API
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.3, # Low temperature for logical and accurate reasoning
            max_tokens=1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error connecting to Groq AI: {str(e)}"
