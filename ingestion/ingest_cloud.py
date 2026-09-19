import argparse
import asyncio
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

import cognee
from ingestion.data import get_all_items

DATASET = "company_brain"

async def ingest_cloud(data_dir: str | Path | None = None):
    items = get_all_items(data_dir)
    print("Connecting to Cognee Cloud...")
    await cognee.serve()

    print(f"Ingesting {len(items)} document(s) into Cognee Cloud dataset '{DATASET}'...")
    await cognee.remember(items, dataset_name=DATASET)
    print("Knowledge graph successfully built on Cognee Cloud.")

    print("\nVerifying cloud recall...")
    results = await cognee.recall(
        query_text="What relationships exist involving Priya Sharma?",
        datasets=[DATASET],
    )
    print(f"Cloud recall verified ({len(results)} items returned):")
    for r in results:
        text = r.get("text") if isinstance(r, dict) else str(r)
        print(" -", text)

    await cognee.disconnect()
    print("Disconnected from Cognee Cloud.")
    return {
        "status": "success",
        "target": "cloud",
        "dataset": DATASET,
        "documents_count": len(items),
        "recall_verified": len(results) > 0,
        "message": f"Successfully ingested {len(items)} document(s) into Cognee Cloud knowledge graph."
    }

if __name__ == "__main__":
    asyncio.run(ingest_cloud())
