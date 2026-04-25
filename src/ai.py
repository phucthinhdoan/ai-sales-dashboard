import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_insight(df):

    df_clean = df.fillna("null")

    data_sample = df_clean.iloc[:10, :5].to_string()

    prompt = f"""
You are a senior business analyst.

Analyze this dataset:

{data_sample}

Give:
- Key insights
- Problems
- Opportunities
- Action plan

Be concise and professional.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ MODEL MỚI
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"
