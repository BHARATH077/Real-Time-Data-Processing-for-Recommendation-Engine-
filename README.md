# Real-Time Recommendation Engine (Simulation)

## 📌 Project Overview
This project simulates a **real-time recommendation engine pipeline**.  
In a real environment, we would use **Kafka + Spark Streaming + Hive + Airflow**, but here we simulate the same workflow using **Python, Pandas, DuckDB, and Colab**, so it can run on free platforms.

The pipeline integrates **real-time user activity logs** with **historical purchase data**, processes them, and produces **clean, enriched datasets** for recommendation algorithms.

---

## 🗓️ Progress Log

### ✅ Step 1 – Setup & Historical Data
- Created initial project structure (`data/` folder, main notebook).  
- Generated a **historical purchase dataset** with:
  - `user_id` (100 unique users)  
  - `item_id` (500 unique items)  
  - `purchase_amount` (randomized between $10–$500)  
  - `purchase_date` (dates across 2023)  
- Saved dataset in **Parquet format** for efficient processing.  
- Verified dataset preview (500 rows, 4 columns).  




