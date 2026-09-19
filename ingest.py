import asyncio
from dotenv import load_dotenv
load_dotenv()

import cognee
from cognee import SearchType
from data import ALL_ITEMS

DATASET = "company_brain"

async def ingest():
    await cognee.prune.prune_data()
    await cognee.prune.prune_system(metadata=True)

    await cognee.add(ALL_ITEMS, dataset_name=DATASET)
    print("Data ingested.")
    try:
        result = await cognee.cognify(datasets=[DATASET])
        print("COGNIFY RESULT:", result)
    except Exception as e:
        print("COGNIFY FAILED:", repr(e))
        raise

    print("Graph built.")

    results = await cognee.search(
        query_text="What relationships exist involving Priya Sharma?",
        query_type=SearchType.GRAPH_COMPLETION,
        datasets=[DATASET],
    )
    print("INSIGHTS COUNT:", len(results))
    for r in results:
        print(r)

if __name__ == "__main__":
    asyncio.run(ingest())