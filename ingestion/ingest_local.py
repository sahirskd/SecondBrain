import argparse
import asyncio
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

import cognee
from cognee import SearchType
from ingestion.data import get_all_items

DATASET = "company_brain"

async def ingest_local(data_dir: str | Path | None = None):
    items = get_all_items(data_dir)
    print("Initializing local Cognee graph ingestion (Kuzu/Ladybug)...")
    try:
        await cognee.disconnect()
    except Exception:
        pass

    print("Pruning previous local database...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    print(f"Adding {len(items)} document(s) to local dataset '{DATASET}'...")
    await cognee.add(items, dataset_name=DATASET)
    print("Items added. Cognifying (extracting entities & graph relationships)...")

    result = await cognee.cognify(datasets=[DATASET])
    print("Local knowledge graph built successfully.")

    print("\nVerifying local graph completion...")
    results = await cognee.search(
        query_text="What relationships exist involving Priya Sharma?",
        query_type=SearchType.GRAPH_COMPLETION,
        datasets=[DATASET],
    )
    print(f"Local graph search returned {len(results)} items:")
    for r in results:
        sr = r.get("search_result") if isinstance(r, dict) else getattr(r, "search_result", r)
        print(" -", sr)

    return {
        "status": "success",
        "target": "local",
        "dataset": DATASET,
        "documents_count": len(items),
        "recall_verified": len(results) > 0,
        "message": f"Successfully built local Kuzu knowledge graph with {len(items)} document(s)."
    }

if __name__ == "__main__":
    asyncio.run(ingest_local())
