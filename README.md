# 📞 AI Call Intelligence Agent (ACI)
### Built with Gemini 2.5 Flash & Model Context Protocol (MCP)

## 🌟 Overview
**AI Call Intelligence Agent** is a high-performance AI solution designed to transform raw call center logs into actionable business insights. By leveraging a **decoupled agentic architecture**, the system allows non-technical stakeholders to query BigQuery datasets using natural language.

The core innovation lies in using the **Model Context Protocol (MCP)** as a secure, standardized bridge between the LLM and enterprise data, ensuring data privacy while maintaining high reasoning capabilities.

---

## 🏗️ Architecture: The "Think-Act-Speak" Loop
This project implements a modern **Agentic RAG** pattern:

1.  **Reasoning Engine:** **Gemini 2.5 Flash** (via **Google ADK**) analyzes the user's intent.
2.  **Secure Retrieval:** A custom **MCP Server** translates natural language into optimized SQL for **BigQuery**.
3.  **Synthesis:** The Agent processes raw results into a 3-sentence executive summary, highlighting sentiment trends and operational anomalies.

---

## 🛠️ Technical Stack
* **LLM:** Gemini 2.5 Flash (Optimized for speed and complex function calling)
* **Orchestration:** Google Agent Development Kit (ADK)
* **Data Connectivity:** Model Context Protocol (MCP)
* **Data Warehouse:** Google BigQuery
* **Backend:** Python / FastAPI
* **Deployment:** Containerized with Docker on Google Cloud Run
* **Frontend:** Responsive HTML5 / JavaScript (AJAX)

---

## 🚀 Key Features
* **Conversational Data Interrogation:** No SQL knowledge required to query complex datasets.
* **Autonomous Tool Use:** The agent independently determines which data tools to call based on the user's request.
* **Sentiment Trend Detection:** Real-time tracking of customer mood (e.g., identifying billing-related frustration spikes).
* **Enterprise Security:** Decoupled architecture ensures the LLM never has unmanaged direct access to the database schema.

---

## 💻 Quick Start Guide

### 1. Prerequisites
* Python 3.10+
* Google Cloud Project with BigQuery enabled
* Gemini API Key

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/indu-ai-coder/ai-call-intelligence.git](https://github.com/indu-ai-coder/ai-call-intelligence.git)
cd ai-call-intelligence

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

🛠️ Environment Setup & Configuration
1. Prerequisites
Python 3.10+ installed on your local machine.

Google Cloud Project with the BigQuery API and Vertex AI API enabled.

Service Account Key: A JSON key file with BigQuery Data Viewer and Vertex AI User roles.

2. Local Environment Initialization
Clone the repository and prepare the Python environment:

Bash
# Clone the project
git clone https://github.com/YOUR_USERNAME/ai-call-intelligence.git
cd ai-call-intelligence

# Create and activate a clean virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install core dependencies (ADK, FastAPI, Gemini SDK)
pip install -r requirements.txt
3. Configuration (.env)
Create a .env file in the root directory to store your architectural constants. Note: This file is excluded from Git for security.

Plaintext
# Project Identity
PROJECT_ID="your-google-cloud-project-id"
REGION="us-central1"

# Model Configuration
MODEL_NAME="gemini-2.5-flash"  # Optimized for Agentic Reasoning

# Database Context
DATASET_ID="call_center_analytics"
TABLE_ID="processed_call_logs"

# Authentication
GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
4. Launching the ACI-Insight Agent
Start the backend server using Uvicorn:

Bash
uvicorn agent.main:app --host 0.0.0.0 --port 8080 --reload
Once running, access the ACI-Insight Dashboard at http://localhost:8080.
<p align="center">
  <img src="assets/dashboard.png" alt="AI Call Intelligence Agent" width="800">
</p>

"Security Note: This architecture uses Application Default Credentials (ADC) and a decoupled MCP Server to ensure that sensitive database schemas are never exposed to the client-side interface."