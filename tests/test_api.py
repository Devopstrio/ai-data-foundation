from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from aidatafoundation.api.endpoints import get_engine
from aidatafoundation.core.engine import DataFoundationEngine
from aidatafoundation.main import app
from aidatafoundation.storage.vector_adapter import VectorStorageAdapter

client = TestClient(app)

def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_ingest_data() -> None:
    mock_db = AsyncMock(spec=VectorStorageAdapter)
    mock_db.upsert_vectors.return_value = ["v1", "v2"]
    
    engine = DataFoundationEngine(mock_db)
    app.dependency_overrides[get_engine] = lambda: engine
    
    response = client.post("/v1/data/ingest", json={
        "source_id": "doc-1",
        "content": "This is a very long text that gets chunked.",
        "metadata": {"author": "mani"}
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["chunks_created"] == 1

@pytest.mark.asyncio
async def test_search_data() -> None:
    mock_db = AsyncMock(spec=VectorStorageAdapter)
    mock_db.search_similar.return_value = [
        {"chunk_id": "c1", "source_id": "s1", "content": "mock result", "score": 0.99}
    ]
    
    engine = DataFoundationEngine(mock_db)
    app.dependency_overrides[get_engine] = lambda: engine
    
    response = client.post("/v1/data/search", json={
        "query": "how to deploy",
        "top_k": 1
    })
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["content"] == "mock result"
