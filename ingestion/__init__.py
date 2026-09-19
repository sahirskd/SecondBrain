"""
Ingestion module for SecondBrain.
Supports both local Kuzu knowledge graph build and Cognee Cloud ingestion.
"""

from ingestion.data import ALL_ITEMS, DOCS, TICKETS, NOTES
from ingestion.ingest_cloud import ingest_cloud
from ingestion.ingest_local import ingest_local

__all__ = ["ALL_ITEMS", "DOCS", "TICKETS", "NOTES", "ingest_cloud", "ingest_local"]
