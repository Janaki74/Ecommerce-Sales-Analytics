import pandas as pd

df = pd.read_csv("data/cleaned_superstore.csv")

print("Total Sales:", round(df["Sales"].sum(), 2))
print("Total Profit:", round(df["Profit"].sum(), 2))
print("Total Orders:", df["Order ID"].nunique())
print("Total Customers:", df["Customer ID"].nunique())

print("\nSales by Category:")
print(df.groupby("Category")["Sales"].sum().sort_values(ascending=False))

print("\nProfit by Region:")
print(df.groupby("Region")["Profit"].sum().sort_values(ascending=False))

print("\nTop 10 Products:")
print(df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10))