# PS-2 Plan — Team of 2, Build Window 11:30–2:15 (2h45m)

## Use Case (lock this immediately, don't debate)
**Engineering/Support "Company Brain"** — matches the slide's own example exactly (docs + tickets + meeting notes), minimizes ambiguity, easy to fake realistic data fast.

- **Docs**: 4–5 markdown files — product spec, API reference, onboarding wiki, incident postmortem
- **Tickets**: 6–8 JSON/text support tickets — bug reports, feature requests
- **Meeting notes**: 4–5 short notes — sprint standups, incident review, roadmap discussion

**Critical**: seed *deliberate cross-references* across the three types (same bug ID in a ticket, a meeting note, and a postmortem doc; same person named in a ticket and a meeting). This is what makes multi-hop possible — don't let this be an afterthought.

---

## Stack
- **Cognee** — ingestion + graph/vector build + grounded Q&A (core requirement)
- **Graph DB**: start with **Kuzu** (zero-config default) → swap to **Neo4j Aura free tier** once pipeline works (sponsor credit + visual graph for demo)
- **Backend**: FastAPI, one `/ask` endpoint
- **Frontend**: minimal chat UI (Streamlit is fastest, or a single HTML page)
- **Deploy**: Render (sponsor requirement)
- **LLM key**: OpenAI (or whatever you have) for `LLM_API_KEY` — get this ready now, first `cognify()` run needs it

---

## Core API calls
```python
import cognee
from cognee import SearchType

await cognee.add([doc1, doc2, ticket1, ...], dataset_name="company_brain")
await cognee.cognify(datasets=["company_brain"])

result = await cognee.search(
    query_text="Which customer reported the bug discussed in the incident review, and who fixed it?",
    query_type=SearchType.GRAPH_COMPLETION,
    datasets=["company_brain"],
)
```
`GRAPH_COMPLETION` is what satisfies "grounded + multi-hop" directly — it traverses triplets, not just vector similarity. Also expose `SearchType.INSIGHTS` on a debug view to literally show judges the relationship triplets behind an answer.

**Neo4j swap (do this last, ~5 min)**:
```bash
pip install "cognee[neo4j]"
```
```env
GRAPH_DATABASE_PROVIDER=neo4j
GRAPH_DATABASE_URL=neo4j+s://<aura-instance>.databases.neo4j.io
GRAPH_DATABASE_USERNAME=neo4j
GRAPH_DATABASE_PASSWORD=<aura-password>
```
Cognee is DB-agnostic — same code, just re-run `cognify()` against the new store.

---

## Time-box (2 people)

| Time | Person A (data + Cognee) | Person B (backend + deploy) |
|---|---|---|
| 11:30–11:50 | Write all synthetic docs/tickets/notes with cross-refs | Scaffold FastAPI + push empty app to Render (de-risk deploy early) |
| 11:50–12:30 | `pip install cognee`, run `add()` + `cognify()` on Kuzu, verify graph builds | Build `/ask` endpoint stub, minimal chat UI |
| 12:30–1:30 | Wire real `GRAPH_COMPLETION` search into `/ask`, test 3–4 questions incl. one multi-hop | Connect UI → backend, get end-to-end working locally |
| 1:30–1:50 | Swap Kuzu → Neo4j Aura, re-run cognify, confirm same queries still work | Add "show retrieved context/triplets" panel next to answer (grounding proof) |
| 1:50–2:15 | Final deploy to Render, smoke test live URL, prep pitch talking points | Same — both hands on deploy/bugfix |

---

## Judge-facing differentiators
1. **Grounding is visible, not claimed** — show retrieved triplets/source snippet alongside every answer (their own requirement, and directly scores "Technical Understanding")
2. **One rehearsed multi-hop query**, stated explicitly in the pitch: "watch this — the answer connects a ticket → a meeting decision → a person, none of which live in the same table"
3. **Neo4j graph visual** (Aura browser screenshot or embedded iframe) — direct appeal to Neo4j judges
4. **Live Render URL**, not localhost — "production standards" criterion
5. Keep dataset small and clean (15–20 items) — judges reward "Scope & Prioritisation," not size

## Risk flags
- Don't attempt Neo4j Aura first — it's an easy 5-min swap later; wasting setup time on it early risks a zero-demo outcome. Kuzu-first is your insurance policy.
- First `cognify()` call can be slow (LLM calls for entity/relationship extraction) — kick it off the moment you have even 3 sample docs, don't wait for the full dataset.
- Have your OpenAI key ready before 11:30 starts.