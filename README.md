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
├── data/                      # Stored Knowledge Documents (.md, .txt, .json)
│   ├── incident_postmortem.md
│   └── customer_issues_and_sprint_notes.md
│
├── ingestion/                 # Knowledge Graph Ingestion Package
│   ├── __init__.py            # Package exports
│   ├── data.py                # Dynamic document loader & fallback dataset
│   ├── ingest_cloud.py        # Cognee Cloud ingestion (cognee.serve + cognee.remember)
│   └── ingest_local.py        # Local Kuzu graph ingestion (cognee.add + cognee.cognify)
│
├── server/                    # Backend API & Admin Service
│   ├── __init__.py            # Server exports (app, ask_brain)
│   ├── app.py                 # FastAPI application routes (/health, /ask, /admin, /api/*)
│   └── brain.py               # Query routing engine (Cognee Cloud with local fallback)
│
├── static/                    # Frontend Web Dashboards
│   ├── index.html             # User Q&A Dashboard (dark-mode, graph visualizer, feedback)
│   └── admin.html             # Dedicated Admin Ingestion Console (upload, preview, rebuild)
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

### Step 1: Start the Web & API Server

Run the server using `uvicorn`:
```bash
uv run uvicorn main:app --reload
```
The server will start at: **`http://localhost:8000`**

---

### Step 2: Ingest Data into the Knowledge Graph

You can ingest documents either via the **Admin Portal UI** or using the **CLI**:

- **Option A: Via Admin Portal (Recommended)**
  Open [http://localhost:8000/admin](http://localhost:8000/admin), drag-and-drop documents into the dropzone, and click **"Run Ingestion Pipeline"**.

- **Option B: Cognee Cloud Ingestion (CLI)**
  ```bash
  uv run ingest.py
  ```
  *Reads all documents from `data/` and builds the cloud graph.*

- **Option C: Local Kuzu Ingestion (CLI)**
  ```bash
  uv run ingest.py --target local
  ```
  *Initializes a local Kuzu/Ladybug embedded graph database from `data/`.*

---

### Step 3: Access the Application

- **User Q&A Dashboard**: [http://localhost:8000](http://localhost:8000)
  - Interactive dark-mode dashboard with built-in 1-click sample prompt chips.
  - View the **Synthesized Answer**, **Retrieved Graph Subgraph Triplets**, and **Interactive Topology Visualizer**.
  - Rate answers with **Thumbs Up / Down** feedback buttons.

- **Admin Ingestion Console**: [http://localhost:8000/admin](http://localhost:8000/admin) (or `/admin.html`)
  - **Drag & Drop Upload**: Upload `.md`, `.txt`, `.json`, or `.csv` files into the knowledge store.
  - **Document Inspector**: View file metadata, live text preview, or delete documents.
  - **Rebuild Engine**: Trigger Cognee Cloud or Local Kuzu rebuild with live terminal event streaming.

- **REST API Endpoints**:
  - `GET /health` — Health check & system posture (`{"status":"ok","cloud_configured":true,"documents_count":2}`).
  - `POST /ask` — Query the knowledge graph (`{"question": "..."}`).
  - `GET /api/documents` — List all active knowledge store documents.
  - `POST /api/upload` — Upload files via multipart form data (`files: UploadFile`).
  - `GET /api/documents/{filename}` — Preview raw document text content.
  - `DELETE /api/documents/{filename}` — Delete document from knowledge store.
  - `POST /api/ingest` — Trigger knowledge graph rebuild (`{"target": "cloud" | "local" | "auto"}`).

---

### Step 4: Run the Automated Smoke Tests

Verify system health, document availability, and multi-hop reasoning with the test suite:
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

---

## 🔮 Future Architecture & Production Roadmap

### 1. Dedicated Multi-Modal Admin Ingestion Panel
For enterprise production rollout, data ingestion moves beyond pre-seeded files to an **Omnichannel Admin Control Panel**:
- **Any-File Universal Ingestion**: Drag-and-drop support for **PDFs, Word Docs, PowerPoint Presentations (PPT/PPTX), Markdown (MD), Spreadsheets, and Audio/Meeting Recordings**.
- **Multi-Modal Processing Pipeline**:
  - **Audio/Meeting Syncs**: Automated speech-to-text transcription via Whisper / Gemini Audio API, converting recorded standups and incident debriefs directly into timestamped entity triplets.
  - **Structured & Semi-Structured Docs**: Layout-aware parsing of slide decks, tables, and architecture diagrams into semantic graph nodes.
- **Enterprise Connectors**: Scheduled background sync jobs pulling incrementally from Google Drive, Confluence, Notion, and Jira webhooks.

### 2. Role-Based Access Control (RBAC) & NodeSet Scoping
- **Query-Time Role Filtering**: Multi-tenant dataset partitioning where query traversals are constrained to user authorization levels (e.g., engineers access codebase postmortems, HR retains salary/personnel confidentiality).
- **Continuous Learning & Auditability**: Feedback ingestion (`improve()` API) linked to thumbs-up/down ratings, plus verifiable audit logs tracing every synthesized claim back to source document hashes.

