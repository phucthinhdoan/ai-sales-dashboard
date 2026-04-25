import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_insight(df):

    # 🔥 LIMIT DATA (QUAN TRỌNG)
    df_clean = df.fillna("null")

    # chỉ lấy 10 dòng + 5 cột đầu tiên để tránh token overflow
    data_sample = df_clean.iloc[:10, :5].to_string()

    prompt = f"""
You are a senior business analyst.

Analyze this dataset:

{data_sample}

Return:
1. Key insights
2. Problems
3. Opportunities
4. Action plan

Be concise and professional.
"""

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",  # 🔥 đổi lại model ổn định hơn
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"
