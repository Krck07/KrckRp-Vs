"""
Tests for LLM Client functionality
"""

import pytest
from unittest.mock import AsyncMock, patch
from llm.client import LLMClient

@pytest.fixture
def llm_client():
    return LLMClient()

@pytest.mark.asyncio
async def test_narrator_call(llm_client):
    """Test narrator call method"""
    with patch('httpx.AsyncClient') as mock_client:
        # Mock the HTTP response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{"text": "Test narrative response"}]
        }
        mock_client.post.return_value = mock_response

        result = await llm_client.call_narrator("Test prompt")

        assert result["status"] == "success"
        assert "Test narrative response" in result["text"]

@pytest.mark.asyncio
async def test_extractor_call(llm_client):
    """Test extractor call method"""
    with patch('httpx.AsyncClient') as mock_client:
        # Mock the HTTP response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{"text": '{"changes": []}'}]
        }
        mock_client.post.return_value = mock_response

        result = await llm_client.call_extractor("Test context", "Player input")

        assert result["status"] == "success"
        assert result["changes"] == []

@pytest.mark.asyncio
async def test_assistant_call(llm_client):
    """Test assistant call method"""
    with patch('httpx.AsyncClient') as mock_client:
        # Mock the HTTP response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{"text": "Assistant response"}]
        }
        mock_client.post.return_value = mock_response

        result = await llm_client.call_assistant("Test request")

        assert result["status"] == "success"
        assert "Assistant response" in result["response"]

# Test that the client can be instantiated correctly
def test_client_instantiation():
    """Test LLMClient instantiation"""
    client = LLMClient()
    assert client.narrator_endpoint == "http://localhost:5000"
    assert client.extractor_endpoint == "http://localhost:5001"
    assert client.assistant_endpoint == "http://localhost:5002"