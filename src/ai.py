import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_insight(df):

    data_sample = df.head(20).to_string()

    prompt = f"""
You are a senior business analyst.

Analyze this dataset:

{data_sample}

Provide:
- Key insights
- Problems
- Opportunities
- Action plan

Keep it short and professional.
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
