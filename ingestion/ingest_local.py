import asyncio
from dotenv import load_dotenv
load_dotenv()

import cognee
from cognee import SearchType
from ingestion.data import ALL_ITEMS

DATASET = "company_brain"

async def ingest_local():
    print("Initializing local Cognee graph ingestion (Kuzu/Ladybug)...")
    try:
        await cognee.disconnect()
    except Exception:
        pass

    print("Pruning previous local database...")
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    print(f"Adding {len(ALL_ITEMS)} items to local dataset '{DATASET}'...")
    await cognee.add(ALL_ITEMS, dataset_name=DATASET)
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

if __name__ == "__main__":
    asyncio.run(ingest_local())
