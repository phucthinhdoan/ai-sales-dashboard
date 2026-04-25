import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_insight(df):
    prompt = f"""
    You are a senior business analyst.

    Analyze this dataset and give:
    - Key trends
    - Problems
    - Opportunities
    - Action plan

    Data sample:
    {df.head(10).to_string()}
    """

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
