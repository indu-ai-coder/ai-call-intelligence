from fastapi import FastAPI, HTTPException
from google.cloud import bigquery
import os

app = FastAPI()
client = bigquery.Client()

@app.post("/tools/get_call_summary")
async def get_call_summary(data: dict):
    target_date = data.get("date")
    if not target_date:
        raise HTTPException(status_code=400, detail="Date is required (YYYY-MM-DD)")

    query = f"""
        SELECT 
            intent, 
            sentiment, 
            AVG(call_duration) as avg_duration,
            COUNT(*) as call_count
        FROM `{os.environ.get("PROJECT_ID")}.call_center_analytics.call_records`
        WHERE DATE(timestamp) = '{target_date}'
        GROUP BY intent, sentiment
    """
    
    try:
        query_job = client.query(query)
        results = query_job.to_dataframe()
        return results.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)