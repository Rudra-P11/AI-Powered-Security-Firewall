from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure the core module can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.security_guard import analyze_prompt
from core.brain_model import generate_safe_response
from core.logger import log_security_incident

app = FastAPI(title="Gemini Security Proxy")

class PromptRequest(BaseModel):
    user_input: str
    user_id: str = "default_user"

@app.post("/generate")
async def secure_generate(request: PromptRequest):
    # 1. Ask the 'Guard' (Gemini Flash)
    score, reason = analyze_prompt(request.user_input, request.user_id)
    
    # 2. Check the risk
    if score > 0.8:
        log_security_incident(request.user_id, request.user_input, score, reason, blocked=True)
        return {
            "status": "error", 
            "message": "Access Denied: Malicious activity detected.", 
            "reason": reason,
            "score": score
        }

    # Log safe and borderline prompts
    log_security_incident(request.user_id, request.user_input, score, reason, blocked=False)

    # 3. If safe, proceed to the main task
    response_text = generate_safe_response(request.user_input)
    
    return {
        "status": "success", 
        "response": response_text,
        "score": score
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
