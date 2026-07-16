import pandas as pd

df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin1")

print(df.head())
print(df.info())
print(df.isnull().sum())
print("Duplicates:", df.duplicated().sum())

df.drop_duplicates(inplace=True)

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["Month Name"] = df["Order Date"].dt.month_name()
df["Delivery Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
df["Profit Margin"] = (df["Profit"] / df["Sales"]) * 100

df.to_csv("data/cleaned_superstore.csv", index=False)

print("Data cleaning completed")