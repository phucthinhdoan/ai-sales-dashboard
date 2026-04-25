import pandas as pd

def load_data(file):
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()
    return df

def clean_data(df):
    df = df.drop_duplicates()
    df["Total Profit"] = pd.to_numeric(df["Total Profit"], errors="coerce")
    df = df.dropna(subset=["Total Profit"])
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    return df