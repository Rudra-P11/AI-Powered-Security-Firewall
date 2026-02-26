import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="Security Firewall Dashboard", layout="wide")
st.title("🛡️ Gemini-Only Security Firewall Dashboard")

# Run this from the root directory of the project
LOG_FILE = "security_logs.jsonl"

def load_data():
    data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    return pd.DataFrame(data)

# Auto-refresh mechanism (button or just rerun)
if st.button("Refresh Data"):
    st.rerun()

df = load_data()

if df.empty:
    st.info("No security logs found yet. Start sending requests to the proxy!")
else:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Metrics
    st.header("Real-Time Metrics")
    col1, col2, col3 = st.columns(3)
    
    total_req = len(df)
    blocked_count = df['blocked'].astype(bool).sum()
    avg_score = df['score'].mean()
    
    col1.metric("Total Analyzed", total_req)
    col2.metric("Blocked Attacks", blocked_count)
    col3.metric("Avg Risk Score", f"{avg_score:.2f}")
    
    st.divider()
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Allowed vs Blocked")
        status_counts = df['blocked'].replace({True: "Blocked", False: "Allowed"}).value_counts()
        st.bar_chart(status_counts)
        
    with col_chart2:
        st.subheader("Risk Score Over Time")
        time_series = df.set_index('timestamp')['score']
        st.line_chart(time_series)
        
    st.divider()
    
    st.subheader("Detailed Incident Logs")
    # Styling trick to highlight blocked ones:
    st.dataframe(
        df.sort_values(by='timestamp', ascending=False),
        column_config={
            "timestamp": "Time",
            "user_id": "User/IP",
            "input": "Prompt Content",
            "score": st.column_config.ProgressColumn("Risk Score", format="%.2f", min_value=0, max_value=1),
            "reason": "Guard Reason",
            "blocked": "Action Taken"
        },
        use_container_width=True
    )
