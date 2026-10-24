# Database Module Documentation

This document provides a reference for the database components implemented in KrckRP. Each method is described with its arguments and return values to facilitate testing and usage.

## Models Overview

The database models define the relational schemas for all game entities:
- World: Reusable world template
- Campaign: One playthrough of a world 
- Character: Player character or NPCs
- Location: Game locations
- Item: Objects in the game
- Ability: Spells, skills, powers
- Faction: Groups of characters
- Relationship: Directed relationships between entities
- Quest: Emergent quests
- Event: Immutable state change logs
- Turn: Player inputs and narrations
- Session: Continuous play periods

## Database Operations Methods

### `DatabaseOperations.__init__(self, db_path="sqlite:///krckrp.db")`
Initialize database connection and create tables if they don't exist.
- **db_path** (str): Path to SQLite database file

### `create_campaign(self, world_id, campaign_name)`
Create a new campaign from a world template.
- **world_id** (int): ID of the source world
- **campaign_name** (str): Name for the new campaign
- Returns: Campaign object

### `save_character(self, character_data)`
Save character data to database.
- **character_data** (dict): Character information including id if updating existing
- Returns: Character object

### `save_location(self, location_data)`  
Save location data to database.
- **location_data** (dict): Location information including id if updating existing
- Returns: Location object

### `save_item(self, item_data)`
Save item data to database. 
- **item_data** (dict): Item information including id if updating existing
- Returns: Item object

### `save_quest(self, quest_data)`  
Save quest data to database.
- **quest_data** (dict): Quest information including id if updating existing
- Returns: Quest object

### `log_event(self, turn_id, source, before_values, after_values)`
Log an event to the append-only event log.
- **turn_id** (int): Turn that generated this event
- **source** (str): Source of change (engine, extractor, etc.)
- **before_values** (dict): Previous state values 
- **after_values** (dict): New state values
- Returns: Event object

### `rollback_to_turn(self, target_turn)`
Rollback database to a previous turn state.
- **target_turn** (int): Turn number to rollback to
- Returns: bool indicating success

### `get_campaign_data(self, campaign_id)`  
Get all data for a specific campaign.
- **campaign_id** (int): ID of the campaign
- Returns: dict with campaign and related entities

### `create_turn(self, player_input, narration_text, campaign_id, session_id)`
Create a new turn in database.
- **player_input** (str): Player's input text
- **narration_text** (str): Generated narrative  
- **campaign_id** (int): Campaign ID
- **session_id** (int): Session ID
- Returns: Turn object

### `create_session(self, campaign_id)`
Create a new session for a campaign.
- **campaign_id** (int): Campaign ID
- Returns: Session object

### `end_session(self, session_id)`  
End a session and update duration.
- **session_id** (int): Session ID to end
- Returns: bool indicating success

## Vector Store Methods

### `VectorStore.__init__(self, db_path="sqlite:///vector_store.db")`
Initialize vector store with SQLite database connection.
- **db_path** (str): Path to SQLite database file

### `store_memory(self, text_content, metadata)`
Store text content with metadata in vector database.
- **text_content** (str): Text to embed and store
- **metadata** (dict): Associated information 
- Returns: int ID of stored memory

### `retrieve_similar(self, query_text, limit=5)`  
Retrieve semantically similar memories.
- **query_text** (str): Query text for similarity search
- **limit** (int): Maximum results to return
- Returns: List of dictionaries with memory entries and similarity scores

### `generate_embedding(self, text)` 
Generate embedding vector for text.
- **text** (str): Text to embed
- Returns: List of float values representing the vector

### `delete_memory(self, memory_id)`  
Delete a specific memory entry.  
- **memory_id** (int): ID of memory to delete
- Returns: bool indicating success

### `get_memory_by_id(self, memory_id)`
Retrieve a specific memory by ID.
- **memory_id** (int): ID of memory to retrieve
- Returns: Dictionary with memory content and metadata