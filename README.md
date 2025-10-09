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

### ✅ Step 2 – Simulated Data Sources
- Generated **two types of datasets** to reflect a real-world recommendation system:

1. **Streaming Logs (`data/stream/user_activity_day1.csv`)**
   - Simulated 200 user activity events with fields:
     - `user_id`
     - `item_id`
     - `event_type` (view, click, add_to_cart)
     - `timestamp`
   - Represents **real-time user behavior** (clickstream data).

2. **Batch Purchases (`data/batch/purchases.csv`)**
   - Simulated 100 historical purchase records with fields:
     - `user_id`
     - `item_id`
     - `purchase_amount`
     - `timestamp`
   - Represents **historical transaction data** from a relational database or data warehouse.

- This dual setup ensures we have:
  - **Real-time logs** for streaming ingestion (Kafka/Spark simulation later).
  - **Batch data** for historical purchase context.

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

### ✅ Step 6 – User Profile Aggregation
- Built **user-level profiles** by aggregating session features from Day 5.
- Key features:
  - `total_sessions`: engagement over time
  - `avg_clicks_per_session`, `avg_views_per_session`: activity intensity
  - `avg_session_length`, `avg_time_gap`: engagement style
  - `avg_purchase_amount`, `max_past_purchases`: monetary history
- Added **recency signals** from last session:
  - `last_session_clicks`, `last_session_views`, `last_session_length`, `last_session_event`
- Saved user-level dataset at `data/users/user_profiles_day1.csv`.

### ✅ Step 7 – User-Item Interaction Matrix
- Constructed a **user-item interaction table** combining purchases and clickstream data.
- Features included:
  - `purchase_count`, `total_spent`
  - `num_clicks`, `num_views`
- Created an **interaction_score**:
  - Weighted combination of purchases, clicks, and views.
  - Formula used: `1*purchases + 0.2*clicks + 0.1*views`
- Saved dataset at `data/reco/user_item_matrix.csv`.

### ✅ Day 8 – Feature Engineering
- Created **feature sets** for users and items:
  
1. **User Features (`data/features/user_features.csv`)**
   - Total purchases
   - Total spent
   - Average spent
   - Engagement counts from stream logs (views, clicks, add_to_cart)

2. **Item Features (`data/features/item_features.csv`)**
   - Total sales count
   - Revenue generated
   - Average selling price

- These features will be used to train recommendation models.
- This marks the transition from **raw data → ML-ready features**.

**Next Step (Day 9):** Start building a baseline recommendation model (e.g., popularity-based or collaborative filtering).









