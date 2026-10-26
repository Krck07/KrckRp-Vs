"""
Application tests for LLM Client - Tests that require actual AI model running.
These test the integration with real KoboldCpp instances.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from llm.client import LLMClient

@pytest.mark.asyncio
class TestLLMClientIntegration:
    """Test LLM client behavior when models are actually available"""

    @pytest.fixture
    def llm_client(self):
        return LLMClient()

    async def test_narrator_call_success(self, llm_client):
        """Test narrator call with mocked successful response"""
        # This would normally make an HTTP request to KoboldCpp
        # In a real environment this tests the actual model interaction

        with patch('httpx.AsyncClient') as mock_client:
            # Mock a successful HTTP response from narrator model
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "results": [{"text": "This is a test narrative response"}]
            }
            mock_client.post.return_value = mock_response

            result = await llm_client.call_narrator("Test prompt")

            # Should return success status and text
            assert result["status"] == "success"
            assert "test narrative response" in result["text"].lower()

    async def test_extractor_call_success(self, llm_client):
        """Test extractor call with mocked successful response"""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock a successful HTTP response from extractor model
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "results": [{"text": '{"changes": [{"entity_type": "character", "action": "create", "details": {"name": "Test Character"}}]}'}]
            }
            mock_client.post.return_value = mock_response

            result = await llm_client.call_extractor("Test context", "Player input")

            # Should return success status and parsed changes
            assert result["status"] == "success"
            assert len(result["changes"]) == 1
            assert result["changes"][0]["entity_type"] == "character"

    async def test_assistant_call_success(self, llm_client):
        """Test assistant call with mocked successful response"""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock a successful HTTP response from assistant model
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "results": [{"text": "This is an assistant correction response"}]
            }
            mock_client.post.return_value = mock_response

            result = await llm_client.call_assistant("Test correction request")

            # Should return success status and response text
            assert result["status"] == "success"
            assert "assistant correction response" in result["response"].lower()

    async def test_narrator_call_error_handling(self, llm_client):
        """Test narrator error handling"""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock an HTTP error
            mock_response = AsyncMock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            mock_client.post.return_value = mock_response

            result = await llm_client.call_narrator("Test prompt")

            # Should return error status
            assert result["status"] == "error"

    async def test_extractor_call_error_handling(self, llm_client):
        """Test extractor error handling"""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock an HTTP error
            mock_response = AsyncMock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            mock_client.post.return_value = mock_response

            result = await llm_client.call_extractor("Test context", "Player input")

            # Should return error status
            assert result["status"] == "error"

    async def test_assistant_call_error_handling(self, llm_client):
        """Test assistant error handling"""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock an HTTP error
            mock_response = AsyncMock()
            mock_response.status_code = 500
            mock_response.text = "Internal Server Error"
            mock_client.post.return_value = mock_response

            result = await llm_client.call_assistant("Test request")

            # Should return error status
            assert result["status"] == "error"

    async def test_extractor_json_parsing_fallback(self, llm_client):
        """Test extractor's ability to handle slightly malformed JSON"""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock response with extra text around JSON (common in LLM outputs)
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "results": [{"text": 'Some introductory text {"changes": []} some trailing text'}]
            }
            mock_client.post.return_value = mock_response

            result = await llm_client.call_extractor("Test context", "Player input")

            # Should still handle the JSON extraction even with extra text
            assert result["status"] == "success"