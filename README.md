# 🧠 Company Brain (SecondBrain)

> **Grounded Multi-Hop Knowledge Graph Assistant** across internal engineering docs, support tickets, and meeting notes, powered by [Cognee](https://www.cognee.ai/) and [FastAPI](https://fastapi.tiangolo.com/).

---

## 📌 Project Overview

Company Brain connects disparate unstructured company data into a persistent knowledge graph, enabling **grounded multi-hop question answering**:
- **Engineering Docs**: Postmortems, rate-limiting guides, onboarding documentation.
- **Support Tickets**: Customer-filed bug reports and engineer assignments.
- **Meeting Notes**: Incident reviews, sprint planning decisions, and support syncs.

Instead of generic vector similarity, the system traverses entity relationships across documents to answer cross-domain queries (e.g., connecting a customer's ticket to a meeting decision and an engineer's fix).

---

## 🗂️ Project Structure

```text
SecondBrain/
├── ingestion/                 # Knowledge Graph Ingestion Package
│   ├── __init__.py            # Package exports
│   ├── data.py                # Synthetic docs, tickets, and meeting notes (cross-referenced)
│   ├── ingest_cloud.py        # Cognee Cloud ingestion (cognee.serve + cognee.remember)
│   └── ingest_local.py        # Local Kuzu graph ingestion (cognee.add + cognee.cognify)
│
├── server/                    # Backend API & Query Service
│   ├── __init__.py            # Server exports (app, ask_brain)
│   ├── app.py                 # FastAPI application routes (/health, /ask, static mount)
│   └── brain.py               # Query routing engine (Cognee Cloud with local fallback)
│
├── static/                    # Frontend Web UI
│   └── index.html             # Obsidian dark-mode dashboard with sample prompt chips
│
├── main.py                    # Root entrypoint for uvicorn & Render deployment
├── ingest.py                  # CLI runner for local and cloud ingestion
├── smoke_test.py              # Automated smoke test suite (health check + queries)
├── hackathon-PS2.md           # Hackathon problem statement and roadmap
├── requirements.txt           # Python dependencies
├── pyproject.toml             # Project build configuration
└── .env                       # Environment credentials & model configuration
```

---

## ⚙️ Prerequisites & Setup

### 1. Requirements
- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) (recommended) or standard `pip`

### 2. Environment Configuration (`.env`)
Create or configure your `.env` file in the project root:

```env
# LLM & Embedding Settings (Google Gemini)
LLM_PROVIDER=gemini
LLM_MODEL=gemini/gemini-3.5-flash-lite
LLM_API_KEY=your_gemini_api_key
LLM_MAX_PARALLEL_REQUESTS=5

EMBEDDING_PROVIDER=gemini
EMBEDDING_MODEL=gemini/gemini-embedding-001
EMBEDDING_API_KEY=your_gemini_api_key
EMBEDDING_DIMENSIONS=768
EMBEDDING_RATE_LIMIT_ENABLED=true
EMBEDDING_RATE_LIMIT_REQUESTS=90
EMBEDDING_RATE_LIMIT_INTERVAL=60

# Cognee Cloud Configuration
COGNEE_SERVICE_URL=https://tenant-f5102d32-40a2-47f8-a350-2a30adb51ddb.aws.cognee.ai
COGNEE_API_KEY=your_cognee_api_key

# Optional: Set to 'true' to force local Kuzu database instead of Cognee Cloud
# USE_LOCAL_COGNEE=false
```

### 3. Install Dependencies
Using `uv`:
```bash
uv sync
```
Or with `pip`:
```bash
pip install -r requirements.txt
```

---

## 🚀 Quickstart: Run the Project

### Step 1: Ingest Data into the Knowledge Graph

You can choose between **Cognee Cloud** (recommended) or **Local Kuzu DB**:

- **Option A: Cognee Cloud Ingestion (Default)**
  ```bash
  uv run ingest.py
  # or: uv run python -m ingestion.ingest_cloud
  ```
  *Connects to your managed Cognee Cloud tenant, ingests all docs/tickets/notes, and builds the cloud graph.*

- **Option B: Local Kuzu Ingestion**
  ```bash
  uv run ingest.py --target local
  # or: uv run python -m ingestion.ingest_local
  ```
  *Initializes a local Kuzu/Ladybug embedded graph database on your machine.*

---

### Step 2: Start the Web & API Server

Run the development server using `uvicorn`:
```bash
uv run uvicorn main:app --reload
```
The server will start at: **`http://localhost:8000`**

---

### Step 3: Access the Application

- **Web Dashboard**: Open [http://localhost:8000](http://localhost:8000) in your browser.
  - Interactive dark-mode dashboard with built-in 1-click sample prompt chips.
  - View both the **Synthesized Answer** and **Retrieved Graph Context / Triplets**.
- **Health Check**:
  ```bash
  curl http://127.0.0.1:8000/health
  # Returns: {"status":"ok"}
  ```
- **Ask Endpoint**:
  ```bash
  curl -X POST http://127.0.0.1:8000/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "Which customer reported the bug discussed in the incident review, and who fixed it?"}'
  ```

---

### Step 4: Run the Automated Smoke Tests

Verify system health and multi-hop reasoning with the test suite:
```bash
uv run smoke_test.py --url http://127.0.0.1:8000
```
To wake up a remote Render instance before a demo:
```bash
uv run smoke_test.py --url https://your-app.onrender.com --warm-only
```

---

## 🔍 Demo Storylines & Multi-Hop Questions

The dataset in `ingestion/data.py` contains deliberate cross-references designed to test multi-hop knowledge graph retrieval:

| # | Question | Grounded Answer | Multi-Hop Traversal Chain |
|---|:---|:---|:---|
| **1** | **"Which customer reported the bug discussed in the incident review, and who fixed it?"** *(Pitch Rehearsal)* | **Acme Corp** reported it, and **Priya Sharma** fixed it. | Ticket `TCK-101` (Acme Corp) $\rightarrow$ Bug `LOOP-482` $\rightarrow$ Incident Review Note $\rightarrow$ Postmortem Doc $\rightarrow$ Priya Sharma. |
| **2** | **"What is bug LOOP-482 and who was assigned to investigate it?"** | Bug `LOOP-482` is failing webhook retries, assigned to **Priya Sharma**. | Ticket `TCK-101` $\rightarrow$ Bug `LOOP-482` $\rightarrow$ Priya Sharma assignment. |
| **3** | **"Who reviewed the Webhook Retry Incident Postmortem?"** | **Dev Kapoor** (Engineering Manager). | Postmortem Doc $\rightarrow$ Reviewed by Dev Kapoor. |
| **4** | **"Who maintains the Loopwave onboarding guide, and what is their role?"** | **Meera Nair**, Support Lead. | Onboarding Guide Doc $\rightarrow$ Maintained by Meera Nair (Support Lead). |
| **5** | **"What issues or tickets was Rahul Verma assigned to?"** | Ticket `TCK-112` (bug `LOOP-517` / dashboard charts) and bug `LOOP-501`. | Ticket `TCK-112` + Support Sync Note $\rightarrow$ Rahul Verma. |

---

## 🚢 Production Deployment (Render)

1. **Deploy Service**: Create a Web Service on [Render](https://render.com) connected to this repository.
2. **Build Command**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Start Command**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
4. **Environment Variables**: Add all environment variables from `.env` to the Render Dashboard.
