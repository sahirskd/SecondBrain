import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from server.brain import ask_brain, is_cloud_configured
from ingestion.ingest_cloud import ingest_cloud
from ingestion.ingest_local import ingest_local

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

app = FastAPI(title="SecondBrain API", description="Company Brain Knowledge Graph Q&A & Ingestion Console")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    context: list[str] = []

class IngestRequest(BaseModel):
    target: str = "auto"  # "cloud", "local", or "auto"

@app.get("/health")
def health():
    return {
        "status": "ok",
        "cloud_configured": is_cloud_configured(),
        "documents_count": len([f for f in DATA_DIR.iterdir() if f.is_file() and not f.name.startswith(".")])
    }

@app.get("/admin")
def admin_redirect():
    return RedirectResponse(url="/admin.html")

# --- Document Management Endpoints ---

@app.get("/api/documents")
def list_documents():
    """List all documents currently stored in the knowledge data folder."""
    docs = []
    if DATA_DIR.exists():
        for f in sorted(DATA_DIR.iterdir(), key=lambda x: x.name):
            if f.is_file() and not f.name.startswith("."):
                stat = f.stat()
                docs.append({
                    "filename": f.name,
                    "size_bytes": stat.st_size,
                    "modified_at": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    "extension": f.suffix.lower().lstrip(".") or "txt"
                })
    return {
        "documents": docs,
        "count": len(docs),
        "cloud_configured": is_cloud_configured()
    }

@app.post("/api/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """Upload one or more documents into the data directory."""
    saved = []
    for file in files:
        safe_name = Path(file.filename).name
        dest_path = DATA_DIR / safe_name
        with dest_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved.append({
            "filename": safe_name,
            "size_bytes": dest_path.stat().st_size
        })
    return {
        "status": "success",
        "message": f"Successfully uploaded {len(saved)} document(s).",
        "uploaded": saved
    }

@app.get("/api/documents/{filename}")
def get_document_content(filename: str):
    """Retrieve text content of a document for preview in the admin console."""
    safe_name = Path(filename).name
    target = DATA_DIR / safe_name
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="Document not found")
    try:
        content = target.read_text(encoding="utf-8", errors="replace")
        return {
            "filename": safe_name,
            "content": content,
            "size_bytes": target.stat().st_size
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {e}")

@app.delete("/api/documents/{filename}")
def delete_document(filename: str):
    """Delete a document from the data directory."""
    safe_name = Path(filename).name
    target = DATA_DIR / safe_name
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="Document not found")
    target.unlink()
    return {
        "status": "success",
        "message": f"Document '{safe_name}' deleted successfully."
    }

# --- Knowledge Graph Ingestion Endpoint ---

@app.post("/api/ingest")
async def trigger_ingestion(req: IngestRequest = IngestRequest()):
    """Trigger Cognee knowledge graph ingestion for all documents in data/."""
    try:
        target = req.target.lower()
        if target == "cloud" or (target == "auto" and is_cloud_configured()):
            res = await ingest_cloud(DATA_DIR)
        else:
            res = await ingest_local(DATA_DIR)
        return res
    except Exception as e:
        return {
            "status": "error",
            "message": f"Ingestion pipeline failed: {str(e)}"
        }

# --- Q&A Endpoint ---

@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    try:
        res = await ask_brain(req.question)
        return AskResponse(
            answer=res.get("answer") or "No answer returned.",
            context=res.get("context") or []
        )
    except Exception as e:
        return AskResponse(
            answer=f"Error querying knowledge graph: {str(e)}",
            context=[]
        )

# Mount static files (HTML frontend)
static_dir = Path(__file__).resolve().parent.parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

