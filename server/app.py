import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from server.brain import ask_brain

app = FastAPI(title="SecondBrain API", description="Company Brain Knowledge Graph Q&A")

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

@app.get("/health")
def health():
    return {"status": "ok"}

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
