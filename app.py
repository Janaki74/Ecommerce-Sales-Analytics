from flask import Flask, render_template, request, redirect, url_for, session, send_file
import pandas as pd
import plotly.express as px
import plotly
import json
import os

from utils.analysis import (
    load_data,
    get_kpis,
    executive_summary,
    product_advisor,
    profit_risk_products
)

app = Flask(__name__)
app.secret_key = "smart_sales_advisor_secret"

df = load_data()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "1234":
            session["user"] = username
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    data = df.copy()

    selected_region = request.form.get("region", "All")
    selected_category = request.form.get("category", "All")
    selected_segment = request.form.get("segment", "All")
    selected_month = request.form.get("month", "All")

    if selected_region != "All":
        data = data[data["Region"] == selected_region]

    if selected_category != "All":
        data = data[data["Category"] == selected_category]

    if selected_segment != "All":
        data = data[data["Segment"] == selected_segment]

    if selected_month != "All":
        data = data[data["Month Name"] == selected_month]

    kpis = get_kpis(data)
    summary = executive_summary(data)

    category_sales = data.groupby("Category", as_index=False)["Sales"].sum()
    fig1 = px.bar(
        category_sales,
        x="Sales",
        y="Category",
        orientation="h",
        title="Sales by Category"
    )

    region_sales = (
        data.groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )
    fig2 = px.bar(
        region_sales,
        x="Sales",
        y="Region",
        orientation="h",
        title="Region-wise Sales"
    )

    monthly_sales = (
        data.groupby(["Month", "Month Name"], as_index=False)["Sales"]
        .sum()
        .sort_values("Month")
    )
    fig3 = px.line(
        monthly_sales,
        x="Month Name",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    top_products = (
        data.groupby("Product Name", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )
    fig4 = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        title="Top 10 Products"
    )

    graphs = [
        json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder),
        json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder),
        json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder),
        json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    ]

    regions = ["All"] + sorted(df["Region"].dropna().unique())
    categories = ["All"] + sorted(df["Category"].dropna().unique())
    segments = ["All"] + sorted(df["Segment"].dropna().unique())
    months = ["All"] + list(df.sort_values("Month")["Month Name"].dropna().unique())

    insights = [
        f"{summary['best_region']} region has the highest sales.",
        f"{summary['weak_region']} region has the lowest sales and needs improvement.",
        f"{summary['best_category']} category is performing best.",
        f"{summary['best_month']} is the best month for sales.",
        f"{summary['risk_products']} products are currently causing losses."
    ]

    return render_template(
        "dashboard.html",
        kpis=kpis,
        summary=summary,
        insights=insights,
        graphs=graphs,
        regions=regions,
        categories=categories,
        segments=segments,
        months=months,
        selected_region=selected_region,
        selected_category=selected_category,
        selected_segment=selected_segment,
        selected_month=selected_month
    )


@app.route("/product-advisor", methods=["GET", "POST"])
def product_page():
    if "user" not in session:
        return redirect(url_for("login"))

    result = None
    product_name = ""

    if request.method == "POST":
        product_name = request.form.get("product_name")
        result = product_advisor(df, product_name)

    return render_template(
        "product_advisor.html",
        result=result,
        product_name=product_name
    )


@app.route("/risk-alerts")
def risk_alerts():
    if "user" not in session:
        return redirect(url_for("login"))

    risk_df = profit_risk_products(df)
    risk_data = risk_df.to_dict("records")

    return render_template(
        "risk_alerts.html",
        risk_data=risk_data
    )


@app.route("/export")
def export_excel():
    if "user" not in session:
        return redirect(url_for("login"))

    os.makedirs("exports", exist_ok=True)
    file_path = "exports/smart_sales_report.xlsx"

    report = df.groupby(["Region", "Category"], as_index=False).agg({
        "Sales": "sum",
        "Profit": "sum",
        "Order ID": "nunique"
    })

    report.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)