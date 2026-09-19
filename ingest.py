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
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Path to folder containing documents to ingest (default: 'data')"
    )
    args = parser.parse_args()
    if args.target == "local":
        asyncio.run(ingest_local(args.data_dir))
    else:
        asyncio.run(ingest_cloud(args.data_dir))

if __name__ == "__main__":
    main()