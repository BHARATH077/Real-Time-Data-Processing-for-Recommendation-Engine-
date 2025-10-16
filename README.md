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

### ✅ Step 8 – Feature Engineering
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

### ✅ Step 9 – Baseline Popularity-Based Recommender
- Implemented a **baseline recommendation model** that suggests the most popular items to every user.
- Popularity is calculated using:
  - Total sales (70% weight)
  - Normalized revenue (30% weight)
- Generated a ranked list of top items and stored it in:
  - `data/recommendations/popularity_based.csv`

This model establishes a **benchmark** for evaluating future recommendation models.

### ✅ Step 10 – Collaborative Filtering (User-Based using sklearn)
- Implemented a **Collaborative Filtering Recommender** using cosine similarity.
- Created a **user–item matrix** from clickstream and purchase interactions.
- Measured **user similarity** using `sklearn.metrics.pairwise.cosine_similarity`.
- Generated personalized recommendations for each user.
- Saved results to `data/recommendations/user_based_cf.csv`.

### ✅ Step 11 – Model Evaluation & Visualization
- Generated **user–item ratings** from `purchase_amount`:
  ```python
  purchases["rating"] = np.clip((purchases["purchase_amount"] / purchases["purchase_amount"].max()) * 5, 1, 5)
- Constructed a user–item matrix from purchase data.
- Calculated user similarity using sklearn.metrics.pairwise.cosine_similarity.
- Generated top-N recommendations for example users.
- Evaluated model performance with RMSE and MAE.
- Visualized user–item interactions via a heatmap.
- Saved evaluation metrics to data/recommendations/evaluation_day11.csv.

### ✅ Step 12 – Recommendation Insights & Visualizations
- Ensured the `visuals/` directory exists before saving plots:
  ```python
  os.makedirs("visuals", exist_ok=True)
- Generated multiple data-driven visualizations to analyze user behavior and recommendation quality:
- Distribution of purchase amounts using Seaborn histograms.
- User–Item interaction heatmap to visualize model coverage.
- Highlighted key trends in purchase frequency and item popularity.
- Exported generated visualizations to:
  ```python
  visuals/purchase_amount_distribution.png  
  visuals/user_item_heatmap.png
- Improved data storytelling by linking visual insights to user engagement metrics.
- Prepared outputs for inclusion in the final project report and GitHub documentation.

### ✅ Step 13: Interactive Dashboard (Streamlit)
#### Objective: Build an interactive dashboard to visualize data and explore recommendations.
Tasks Completed
- Designed Streamlit app (app.py) for quick visualization of purchase insights and model results.
- Displayed key metrics: total users, total items, total purchases.
- Embedded visualizations from Day 12.
- Added user selection feature for personalized recommendation view.
- Enabled local hosting inside Colab using localtunnel (no paid tools).

### ✅ Step 14 – Final Cleanup and GitHub Preparation
#### Objective: Finalize the project by organizing files, creating the required folder structure, and preparing the repository for GitHub deployment.
🧩 Tasks Completed
- Organized all assets into a clean, production-style structure.
- Added a requirements.txt file listing dependencies (pandas, numpy, scikit-learn, matplotlib, seaborn, streamlit).
- Consolidated all notebooks and scripts into one unified directory for version control.
- Created the final README.md documenting:
  - End-to-end pipeline overview
  - Daily progress summary
  - Architecture flow
  - Setup and execution steps
  - Future enhancement ideas
- Verified visualization and model directories contain final outputs.
- Prepared the project for GitHub publishing with proper .gitignore and commit instructions.










