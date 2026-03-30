import os
import requests
import vertexai
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from vertexai.generative_models import GenerativeModel, Tool, FunctionDeclaration
from dotenv import load_dotenv
from pathlib import Path

# Look for .env in the parent directory (the project root)
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Now these will pull from your root .env file
PROJECT_ID = os.getenv("PROJECT_ID")
MCP_URL = os.getenv("MCP_URL")

vertexai.init(project=PROJECT_ID, location="us-central1")

app = FastAPI()

# Define the Tool for the Agent
mcp_tool = Tool(function_declarations=[
    FunctionDeclaration(
        name="get_call_summary",
        description="Retrieves call center analytics (intent, sentiment, duration) for a specific date.",
        parameters={
            "type": "object",
            "properties": {"date": {"type": "string", "description": "The date in YYYY-MM-DD format"}},
            "required": ["date"]
        }
    )
])

# Initialize the Gemini Model with the Tool
model = GenerativeModel("gemini-2.5-flash", tools=[mcp_tool])

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <html>
        <head>
            <title>Call Intelligence Agent</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 50px; background-color: #f8f9fa; }
                .container { max-width: 600px; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
                h2 { color: #1a73e8; margin-top: 0; }
                input { width: 70%; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; }
                button { padding: 12px 20px; background-color: #1a73e8; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; }
                button:hover { background-color: #1557b0; }
                #response { margin-top: 30px; line-height: 1.6; color: #333; white-space: pre-wrap; border-top: 1px solid #eee; padding-top: 20px; }
                .loader { border: 4px solid #f3f3f3; border-top: 4px solid #1a73e8; border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite; display: none; margin: 20px auto; }
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>📞 Call Intelligence Agent</h2>
                <p>Ask about call volumes, intents, or sentiment for a specific date.</p>
                
                <input id="question" placeholder="Try: Summarize 2026-03-25">
                <button type="button" onclick="askAgent()">Ask Agent</button>
                
                <div id="loader" class="loader"></div>
                <div id="response"></div>
            </div>

            <script>
                async function askAgent() {
                    const question = document.getElementById('question').value;
                    const responseDiv = document.getElementById('response');
                    const loader = document.getElementById('loader');
                    
                    if (!question) return alert("Please enter a question!");

                    // Setup UI for loading
                    responseDiv.innerText = "";
                    loader.style.display = "block";

                    try {
                        const res = await fetch('/chat', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                            body: new URLSearchParams({ 'q': question })
                        });
                        
                        const data = await res.json();
                        loader.style.display = "none";
                        
                        if (data.answer) {
                            responseDiv.innerHTML = "<strong>Result:</strong><br>" + data.answer;
                        } else {
                            responseDiv.innerText = "Error: " + JSON.stringify(data);
                        }
                    } catch (err) {
                        loader.style.display = "none";
                        responseDiv.innerText = "Failed to connect to agent: " + err;
                    }
                }
            </script>
        </body>
    </html>
    """

@app.post("/chat")
async def chat(q: str = Form(...)):
    chat_session = model.start_chat()
    response = chat_session.send_message(q)
    
    # Check if Gemini wants to use the MCP Tool
    part = response.candidates[0].content.parts[0]
    if part.function_call:
        # 1. Get the date Gemini identified
        args = dict(part.function_call.args)
        
        # 2. Call your live MCP Server
        mcp_res = requests.post(f"{MCP_URL}/tools/get_call_summary", json=args)
        
        # 3. Give the data back to Gemini for the final answer
        final_response = chat_session.send_message(
            f"The data for that date is: {mcp_res.text}. Summarize the top intents and sentiment."
        )
        return {"answer": final_response.text}
    
    return {"answer": response.text}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Agent is starting on http://0.0.0.0:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)