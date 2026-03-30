# Use a slim Python image to keep it fast
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the agent code
COPY . .

# Start the server using Uvicorn
# 'agent' refers to agent.py, 'app' refers to the FastAPI variable inside it
CMD ["uvicorn", "agent:app", "--host", "0.0.0.0", "--port", "8080"]