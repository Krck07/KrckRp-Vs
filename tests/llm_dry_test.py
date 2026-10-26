"""
Dry tests for LLM Client - Tests that don't require actual AI model running.
These test the structure and logic of the LLM client without making HTTP calls.
"""

import pytest
from unittest.mock import patch, MagicMock
from llm.client import LLMClient

def test_llm_client_instantiation():
    """Test LLMClient can be instantiated correctly"""
    client = LLMClient()

    assert client.narrator_endpoint == "http://localhost:5000"
    assert client.extractor_endpoint == "http://localhost:5001"
    assert client.assistant_endpoint == "http://localhost:5002"

def test_client_attributes():
    """Test that all required attributes are present"""
    client = LLMClient()

    # Check for required methods
    assert hasattr(client, 'call_narrator')
    assert hasattr(client, 'call_extractor')
    assert hasattr(client, 'call_assistant')

@pytest.mark.asyncio
async def test_narrator_method_signature():
    """Test that narrator method has correct signature"""
    client = LLMClient()

    # Should be callable with prompt and optional streaming parameter
    import inspect
    sig = inspect.signature(client.call_narrator)
    params = list(sig.parameters.keys())

    assert 'prompt' in params
    assert 'streaming' in params

@pytest.mark.asyncio
async def test_extractor_method_signature():
    """Test that extractor method has correct signature"""
    client = LLMClient()

    import inspect
    sig = inspect.signature(client.call_extractor)
    params = list(sig.parameters.keys())

    assert 'context' in params
    assert 'player_input' in params

@pytest.mark.asyncio
async def test_assistant_method_signature():
    """Test that assistant method has correct signature"""
    client = LLMClient()

    import inspect
    sig = inspect.signature(client.call_assistant)
    params = list(sig.parameters.keys())

    assert 'request' in params

def test_schema_definitions_exist():
    """Test that schema definitions are available in the schemas module"""
    try:
        from llm.schemas import (
            EXTRACTOR_SCHEMA,
            ASSISTANT_TOOL_SCHEMA,
            CHARACTER_CHANGE_SCHEMA,
            ITEM_CHANGE_SCHEMA,
            LOCATION_CHANGE_SCHEMA,
            RELATIONSHIP_CHANGE_SCHEMA,
            QUEST_CHANGE_SCHEMA,
            FACTION_CHANGE_SCHEMA,
            DETAILED_EXTRACTOR_SCHEMA
        )

        # Basic validation that schemas exist and are dictionaries
        assert isinstance(EXTRACTOR_SCHEMA, dict)
        assert isinstance(ASSISTANT_TOOL_SCHEMA, dict)
        assert isinstance(CHARACTER_CHANGE_SCHEMA, dict)
        assert isinstance(ITEM_CHANGE_SCHEMA, dict)
        assert isinstance(LOCATION_CHANGE_SCHEMA, dict)
        assert isinstance(RELATIONSHIP_CHANGE_SCHEMA, dict)
        assert isinstance(QUEST_CHANGE_SCHEMA, dict)
        assert isinstance(FACTION_CHANGE_SCHEMA, dict)
        assert isinstance(DETAILED_EXTRACTOR_SCHEMA, dict)

    except ImportError:
        pytest.fail("Schema definitions not accessible")

def test_schema_structure():
    """Test that schemas have expected structure"""
    from llm.schemas import EXTRACTOR_SCHEMA

    # Check basic schema structure
    assert "type" in EXTRACTOR_SCHEMA
    assert EXTRACTOR_SCHEMA["type"] == "object"
    assert "properties" in EXTRACTOR_SCHEMA
    assert "changes" in EXTRACTOR_SCHEMA["properties"]

    changes_schema = EXTRACTOR_SCHEMA["properties"]["changes"]
    assert "type" in changes_schema
    assert changes_schema["type"] == "array"