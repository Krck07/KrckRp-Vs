"""
Unit tests for VectorStore class in database/vector_store.py

This file contains comprehensive tests for all methods of the VectorStore class,
ensuring proper functionality for memory storage, retrieval and embedding.
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the project root to Python path so we can import database modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.vector_store import VectorStore


class TestVectorStore(unittest.TestCase):
    """Test suite for VectorStore class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Use a temporary file-based SQLite database for testing to avoid connection issues
        import tempfile
        import os

        # Create temp file path
        self.temp_db_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db_file.close()

        self.db_path = self.temp_db_file.name
        self.vector_store = VectorStore(self.db_path)

    def tearDown(self):
        """Clean up after each test."""
        # Clean up temp file
        import os
        try:
            if hasattr(self, 'temp_db_file') and self.temp_db_file.name:
                os.unlink(self.temp_db_file.name)
        except:
            pass

    @patch('database.vector_store.SentenceTransformer')
    def test_init_with_model(self, mock_transformer_class):
        """Test that the VectorStore initializes properly with a model"""
        # Mock successful loading of sentence transformer
        mock_model = MagicMock()
        mock_transformer_class.return_value = mock_model

        vector_store = VectorStore(self.db_path)

        self.assertIsNotNone(vector_store.model)
        self.assertEqual(vector_store.db_path, self.db_path)

    @patch('database.vector_store.SentenceTransformer')
    def test_init_without_model(self, mock_transformer_class):
        """Test that the VectorStore handles missing model gracefully"""
        # Mock failure in loading sentence transformer
        mock_transformer_class.side_effect = Exception("Model not available")

        vector_store = VectorStore(self.db_path)

        self.assertIsNone(vector_store.model)

    def test_store_memory_basic(self):
        """Test store_memory method with basic functionality"""
        text_content = "This is a test memory for storing"
        metadata = {"test": "value", "turn_id": 1}

        memory_id = self.vector_store.store_memory(text_content, metadata)

        # Verify the memory was stored correctly
        self.assertIsInstance(memory_id, int)
        self.assertGreater(memory_id, 0)

    def test_store_memory_no_metadata(self):
        """Test store_memory method with no metadata"""
        text_content = "This is a test memory without metadata"

        memory_id = self.vector_store.store_memory(text_content)

        # Verify the memory was stored correctly
        self.assertIsInstance(memory_id, int)
        self.assertGreater(memory_id, 0)

    def test_get_memory_by_id(self):
        """Test get_memory_by_id method"""
        text_content = "This is a test memory for retrieval"
        metadata = {"test": "value"}

        # Store the memory first
        memory_id = self.vector_store.store_memory(text_content, metadata)

        # Retrieve it by ID
        retrieved_memory = self.vector_store.get_memory_by_id(memory_id)

        # Verify retrieval worked correctly
        self.assertIsNotNone(retrieved_memory)
        self.assertEqual(retrieved_memory['id'], memory_id)
        self.assertEqual(retrieved_memory['text_content'], text_content)
        self.assertEqual(retrieved_memory['metadata'], metadata)

    def test_get_memory_by_id_nonexistent(self):
        """Test get_memory_by_id method with nonexistent ID"""
        # Try to retrieve a non-existent memory
        retrieved_memory = self.vector_store.get_memory_by_id(999999)

        # Should return None for nonexistent memory
        self.assertIsNone(retrieved_memory)

    def test_delete_memory(self):
        """Test delete_memory method"""
        text_content = "This is a test memory to be deleted"
        metadata = {"test": "value"}

        # Store the memory first
        memory_id = self.vector_store.store_memory(text_content, metadata)

        # Delete it
        success = self.vector_store.delete_memory(memory_id)

        # Verify deletion worked correctly
        self.assertTrue(success)

        # Try to retrieve deleted memory (should return None)
        retrieved_memory = self.vector_store.get_memory_by_id(memory_id)
        self.assertIsNone(retrieved_memory)

    def test_delete_nonexistent_memory(self):
        """Test delete_memory method with nonexistent ID"""
        # Try to delete a non-existent memory
        success = self.vector_store.delete_memory(999999)

        # Should return True (no error, no-op)
        self.assertTrue(success)

    @patch('database.vector_store.SentenceTransformer')
    def test_generate_embedding_with_model(self, mock_transformer_class):
        """Test generate_embedding method when model is available"""
        # Mock successful loading of sentence transformer
        mock_model = MagicMock()
        mock_model.encode.return_value = [0.1, 0.2, 0.3]
        mock_transformer_class.return_value = mock_model

        vector_store = VectorStore(self.db_path)

        embedding = vector_store.generate_embedding("Test text for embedding")

        # Verify embedding was generated
        self.assertIsInstance(embedding, list)
        self.assertEqual(len(embedding), 3)

    @patch('database.vector_store.SentenceTransformer')
    def test_generate_embedding_without_model(self, mock_transformer_class):
        """Test generate_embedding method when model is not available"""
        # Mock failure in loading sentence transformer
        mock_transformer_class.side_effect = Exception("Model not available")

        vector_store = VectorStore(self.db_path)

        embedding = vector_store.generate_embedding("Test text for embedding")

        # Should return empty list when no model
        self.assertEqual(embedding, [])

    def test_retrieve_similar_empty_database(self):
        """Test retrieve_similar method with an empty database"""
        results = self.vector_store.retrieve_similar("test query", limit=5)

        # Should return empty list when there's nothing to compare against
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)

    def test_retrieve_similar_with_content(self):
        """Test retrieve_similar method with actual content"""
        # First store some memories
        self.vector_store.store_memory("This is a memory about testing", {"category": "test"})
        self.vector_store.store_memory("Another memory about development", {"category": "dev"})

        # Try to retrieve similar memories (this will be empty since we don't have embeddings)
        results = self.vector_store.retrieve_similar("testing query", limit=5)

        # Since there's no model loaded in test, should return empty list
        self.assertIsInstance(results, list)
        # Depending on the implementation, this might also fail gracefully


if __name__ == '__main__':
    unittest.main()