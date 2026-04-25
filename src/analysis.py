def compute_kpis(df):
    return {
        "Total Profit": df["Total Profit"].sum(),
        "Avg Profit": df["Total Profit"].mean(),
        "Orders": len(df)
    }

def monthly_trend(df):
    df["Month"] = df["Order Date"].dt.to_period("M")
    result = df.groupby("Month")["Total Profit"].sum().reset_index()
    result["Month"] = result["Month"].astype(str)
    return result

def top_products(df):
    return df.groupby("Item Type")["Total Profit"].sum().reset_index().sort_values(by="Total Profit", ascending=False).head(5)