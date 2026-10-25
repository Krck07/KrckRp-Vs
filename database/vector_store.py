"""
Vector Store - Manages local semantic storage (ChromaDB/FAISS/sqlite-vec).
Handles embedding generation and similarity retrieval for episodic memory and lore.
"""

import os
import json
from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
import sqlite3

class VectorStore:
    def __init__(self, db_path=":memory:"):
        """
        Initialize the vector store with a connection to SQLite database.

        Args:
            db_path (str): Path to the SQLite database file for storing embeddings and metadata
        """
        # Convert SQLAlchemy URL format to actual path if needed
        if db_path.startswith("sqlite:///"):
            self.db_path = db_path[10:]  # Remove 'sqlite:///' prefix
        else:
            self.db_path = db_path

        # Initialize embedding model (using a lightweight model)
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Warning: Could not load sentence transformer, falling back to basic implementation. Error: {e}")
            self.model = None

        # Create tables if they don't exist (just in case)
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database with required tables."""
        try:
            # Ensure we have a fresh connection for initialization
            conn = sqlite3.connect(self.db_path)

            # Check existing tables before creating them
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            all_tables_before = cursor.fetchall()

            # Create memories table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text_content TEXT NOT NULL,
                    metadata TEXT,  -- JSON string of metadata
                    embedding BLOB,  -- Binary representation of vector
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create embeddings table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS embeddings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_id INTEGER,
                    vector_data BLOB,  -- Binary representation of embedding vector
                    FOREIGN KEY (memory_id) REFERENCES memories(id)
                )
            ''')

            conn.commit()

            # Verify tables were created by checking again
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            all_tables_after = cursor.fetchall()
            print(f"DEBUG: Tables after initialization: {all_tables_after}")

            conn.close()
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise

    def store_memory(self, text_content: str, metadata: Dict[str, Any] = None):
        """
        Store text content with metadata in the vector database.

        Args:
            text_content (str): The text to embed and store
            metadata (dict): Associated information (turn number, characters, location)

        Returns:
            int: ID of stored memory
        """
        try:
            # Use a fresh connection for storage operations
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Store the basic content with metadata first
            if metadata is None:
                metadata_str = '{}'
            else:
                metadata_str = json.dumps(metadata)

            cursor.execute('''
                INSERT INTO memories (text_content, metadata)
                VALUES (?, ?)
            ''', (text_content, metadata_str))

            memory_id = cursor.lastrowid

            # Generate embedding if model is available
            if self.model:
                try:
                    embedding = self.model.encode(text_content)
                    # Convert numpy array to binary format for storage
                    embedding_blob = embedding.tobytes()

                    cursor.execute('''
                        INSERT INTO embeddings (memory_id, vector_data)
                        VALUES (?, ?)
                    ''', (memory_id, embedding_blob))
                except Exception as e:
                    print(f"Warning: Could not generate embedding. Error: {e}")
            else:
                # Even without embedding, store the memory
                pass

            conn.commit()
            conn.close()

            return memory_id

        except Exception as e:
            if 'conn' in locals():
                try:
                    conn.rollback()
                    conn.close()
                except:
                    pass
            print(f"Error storing memory: {e}")
            raise

    def retrieve_similar(self, query_text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve semantically similar memories.

        Args:
            query_text (str): Query to search for similarities
            limit (int): Maximum number of results to return

        Returns:
            List of dictionaries containing memory entries and similarity scores
        """
        try:
            # If we don't have a model, return empty list or basic text search
            if not self.model:
                return []

            # Generate embedding for query
            query_embedding = self.model.encode(query_text)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get all stored embeddings and calculate similarity scores
            cursor.execute('''
                SELECT m.id, m.text_content, m.metadata, e.vector_data
                FROM memories m
                LEFT JOIN embeddings e ON m.id = e.memory_id
                WHERE e.vector_data IS NOT NULL
            ''')

            results = []
            for row in cursor.fetchall():
                memory_id, text_content, metadata_str, vector_blob = row

                # Convert binary embedding back to numpy array
                if vector_blob:
                    stored_embedding = np.frombuffer(vector_blob, dtype=np.float32)

                    # Calculate cosine similarity
                    dot_product = np.dot(query_embedding, stored_embedding)
                    norm_query = np.linalg.norm(query_embedding)
                    norm_stored = np.linalg.norm(stored_embedding)

                    if norm_query > 0 and norm_stored > 0:
                        similarity = dot_product / (norm_query * norm_stored)

                        # Convert metadata string back to dict
                        try:
                            metadata = json.loads(metadata_str) if metadata_str else {}
                        except:
                            metadata = {}

                        results.append({
                            'memory_id': memory_id,
                            'text_content': text_content,
                            'metadata': metadata,
                            'similarity_score': float(similarity)
                        })

            # Sort by similarity score descending and limit results
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            return results[:limit]

        except Exception as e:
            print(f"Error retrieving similar memories: {e}")
            return []
        finally:
            try:
                conn.close()
            except:
                pass

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using local model.

        Args:
            text (str): Text to embed

        Returns:
            List of float values representing the vector
        """
        if self.model:
            try:
                result = self.model.encode(text)
                # Handle both numpy arrays and lists properly
                if hasattr(result, 'tolist'):
                    return result.tolist()
                else:
                    return list(result)
            except Exception as e:
                print(f"Error generating embedding: {e}")
                return []
        else:
            # Fallback for when no model is available
            # This could be replaced with a simpler hashing approach or similar method
            return []

    def delete_memory(self, memory_id: int) -> bool:
        """
        Delete a specific memory entry.

        Args:
            memory_id (int): ID of the memory to delete

        Returns:
            bool: True if deleted successfully
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check if memory exists first
            cursor.execute('SELECT id FROM memories WHERE id = ?', (memory_id,))
            existing_memory = cursor.fetchone()

            if existing_memory is None:
                # Memory doesn't exist, but we consider this a successful "no-op"
                return True

            # Delete from embeddings table first due to foreign key constraint
            cursor.execute('DELETE FROM embeddings WHERE memory_id = ?', (memory_id,))

            # Then delete from memories table
            cursor.execute('DELETE FROM memories WHERE id = ?', (memory_id,))

            conn.commit()
            conn.close()

            return True
        except Exception as e:
            print(f"Error deleting memory: {e}")
            return False  # Return False on actual errors (but not non-existent IDs)

    def get_memory_by_id(self, memory_id: int) -> Dict[str, Any]:
        """
        Retrieve a specific memory by ID.

        Args:
            memory_id (int): ID of the memory to retrieve

        Returns:
            Dictionary with memory content and metadata
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, text_content, metadata
                FROM memories
                WHERE id = ?
            ''', (memory_id,))

            row = cursor.fetchone()
            if row:
                memory_id, text_content, metadata_str = row

                try:
                    metadata = json.loads(metadata_str) if metadata_str else {}
                except:
                    metadata = {}

                return {
                    'id': memory_id,
                    'text_content': text_content,
                    'metadata': metadata
                }
            return None

        except Exception as e:
            print(f"Error retrieving memory: {e}")
            return None
        finally:
            try:
                conn.close()
            except:
                pass

# Example usage
def store_narrative(memory_text, metadata):
    vector_store = VectorStore()
    return vector_store.store_memory(memory_text, metadata)

def search_memories(query_text, limit=5):
    vector_store = VectorStore()
    return vector_store.retrieve_similar(query_text, limit)