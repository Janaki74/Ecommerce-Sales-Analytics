SELECT *
FROM orders
LIMIT 10;

SELECT 
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    COUNT(DISTINCT "Order ID") AS total_orders,
    COUNT(DISTINCT "Customer ID") AS total_customers
FROM orders;

SELECT 
    Category,
    ROUND(SUM(Sales), 2) AS total_sales
FROM orders
GROUP BY Category
ORDER BY total_sales DESC;

SELECT 
    Region,
    ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY Region
ORDER BY total_profit DESC;

SELECT 
    "Product Name",
    ROUND(SUM(Sales), 2) AS total_sales
FROM orders
GROUP BY "Product Name"
ORDER BY total_sales DESC
LIMIT 10;

SELECT 
    "Customer Name",
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY "Customer Name"
ORDER BY total_sales DESC
LIMIT 10;