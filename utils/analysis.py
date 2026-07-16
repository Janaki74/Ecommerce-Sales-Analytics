import pandas as pd


def load_data():
    df = pd.read_csv("data/cleaned_superstore.csv")
    return df


def get_kpis(df):
    return {
        "total_sales": round(df["Sales"].sum(), 2),
        "total_profit": round(df["Profit"].sum(), 2),
        "total_orders": df["Order ID"].nunique(),
        "total_customers": df["Customer ID"].nunique()
    }


def executive_summary(df):
    region_sales = df.groupby("Region")["Sales"].sum()
    category_sales = df.groupby("Category")["Sales"].sum()
    monthly_sales = df.groupby("Month Name")["Sales"].sum()

    best_region = region_sales.idxmax()
    weak_region = region_sales.idxmin()
    best_category = category_sales.idxmax()
    best_month = monthly_sales.idxmax()

    loss_products = df[df["Profit"] < 0]["Product Name"].nunique()

    return {
        "best_region": best_region,
        "weak_region": weak_region,
        "best_category": best_category,
        "best_month": best_month,
        "risk_products": loss_products
    }


def product_advisor(df, product_name):
    product_df = df[df["Product Name"].str.contains(product_name, case=False, na=False)]

    if product_df.empty:
        return None

    monthly_sales = product_df.groupby("Month Name")["Sales"].sum()
    region_sales = product_df.groupby("Region")["Sales"].sum()

    return {
        "product": product_name,
        "total_sales": round(product_df["Sales"].sum(), 2),
        "total_profit": round(product_df["Profit"].sum(), 2),
        "best_month": monthly_sales.idxmax(),
        "worst_month": monthly_sales.idxmin(),
        "best_region": region_sales.idxmax(),
        "weak_region": region_sales.idxmin(),
        "recommendation": f"Promote this product more in {monthly_sales.idxmax()} and focus improvement in {region_sales.idxmin()} region."
    }


def profit_risk_products(df):
    risk_df = (
        df.groupby("Product Name", as_index=False)
        .agg({"Sales": "sum", "Profit": "sum", "Discount": "mean"})
    )

    risk_df = risk_df[risk_df["Profit"] < 0]
    risk_df = risk_df.sort_values("Profit")

    return risk_df.head(20)