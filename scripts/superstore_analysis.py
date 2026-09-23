"""
RETAIL SALES & PROFITABILITY ANALYSIS
=======================================

"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# ---------------------------------------------------------
# 1. LOADING & CLEANING DATA
# ---------------------------------------------------------
# encoding='latin1' because this dataset commonly has non-UTF8 characters
df = pd.read_csv(r"C:\Users\DELL\OneDrive\Documents\Data Analytics Projects\Sample-superstore_project\Sample - Superstore.csv", encoding="latin1")

print("Shape:", df.shape)
print(df.columns.tolist())

# Standardize column names (remove spaces, lowercase) for easier SQL writing
df.columns = [c.strip().replace(" ", "_").replace("-", "_") for c in df.columns]

# Parse dates
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Ship_Date"] = pd.to_datetime(df["Ship_Date"])

print("\nMissing values:\n", df.isnull().sum()[df.isnull().sum() > 0])
print("\nDate range:", df["Order_Date"].min(), "to", df["Order_Date"].max())

# ---------------------------------------------------------
# 2. LOAD INTO SQLITE — now we can write real SQL
# ---------------------------------------------------------
conn = sqlite3.connect(":memory:")
df.to_sql("orders", conn, index=False, if_exists="replace")


def run_query(sql):
    """Helper to run SQL and return a DataFrame"""
    return pd.read_sql_query(sql, conn)


# ---------------------------------------------------------
# 3. BUSINESS QUESTION 1: Which regions/states drive revenue vs profit?
# ---------------------------------------------------------
q1 = """
SELECT Region,
       ROUND(SUM(Sales), 2)  AS total_sales,
       ROUND(SUM(Profit), 2) AS total_profit,
       ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin_pct
FROM orders
GROUP BY Region
ORDER BY total_sales DESC;
"""
region_perf = run_query(q1)
print("\n--- Sales & Profit by Region ---\n", region_perf)

plt.figure(figsize=(7, 4))
sns.barplot(data=region_perf, x="Region", y="total_sales")
plt.title("Total Sales by Region")
plt.tight_layout()
plt.savefig("sales_by_region.png")
plt.show()

# ---------------------------------------------------------
# 4. BUSINESS QUESTION 2: Which product categories/sub-categories
#    are LOSING money despite high sales? (this is the "insight" question)
# ---------------------------------------------------------
q2 = """
SELECT Category, Sub_Category,
       ROUND(SUM(Sales), 2)  AS total_sales,
       ROUND(SUM(Profit), 2) AS total_profit,
       ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin_pct
FROM orders
GROUP BY Category, Sub_Category
ORDER BY total_profit ASC
LIMIT 10;
"""
losing_products = run_query(q2)
print("\n--- 10 Least Profitable Sub-Categories (by total profit) ---\n", losing_products)

plt.figure(figsize=(9, 5))
sns.barplot(data=losing_products, x="total_profit", y="Sub_Category", hue="Category", dodge=False)
plt.title("Least Profitable Sub-Categories")
plt.axvline(0, color="black", linewidth=1)
plt.tight_layout()
plt.savefig("least_profitable_subcategories.png")
plt.show()

# ---------------------------------------------------------
# 5. BUSINESS QUESTION 3: Are discounts killing profit?
#    (a classic "hidden insight" — high discounts often correlate with losses)
# ---------------------------------------------------------
q3 = """
SELECT
    CASE
        WHEN Discount = 0 THEN '0%'
        WHEN Discount <= 0.2 THEN '1-20%'
        WHEN Discount <= 0.4 THEN '21-40%'
        ELSE '40%+'
    END AS discount_band,
    COUNT(*) AS num_orders,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(AVG(Profit), 2) AS avg_profit_per_order
FROM orders
GROUP BY discount_band
ORDER BY discount_band;
"""
discount_impact = run_query(q3)
print("\n--- Discount Band vs Profit ---\n", discount_impact)

plt.figure(figsize=(7, 4))
sns.barplot(data=discount_impact, x="discount_band", y="avg_profit_per_order")
plt.title("Average Profit per Order by Discount Band")
plt.axhline(0, color="black", linewidth=1)
plt.tight_layout()
plt.savefig("discount_vs_profit.png")
plt.show()

# ---------------------------------------------------------
# 6. BUSINESS QUESTION 4: Monthly sales trend — is the business
#    growing, seasonal, or declining?
# ---------------------------------------------------------
q4 = """
SELECT strftime('%Y-%m', Order_Date) AS month,
       ROUND(SUM(Sales), 2) AS total_sales,
       ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY month
ORDER BY month;
"""
monthly_trend = run_query(q4)

plt.figure(figsize=(12, 5))
plt.plot(monthly_trend["month"], monthly_trend["total_sales"], label="Sales", marker="o")
plt.plot(monthly_trend["month"], monthly_trend["total_profit"], label="Profit", marker="o")
plt.xticks(rotation=90)
plt.title("Monthly Sales & Profit Trend")
plt.legend()
plt.tight_layout()
plt.savefig("monthly_trend.png")
plt.show()

# ---------------------------------------------------------
# 7. BUSINESS QUESTION 5: Who are the top 10 customers by profit?
#    (useful for a "VIP retention" recommendation)
# ---------------------------------------------------------
q5 = """
SELECT Customer_Name,
       COUNT(DISTINCT Order_ID) AS num_orders,
       ROUND(SUM(Sales), 2) AS total_sales,
       ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY Customer_Name
ORDER BY total_profit DESC
LIMIT 10;
"""
top_customers = run_query(q5)
print("\n--- Top 10 Customers by Profit ---\n", top_customers)

# ---------------------------------------------------------
# 8. BUSINESS QUESTION 6: Shipping delay analysis
#    (Order_Date to Ship_Date gap — an ops-angle question, shows range)
# ---------------------------------------------------------
q6 = """
SELECT Ship_Mode,
       ROUND(AVG(julianday(Ship_Date) - julianday(Order_Date)), 2) AS avg_days_to_ship,
       COUNT(*) AS num_orders
FROM orders
GROUP BY Ship_Mode
ORDER BY avg_days_to_ship DESC;
"""
shipping = run_query(q6)
print("\n--- Avg Shipping Time by Ship Mode ---\n", shipping)

# ---------------------------------------------------------
# 9. SAVE ALL QUERY RESULTS FOR YOUR README / DASHBOARD
# ---------------------------------------------------------
region_perf.to_csv("region_performance.csv", index=False)
losing_products.to_csv("least_profitable_subcategories.csv", index=False)
discount_impact.to_csv("discount_impact.csv", index=False)
monthly_trend.to_csv("monthly_trend.csv", index=False)
top_customers.to_csv("top_customers.csv", index=False)
shipping.to_csv("shipping_analysis.csv", index=False)

conn.close()

# ---------------------------------------------------------
# 10. FINDINGS TEMPLATE — replace with YOUR actual numbers
# ---------------------------------------------------------
print("""
KEY FINDINGS TEMPLATE (fill in with your real output above):
1. [Region] generates the highest sales but [Region] has the lowest
   profit margin -> investigate pricing/logistics costs there.
2. [Sub-Category] sells well but is actually losing money overall
   -> recommend renegotiating supplier cost or repricing.
3. Orders with discounts above 40% have negative average profit
   -> recommend capping discretionary discounts at 20%.
4. Sales show a clear seasonal spike in [month(s)] -> recommend
   inventory/staffing planning ahead of that period.
5. Top 10 customers contribute a disproportionate share of profit
   -> recommend a loyalty/priority program for them.
""")
