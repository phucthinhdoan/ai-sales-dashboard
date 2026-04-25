from src.data import load_data, clean_data
from src.analysis import compute_kpis, monthly_trend, top_products
from src.ai import generate_insight

def main():
    print("🚀 Running Sales Analysis Pipeline...")

    df = load_data("sales.csv")
    df = clean_data(df)

    # KPI
    kpis = compute_kpis(df)
    print("\n📊 KPIs:")
    print(kpis)

    # Trend
    trend = monthly_trend(df)
    print("\n📈 Monthly Trend:")
    print(trend.head())

    # Top products
    print("\n🏆 Top Products:")
    print(top_products(df))

    # AI Insight
    print("\n🤖 Generating AI Insight...")
    insight = generate_insight(df)
    print("\n💡 Insight:")
    print(insight)


if __name__ == "__main__":
    main()