import json
import os
from datetime import datetime

LOG_FILE = "security_logs.jsonl"

def log_security_incident(user_id, user_input, score, reason, blocked):
    incident = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "input": user_input,
        "score": score,
        "reason": reason,
        "blocked": blocked
    }
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(incident) + "\n")
