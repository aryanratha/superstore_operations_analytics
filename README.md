# Retail Sales & Profitability Analysis

## Problem Statement
A retail business tracks sales across regions, product categories, and customer segments, but raw transaction data doesn't tell leadership where they're actually making or losing money. High sales volume doesn't always mean high profit — some products or discount strategies can quietly erode margins. The business needs a clear, queryable view of which regions, products, and discount practices help or hurt profitability, so pricing, inventory, and sales strategy decisions can be made with evidence instead of gut feel.

This project uses SQL to answer six concrete business questions from raw order data and presents the findings as an interactive Power BI dashboard.

## Dataset
**Sample Superstore Dataset**
— ~9,800 retail orders with sales, profit, discount, shipping, and customer detail.
**link:** www.kaggle.com/datasets/vivek468/superstore-dataset-final.csv

## Tools & Skills Used
* **SQL (via SQLite):** Joins, GROUP BY, CASE statements, date functions, aggregate queries answering real business questions.
* **Python:** Pandas for loading/cleaning, Matplotlib/Seaborn for visualizing query results.
* **Power BI:** Interactive dashboard with regional map, profitability drill-downs, and slicers.

## Business Questions Answered
1. Which regions drive the most revenue, and do they have healthy profit margins?
2. Which product sub-categories are losing money despite strong sales?
3. Do heavy discounts actually hurt overall profitability?
4. What does the monthly sales and profit trend look like — growth, decline, or seasonal?
5. Who are the top 10 most profitable customers?
6. Which shipping mode has the slowest average delivery time?

## Approach
* Loaded and cleaned the raw CSV in Python.
* Loaded the cleaned data into an in-memory SQLite database.
* Wrote SQL queries to answer each business question above.
* Visualized each query result with Matplotlib/Seaborn.
* Rebuilt the same logic in Power BI using DAX measures for an interactive, filterable dashboard.

## Key Findings
* **Highest-revenue region / lowest-margin region:** The West region makes the most sales. The Central region has the lowest margin because the profit is very small even though it has more sales than the South.   
* **Least profitable sub-category:** : Tables are losing the most money. Bookcases and Supplies are also in the negative red color.
* **Top customer by profit contribution:** Raymond Buch is the number one customer, giving the company $6,976.10 in total profit.

## Business Recommendations
1. Stop giving big discounts: We should not give discount more than 20%. The data is showing if we give more than 20% discount, the company makes loss in profit per order. For any big discount, the manager needs to approve first so we don't lose money.

2. Check products that lose money: Some items like Tables are selling a lot but making negative profit. We need to check with suppliers to reduce cost or just increase the selling price. If it is still losing money, we should stop selling them completely.

3. Look into region costs: Some regions have very high sales but the profit is very low. This means the shipping or working cost is too high there. We need to investigate the lowest margin region to see why we are spending so much money.

4. Make a VIP customer group: Very few top customers are giving us the maximum profit. We should give them VIP treatment like free fast shipping or special offers so they feel happy and keep buying from us.

5. Plan for busy months: The monthly trend chart shows sales go very high in the last few months. We need to keep more stock ready and put more people in the warehouse during this time so delivery is not late and we don't run out of items.

## Dashboard Preview


## Run

```bash
pip install -r requirements.txt
python scripts/superstore_analysis.py



├── datasets/
│   └── Sample - Superstore.csv
├── scripts/
│   └── superstore_analysis.py
├── images/
│   └── dashboard_preview.png
├── power_bi_files/
│   └── Superstore_Dashboard.pbix
├── requirements.txt
├── .gitignore
└── README.md
