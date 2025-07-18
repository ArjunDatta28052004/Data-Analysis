# 📊 Vendor Performance Analysis

This project analyzes and summarizes vendor performance using purchase, sales, and invoice data. It integrates data from multiple sources, computes essential business metrics, and stores the final summary in a structured SQLite database.

---

## 🔧 Features

- ✅ **Data Integration**  
  Joins data from `purchases`, `sales`, `vendor_invoice`, and `purchase_prices` using SQL to compute vendor-level insights.

- ✅ **ETL Automation**  
  - CSV files ingested into an SQLite database using modular Python scripts (`ingestion_db.py`)
  - Data is transformed and summarized in `get_vendor_summary.py`

- ✅ **Key Business Metrics**  
  - `Gross Profit`  
  - `Profit Margin (%)`  
  - `Sales-to-Purchase Ratio`  
  - `Stock Turnover Ratio`  
  - `Freight Cost`  
  - Total purchase and sales quantities and revenue

- ✅ **Data Cleaning**  
  - Null handling, trimming whitespaces, and converting data types using Pandas  
  - Derived metric fields added to the final summary table

- ✅ **Logging**  
  - Robust logging using Python’s `logging` module to track the execution flow and catch issues

---
### 📥 Download Dataset

You can download the dataset used in this project from the following link:

🔗 [Click here to download the dataset](https://drive.google.com/drive/folders/1erbLbZfkdrBo5fBNuPR1sFVMkdXnivg7)



## 🚀 How to Run

1. **Install Dependencies**  
   Make sure you have `pandas`, `sqlalchemy`, and `sqlite3` installed.

2. **Ingest Raw CSV Files**
python ingestion_db.py
Create and Analyze Vendor Summary

bash
Copy
Edit
python get_vendor_summary.py
Check the SQLite DB
You’ll find the vendor_sales_summary table in inventory.db, ready for analysis or visualization.

🧠 Insights Generated
Identify high-performing vendors based on sales volume and margins

Detect inefficiencies using metrics like freight cost and turnover

Enable data-backed negotiation and sourcing decisions

🛠️ Tech Stack
Python (Pandas, SQLAlchemy, SQLite3)

SQL (Joins, Aggregations, CTEs)

Jupyter Notebook (for EDA and visual insights)

📌 Author
Arjun Datta
Data Enthusiast | ETL Builder | KPI-Driven Analyst



