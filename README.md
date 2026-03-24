# DataAgent Core: Autonomous B2B Data Analytics Engine

Most AI portfolio projects are simple text wrappers around an LLM API. DataAgent Core is a fully autonomous, fault-tolerant Python execution engine. 

It takes plain-English business questions, translates them into executable Python data science code (using pandas and matplotlib), securely executes that code in an isolated ephemeral cloud container, and streams the standard output and base64-encoded charts back to the client.

## 🏗 System Architecture

The backend handles multi-turn conversational memory, secure file mounting, and autonomous error recovery without requiring human intervention.

```text
[Client UI] 
   | (JSON: Query + Chat History + Session ID)
   v
[FastAPI Router] ---> [Security Interceptor: Blocks malicious prompt injections]
   |
   +---> [Groq API / Llama 3.3 70B] ---> Generates Pandas/Matplotlib Python Code
   |
   v
[E2B Cloud Sandbox] ---> Mounts Dataset & Executes Untrusted Code
   |
   +---> On Success: Bash POSIX pipe extracts binary PNGs and Stdout.
   |
   +---> On Failure: Triggers Self-Healing Loop (Feeds traceback to LLM to self-correct).
   |
   +---> On Timeout: Triggers Silent Resurrection (Spins up new container, remounts data).
   |
   v
[Client UI] (Returns JSON Payload: Text, Code, Base64 Images)
```

## 🚀 Core Engineering Features

**1. The Self-Healing Execution Loop**
LLMs hallucinate. When Llama 3 generates invalid Python code (e.g., referencing a missing dataframe column), the system does not crash. The backend catches the container runtime error, appends the traceback to the conversational context, and autonomously prompts the LLM to write a fix. It loops up to three times before gracefully failing.

**2. Silent Sandbox Resurrection**
Cloud execution containers are ephemeral and will time out. If a user leaves the application and returns later, the backend intercepts the dead connection, provisions a fresh E2B sandbox, reads the raw dataset from local persistent storage, remounts it to the new remote container, and executes the query seamlessly. The user never sees a timeout error.

**3. POSIX-Level Binary Extraction**
Relying on high-level Python SDKs to intercept graphical outputs is fragile. Instead, the backend forces the LLM to write absolute file paths, and then utilizes native Linux `bash` commands (`base64` piped through `tr`) inside the sandbox to convert graphical chart data into clean string payloads for a single-trip frontend response.

**4. Prompt Injection Guardrails**
The system is locked down to strictly data analysis. Context-injected system prompts paired with a FastApi router interceptor immediately neutralize malicious requests (e.g., web scraping, system wiping, network pinging) before they ever reach the code execution environment.

## 🛠 Tech Stack

*   **Framework:** Python 3, FastAPI
*   **Data Validation:** Pydantic V2
*   **LLM Inference:** Groq API (Llama-3.3-70b-versatile)
*   **Secure Compute:** E2B Code Interpreter SDK
*   **Data Science:** Pandas, Matplotlib

## ⚙️ Local Development Setup

1. Clone the repository and navigate into the directory.
2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install fastapi uvicorn pydantic python-multipart python-dotenv openai e2b_code_interpreter pandas
```
4. Create a `.env` file in the root directory and add your API keys:
```text
GROQ_API_KEY=your_groq_api_key_here
E2B_API_KEY=your_e2b_api_key_here
```
5. Start the FastAPI server:
```bash
uvicorn main:app --reload --port 8000
```
