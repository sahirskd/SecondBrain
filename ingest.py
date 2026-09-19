"""
Ingestion CLI for SecondBrain.
Allows targeting either Cognee Cloud or local Kuzu graph database.
Usage:
    uv run ingest.py                 # Ingests to Cognee Cloud (default)
    uv run ingest.py --target local  # Ingests to local Kuzu graph
"""

import argparse
import asyncio
from ingestion.ingest_cloud import ingest_cloud
from ingestion.ingest_local import ingest_local

def main():
    parser = argparse.ArgumentParser(description="Ingest SecondBrain data into Cognee (Cloud or Local)")
    parser.add_argument(
        "--target",
        choices=["cloud", "local"],
        default="cloud",
        help="Target Cognee instance: 'cloud' (default) or 'local'"
    )
    args = parser.parse_args()
    if args.target == "local":
        asyncio.run(ingest_local())
    else:
        asyncio.run(ingest_cloud())

if __name__ == "__main__":
    main()