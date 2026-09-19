import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

import cognee
from cognee import SearchType

DATASET = "company_brain"
_connected = False

def is_cloud_configured() -> bool:
    """Check if Cognee Cloud is configured and enabled."""
    force_local = os.getenv("USE_LOCAL_COGNEE", "false").lower() in ("true", "1", "yes")
    has_cloud_url = bool(os.getenv("COGNEE_SERVICE_URL"))
    return has_cloud_url and not force_local

async def _ensure_connected():
    global _connected
    if is_cloud_configured() and not _connected:
        await cognee.serve()
        _connected = True

async def _ask_cloud(query: str) -> dict:
    await _ensure_connected()
    answer = await cognee.recall(query_text=query, datasets=[DATASET])
    context = await cognee.recall(query_text=query, datasets=[DATASET], only_context=True)

    # 1. Parse answer text
    ans_text = ""
    if answer and len(answer) > 0:
        first = answer[0]
        if isinstance(first, dict):
            ans_text = first.get("text") or first.get("raw", {}).get("value", "")
        elif hasattr(first, "text"):
            ans_text = first.text
        else:
            ans_text = str(first)
    if not ans_text:
        ans_text = "No answer could be retrieved from Cognee Cloud."

    # 2. Parse context passages / graph connections
    ctx_list = []
    if context and len(context) > 0:
        first_ctx = context[0]
        raw_val = ""
        if isinstance(first_ctx, dict):
            raw_val = first_ctx.get("raw", {}).get("value") or first_ctx.get("text") or ""
        elif hasattr(first_ctx, "text"):
            raw_val = first_ctx.text
        else:
            raw_val = str(first_ctx)

        if raw_val:
            ctx_list = [
                line.strip().lstrip("- ")
                for line in raw_val.split("\n")
                if line.strip() and not line.strip().startswith("`")
            ]

    return {"answer": ans_text, "context": ctx_list}

async def _ask_local(query: str) -> dict:
    answer = await cognee.search(
        query_text=query,
        query_type=SearchType.GRAPH_COMPLETION,
        datasets=[DATASET]
    )
    context = await cognee.search(
        query_text=query,
        query_type=SearchType.GRAPH_COMPLETION,
        datasets=[DATASET],
        only_context=True
    )

    ans_text = ""
    if answer:
        first = answer[0]
        sr = first.get("search_result") if isinstance(first, dict) else getattr(first, "search_result", first)
        if isinstance(sr, list) and len(sr) > 0:
            ans_text = str(sr[0])
        elif sr:
            ans_text = str(sr)
    if not ans_text:
        ans_text = "No answer found in local knowledge graph."

    ctx_list = []
    if context:
        first_ctx = context[0]
        csr = first_ctx.get("search_result") if isinstance(first_ctx, dict) else getattr(first_ctx, "search_result", first_ctx)
        csr_str = str(csr)
        if "Connections:" in csr_str:
            parts = csr_str.split("Connections:")
            connections_block = parts[1].strip()
            lines = [
                line.strip().rstrip("`")
                for line in connections_block.split("\n")
                if line.strip() and not line.strip().startswith("`")
            ]
            ctx_list.extend(lines)
        else:
            ctx_list.append(csr_str)

    return {"answer": ans_text, "context": ctx_list}

async def ask_brain(query: str) -> dict:
    """Route query to Cognee Cloud or local Kuzu graph based on environment configuration."""
    if is_cloud_configured():
        try:
            return await _ask_cloud(query)
        except Exception as e:
            print(f"Cloud query failed: {e}. Falling back to local graph...")
            return await _ask_local(query)
    else:
        return await _ask_local(query)

async def _test():
    res = await ask_brain("Which customer reported the bug discussed in the incident review, and who fixed it?")
    print("ANSWER:", res["answer"])
    print(f"CONTEXT ({len(res['context'])} items):")
    for c in res["context"][:5]:
        print(" -", c)

if __name__ == "__main__":
    asyncio.run(_test())
