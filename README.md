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

### ✅ Step 2 – Real-Time User Activity Logs
- Simulated **200 user activity events** to mimic real-time streaming logs.
- Each event contains:
  - `user_id`
  - `item_id`
  - `event_type` (view, click, add_to_cart)
  - `timestamp`
- Saved logs to `data/stream/user_activity_day1.csv` to represent streaming ingestion.

### ✅ Step 3 – Mini Streaming Pipeline (First Join)
- Read historical purchases (`historical_purchases.parquet`) and simulated stream logs (`user_activity_day1.csv`).
- Built a **mini streaming pipeline** using DuckDB:
  - Joined stream events with purchase history by `user_id`.
  - Calculated features:
    - Average purchase amount per user.
    - Count of past purchases per user.
- Saved enriched events to `data/enriched/enriched_day1.csv`.

### ✅ Step 4 – Simulated Chunked Streaming
- Instead of processing all logs at once, simulated **real-time arrival** by splitting `user_activity_day1.csv` into **chunks of 50 events**.
- Processed each batch separately with DuckDB:
  - Enriched with purchase history (average spend, past purchases).
- Appended enriched results to `data/enriched/enriched_day1_chunked.csv`.

### ✅ Step 5 – Session-Level Feature Engineering
- Took enriched streaming data (`enriched_day1_chunked.csv`) and grouped activity into **sessions per user**.
- Defined a session as continuous activity with no gap larger than **30 minutes**.
- Engineered session features:
  - `num_clicks`, `num_views` → interaction counts
  - `session_length`, `avg_time_gap` → engagement intensity
  - `last_event` → potential intent signal
  - `avg_purchase_amount`, `past_purchases` → historical enrichment
- Saved the final session dataset at `data/sessions/session_features_day1.csv`.

**Next Step (Day 6):** Generate **user profiles** by aggregating across sessions (long-term behavior), preparing for recommendation modeling.









