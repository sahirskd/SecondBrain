import asyncio
from dotenv import load_dotenv
load_dotenv()

import cognee
from ingestion.data import ALL_ITEMS

DATASET = "company_brain"

async def ingest_cloud():
    print("Connecting to Cognee Cloud...")
    await cognee.serve()

    print(f"Ingesting {len(ALL_ITEMS)} items into Cognee Cloud dataset '{DATASET}'...")
    await cognee.remember(ALL_ITEMS, dataset_name=DATASET)
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

if __name__ == "__main__":
    asyncio.run(ingest_cloud())
