import asyncio
from dotenv import load_dotenv
load_dotenv()

import cognee
from cognee import SearchType

DATASET = "company_brain"

async def ask_brain(query: str) -> dict:
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

    # 1. Extract and clean answer
    ans_text = ""
    if answer:
        first = answer[0]
        sr = first.get("search_result") if isinstance(first, dict) else getattr(first, "search_result", first)
        if isinstance(sr, list) and len(sr) > 0:
            ans_text = str(sr[0])
        elif sr:
            ans_text = str(sr)
    if not ans_text:
        ans_text = "No answer could be retrieved from the knowledge graph."

    # 2. Extract and format context / triplets
    ctx_list = []
    if context:
        first_ctx = context[0]
        csr = first_ctx.get("search_result") if isinstance(first_ctx, dict) else getattr(first_ctx, "search_result", first_ctx)
        csr_str = str(csr)
        
        # If there is a Connections section, prioritize showing those relationship triplets
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

    return {
        "answer": ans_text,
        "context": ctx_list,
    }

async def _test():
    result = await ask_brain(
        "Which customer reported the bug discussed in the incident review, and who fixed it?"
    )
    print("ANSWER:", result["answer"])
    print("CONTEXT (count = %d):" % len(result["context"]))
    for c in result["context"]:
        print(" -", c)

if __name__ == "__main__":
    asyncio.run(_test())