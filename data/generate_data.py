import pandas as pd
import numpy as np
from google.cloud import bigquery
from datetime import datetime, timedelta
import uuid
import os

def generate_call_data(rows=800):
    intents = ["Billing", "Technical Issue", "Cancellation", "General Inquiry"]
    sentiments = ["Positive", "Neutral", "Negative"]
    
    data = []
    # Generate data for the last 7 days including today
    start_date = datetime.now() - timedelta(days=7)

    for i in range(rows):
        # Randomize time within the 7-day window
        random_days = np.random.randint(0, 8)
        random_hours = np.random.randint(0, 24)
        dt = start_date + timedelta(days=random_days, hours=random_hours)
        
        data.append({
            "call_id": str(uuid.uuid4()),
            "timestamp": dt, # BigQuery handles Python datetime objects
            "customer_id": f"CUST-{np.random.randint(1000, 9999)}",
            "intent": np.random.choice(intents, p=[0.35, 0.30, 0.15, 0.20]),
            "sentiment": np.random.choice(sentiments, p=[0.25, 0.35, 0.40]),
            "call_duration": np.random.randint(60, 1500),
            "agent_id": f"AGENT-{np.random.randint(1, 30)}"
        })
    
    return pd.DataFrame(data)

def upload_to_bq(df):
    project_id = os.environ.get("PROJECT_ID")
    client = bigquery.Client(project=project_id)
    table_id = f"{project_id}.call_center_analytics.call_records"
    
    # Overwrite if exists to keep the lab clean
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    
    print(f"🚀 Uploading {len(df)} rows to {table_id}...")
    client.load_table_from_dataframe(df, table_id, job_config=job_config).result()
    print("✅ Data Layer successfully established!")

if __name__ == "__main__":
    df = generate_call_data()
    upload_to_bq(df)