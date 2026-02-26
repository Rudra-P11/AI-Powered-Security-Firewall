# 🛡️ Gemini-Only Security Firewall

An intelligent middleware proxy application that acts as a robust security firewall for Large Language Models (LLMs). This project implements an architecture where a smaller, faster model (**Gemini 2.5 Flash**) acts as "The Guard" and structurally evaluates incoming prompts before passing them to the more powerful "Brain" model (**Gemini 2.5 Pro**).

## 🚀 Key Features

*   **Intelligent Routing proxy:** A FastAPI server that handles prompt requests.
*   **The Guard Model:** Instructed using strictly defined System Instructions and Few-Shot Prompting, to analyze input for Prompt Injections, Jailbreaking, and System Prompt Leakage. 
*   **The Brain Model:** Processes tasks only when given the green light from the Guard.
*   **Safety Override:** Safety Settings are programmatically set to `BLOCK_NONE` on the Guard to allow it to evaluate and analyze malicious payloads, rather than failing immediately at the API level.
*   **"Shadow Intelligence" (Adaptive Rate Limiting):** User prompt strictness dynamically adjusts. If a user consistently sends "borderline" queries, the Guard tightens security explicitly for that user ID.
*   **Security Visualizer Dashboard:** A Streamlit UI tracking total blocked attacks, incident logs, and average risk score.
*   **Automated Red Teaming:** A built-in Python script uses Python `requests` and `fpdf2` to send test attacks against the proxy and dynamically outputs a `Vulnerability_Report.pdf` displaying results.

## 🛠️ Tech Stack
*   **Python:** The core scripting language.
*   **FastAPI:** Serves as the high-speed middleware proxy.
*   **Streamlit:** For building the interactive, real-time Security Dashboard.
*   **Google GenAI SDK (`google-genai`):** The primary bridge to interact with both the Flash and Pro Gemini variants.
*   **FPDF2:** For generating dynamic vulnerability reports.

## 📦 Setup and Installation

### 1. Clone & Set Up Virtual Environment

```bash
mkdir CyberAgent && cd CyberAgent
python -m venv venv
```

Activate the virtual environment:
*   **Windows:** `.\venv\Scripts\activate`
*   **macOS/Linux:** `source venv/bin/activate`

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add API Keys

Create a `.env` file at the root of the project by copying the example:
```bash
cp .env.example .env
```
Inside `.env`, populate the API Key replacing the placeholder text:
```ini
GEMINI_API_KEY=your_actual_api_key_here
```

## 🏃 Running the Application

There are three core components to run. It's recommended to run them in three separate terminal environments while your `venv` is activated.

### 1. Start the API Proxy (Middleware)
This starts the FastAPI firewall that protects the Brain model.
```bash
uvicorn api.main:app --host localhost --port 8000 --reload
```
The API is now running locally on `http://localhost:8000/generate`.

### 2. Start the Security Dashboard
This launches the Streamlit UI to monitor logs.
```bash
streamlit run dashboard/app.py
```
Open your browser and navigate to `http://localhost:8501`.

### 3. Run Automated Testing and Generate Vulnerability Report
With the FastAPI Proxy running, test its defenses:
```bash
python reporting/generate_report.py
```
This script will shoot benign and malicious payloads at the API and generate a `Vulnerability_Report.pdf` at the root directory highlighting the proxy's responses and the Guardian's scores.

## 📁 Repository Structure

```text
CyberAgent/
│
├── api/
│   └── main.py              # The FastAPI proxy entry point
│
├── core/
│   ├── brain_model.py       # Main task handling (Gemini Pro)
│   ├── logger.py            # Log management logic
│   └── security_guard.py    # Guard model (Gemini Flash + Shadow Intelligence)
│
├── dashboard/
│   └── app.py               # Streamlit Dashboard UI
│
├── reporting/
│   └── generate_report.py   # Red-teaming & PDF Generator script
│
├── .env                     # API Key configurations
├── requirements.txt         # Project dependencies
├── security_logs.jsonl      # System-generated Security Logs (appears after first run)
└── README.md                # Project documentation
```
