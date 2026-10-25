"""
Integration tests for DatabaseOperations and VectorStore classes.

This file contains integration tests that verify the interaction between
database operations and vector storage.
"""

import unittest
import os
import sys

# Add the project root to Python path so we can import database modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.operations import DatabaseOperations
from database.vector_store import VectorStore
from database.models import Character


class TestDatabaseIntegration(unittest.TestCase):
    """Test suite for integration between database and vector store"""

    def setUp(self):
        """Set up test fixtures."""
        import tempfile
        import os

        # Use a temporary file-based SQLite database for testing to avoid connection issues
        self.temp_db_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db_file.close()

        self.db_path = self.temp_db_file.name
        self.db_ops = DatabaseOperations(self.db_path)
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

    def test_basic_functionality_combination(self):
        """Test that basic functionality works across both modules"""
        # Test storing a character in database
        character_data = {
            'name': 'Integration Test Character',
            'description': 'A character used for integration testing'
        }

        character = self.db_ops.save_character(character_data)
        self.assertIsNotNone(character)

        # Test storing memory in vector store
        memory_id = self.vector_store.store_memory(
            "This is a test narrative about the character",
            {"character_id": character.id, "turn": 1}
        )

        self.assertIsInstance(memory_id, int)
        self.assertGreater(memory_id, 0)

    def test_data_consistency(self):
        """Test that data can be consistently retrieved from both systems"""
        # Create and save a character
        character_data = {
            'name': 'Consistency Test Character',
            'description': 'Character for consistency testing'
        }

        character = self.db_ops.save_character(character_data)

        # Store related memory
        memory_id = self.vector_store.store_memory(
            "Narrative about the consistency test character",
            {"character_id": character.id}
        )

        # Retrieve character from database
        retrieved_char = self.db_ops.SessionLocal().query(Character).filter_by(id=character.id).first()
        self.assertEqual(retrieved_char.name, 'Consistency Test Character')

        # Verify memory exists
        retrieved_memory = self.vector_store.get_memory_by_id(memory_id)
        self.assertIsNotNone(retrieved_memory)


if __name__ == '__main__':
    unittest.main()