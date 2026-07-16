import pandas as pd
import sqlite3

df = pd.read_csv("data/cleaned_superstore.csv")

conn = sqlite3.connect("database/ecommerce.db")

df.to_sql("orders", conn, if_exists="replace", index=False)

conn.close()

print("Database created successfully")
print("Table name: orders")