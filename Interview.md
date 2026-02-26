# 🎙️ Interview Preparation Guide: Gemini-Only Security Firewall

Use this document to prepare for interviews. The first section is a "Narrative Explanation" that you can use to explain the project in a conversational way. The second section contains common technical questions and answers.

---

## 📖 How to Explain This Project (The Pitch)

"I built a project called the **Ai-Powered Security Firewall**. The core idea came from a growing problem in AI: **LLM Security**. As we integrate AI into more apps, they become vulnerable to things like 'Prompt Injections' or 'Jailbreaking'—where a user tries to trick the AI into ignoring its safety rules or leaking sensitive instructions.

Most people try to solve this with simple word filters, but that’s not enough. So, I designed a **'Multi-Layered Middleware'** architecture. I used two different models for two different jobs. I call them **The Guard** and **The Brain**.

**The Guard** is powered by Gemini Flash. It’s fast and cheap. Its only job is to look at every single thing a user says and give it a 'Security Score' from 0 to 1. I wrote a very strict system prompt and used few-shot examples to make it act like a security classifier. One cool thing I did here was setting the API's safety settings to `BLOCK_NONE`. This might sound counter-intuitive, but I did it because I wanted the *Guard* to actually see the malicious attack so it could analyze it, rather than having the API block it before my code could process and log what happened.

If the Guard gives a 'Green Light' (a low risk score), the prompt is passed to **The Brain**, which is Gemini Pro. This is the more powerful model that actually does the work. If the score is too high, the request is blocked immediately.

I also added a feature I call **'Shadow Intelligence'**. It’s a form of adaptive rate limiting. If a user is sending a lot of 'borderline' prompts—nothing that's a direct attack but looks suspicious—the system automatically increases the strictness of the Guard for that specific user.

To wrap it all up, I built a **Security Dashboard** using Streamlit so an admin can see the attacks in real-time, and I wrote a **Red-Teaming script** that automatically tests the system with known injections and generates a professional **PDF Vulnerability Report**. This makes the project 'enterprise-ready' because it shows you can monitor and audit the security of your AI."

---

## 🛠️ Step-by-Step implementation Thought Process

1.  **Thinking Phase:** I realized that "Brain" models (like Gemini Pro) are too expensive and slow to use for security filtering. I needed a "Fast" model (Gemini Flash) to act as a gatekeeper.
2.  **Architecture:** I decided on a **Proxy Pattern**. All requests go through my FastAPI server first. It acts as the "Intelligent Middleware."
3.  **Prompt Engineering:** I focused on turning Gemini Flash into a sensor. Instead of having it chat, I instructed it to only output JSON. This makes it easy for the code to parse the score.
4.  **Logging & Monitoring:** Security is useless without visibility. I implemented a logger that saves every incident to a JSONL file, which the Streamlit dashboard reads.
5.  **Verification:** I knew a project like this needs proof. So I built an automated attack simulator that generates a PDF report to prove the firewall actually works.

---

## ❓ Common Interview Questions & Answers

### 1. "Why did you use two models instead of just one?"
**Answer:** "Efficiency and Safety. Using a massive model like Gemini Pro to check every prompt for security is expensive and adds latency. By using Gemini Flash as 'The Guard,' I get a high-speed security check at a fraction of the cost. It also creates a separation of concerns: the security logic is isolated from the functional logic."

### 2. "Why did you set safety settings to BLOCK_NONE for the Guard model?"
**Answer:** "That was a strategic choice. If the API blocks a request before it reaches my code, I lose the ability to log the attack, analyze it, or identify the attacker for rate-limiting. By setting it to `BLOCK_NONE`, I allow my 'Guard' model to see the full malicious payload, score it accurately, and log it into my dashboard for admin review."

### 3. "What happens if the 'Guard' model itself is tricked?"
**Answer:** "This is a risk known as 'Recursive Injection.' To mitigate this, I used a very strict System Instruction and forced a JSON output format. Because the Guard isn't allowed to 'answer' the user—it only outputs a score—there is much less surface area for it to be manipulated. Additionally, my 'Shadow Intelligence' logic adds a layer of behavior analysis to catch users who are trying to 'probe' the guard."

### 4. "How does the 'Shadow Intelligence' feature work?"
**Answer:** "It's an adaptive threshold logic. If a user's prompt consistently scores between 0.5 and 0.7 (borderline), the system flags that User ID and programmatically updates the system instructions for future calls to be even more strict. This makes it harder for attackers to fine-tune their jailbreaks over multiple attempts."

### 5. "What was the biggest challenge you faced?"
**Answer:** "Handling the JSON response from the Guard model reliably. LLMs can sometimes add extra text or fail to close a bracket. I handled this by using Pydantic for validation and implementing a 'fail-closed' mechanism—meaning if the guard check fails or errors out, the system defaults to blocking the request just to be safe."

### 6. "Which OWASP Top 10 for LLMs does this project address?"
**Answer:** "The main ones are **LLM01: Prompt Injection** and **LLM06: Sensitive Information Disclosure** (by preventing system prompt leakage). By routing everything through a security-hardened middleware, we significantly reduce the risk of these common vulnerabilities."
