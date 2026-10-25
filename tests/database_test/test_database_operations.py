"""
Unit tests for DatabaseOperations class in database/operations.py

This file contains comprehensive tests for all methods of the DatabaseOperations class,
ensuring proper functionality for CRUD operations, event logging, and rollback.
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the project root to Python path so we can import database modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.operations import DatabaseOperations
from database.models import Base, World, Campaign, Character, Location, Item, Ability, Faction, Relationship, Quest, Event, Turn, Session


class TestDatabaseOperations(unittest.TestCase):
    """Test suite for DatabaseOperations class"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Use an in-memory SQLite database for testing
        self.db_path = ":memory:"
        self.db_ops = DatabaseOperations(self.db_path)

    def tearDown(self):
        """Clean up after each test."""
        pass

    def test_init_database_connection(self):
        """Test that the DatabaseOperations initializes with proper connection"""
        self.assertIsNotNone(self.db_ops.engine)
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(self.db_ops.engine)
        table_names = inspector.get_table_names()
        expected_tables = [
            'worlds', 'campaigns', 'characters', 'locations',
            'items', 'abilities', 'factions', 'relationships',
            'quests', 'events', 'turns', 'sessions'
        ]
        for table in expected_tables:
            self.assertIn(table, table_names)

    def test_create_campaign(self):
        """Test create_campaign method"""
        # First we need to create a world
        db = self.db_ops.SessionLocal()
        try:
            world = World(
                name="Test World",
                premise="A test world for testing",
                genre="Fantasy"
            )
            db.add(world)
            db.commit()
            db.refresh(world)

            # Now create campaign from this world
            campaign = self.db_ops.create_campaign(world.id, "Test Campaign")

            # Verify the campaign was created correctly
            self.assertIsNotNone(campaign)
            self.assertEqual(campaign.world_id, world.id)
            self.assertEqual(campaign.name, "Test Campaign")
            self.assertIsNotNone(campaign.created_at)
        finally:
            db.close()

    def test_save_character(self):
        """Test save_character method"""
        # Test creating a new character
        character_data = {
            'name': 'Test Character',
            'description': 'A test character for testing purposes',
            'role': 'npc'
        }

        character = self.db_ops.save_character(character_data)

        # Verify the character was created correctly
        self.assertIsNotNone(character)
        self.assertEqual(character.name, 'Test Character')
        self.assertEqual(character.description, 'A test character for testing purposes')
        self.assertEqual(character.role, 'npc')

    def test_save_location(self):
        """Test save_location method"""
        # Test creating a new location
        location_data = {
            'name': 'Test Location',
            'description': 'A test location for testing purposes'
        }

        location = self.db_ops.save_location(location_data)

        # Verify the location was created correctly
        self.assertIsNotNone(location)
        self.assertEqual(location.name, 'Test Location')
        self.assertEqual(location.description, 'A test location for testing purposes')

    def test_save_item(self):
        """Test save_item method"""
        # Test creating a new item
        item_data = {
            'name': 'Test Item',
            'description': 'A test item for testing purposes'
        }

        item = self.db_ops.save_item(item_data)

        # Verify the item was created correctly
        self.assertIsNotNone(item)
        self.assertEqual(item.name, 'Test Item')
        self.assertEqual(item.description, 'A test item for testing purposes')

    def test_save_quest(self):
        """Test save_quest method"""
        # Test creating a new quest
        quest_data = {
            'title': 'Test Quest',
            'summary': 'A test quest for testing purposes'
        }

        quest = self.db_ops.save_quest(quest_data)

        # Verify the quest was created correctly
        self.assertIsNotNone(quest)
        self.assertEqual(quest.title, 'Test Quest')
        self.assertEqual(quest.summary, 'A test quest for testing purposes')

    def test_log_event(self):
        """Test log_event method"""
        # Test logging an event
        event = self.db_ops.log_event(
            turn_id=1,
            source="engine",
            before_values={"test": "before"},
            after_values={"test": "after"}
        )

        # Verify the event was logged correctly
        self.assertIsNotNone(event)
        self.assertEqual(event.turn_id, 1)
        self.assertEqual(event.source, "engine")
        self.assertEqual(event.before_values, "{'test': 'before'}")
        self.assertEqual(event.after_values, "{'test': 'after'}")

    def test_rollback_to_turn(self):
        """Test rollback_to_turn method"""
        # Create some events
        self.db_ops.log_event(1, "engine", {"a": 1}, {"a": 2})
        self.db_ops.log_event(2, "engine", {"b": 1}, {"b": 2})
        self.db_ops.log_event(3, "engine", {"c": 1}, {"c": 2})

        # Rollback to turn 2 (should delete events from turn 2 and higher)
        success = self.db_ops.rollback_to_turn(2)

        # Verify rollback worked
        self.assertTrue(success)

    def test_get_campaign_data(self):
        """Test get_campaign_data method"""
        # First create a campaign
        db = self.db_ops.SessionLocal()
        try:
            world = World(
                name="Test World",
                premise="A test world for testing",
                genre="Fantasy"
            )
            db.add(world)
            db.commit()
            db.refresh(world)

            campaign = self.db_ops.create_campaign(world.id, "Test Campaign")

            # Get the campaign data
            campaign_data = self.db_ops.get_campaign_data(campaign.id)

            # Verify the data was retrieved correctly
            self.assertIsNotNone(campaign_data)
            self.assertEqual(campaign_data['campaign'].id, campaign.id)
        finally:
            db.close()

    def test_create_turn(self):
        """Test create_turn method"""
        # First create a session and campaign
        db = self.db_ops.SessionLocal()
        try:
            world = World(
                name="Test World",
                premise="A test world for testing",
                genre="Fantasy"
            )
            db.add(world)
            db.commit()
            db.refresh(world)

            campaign = self.db_ops.create_campaign(world.id, "Test Campaign")
            session = self.db_ops.create_session(campaign.id)

            # Create a turn
            turn = self.db_ops.create_turn(
                player_input="test input",
                narration_text="test narration",
                campaign_id=campaign.id,
                session_id=session.id
            )

            # Verify the turn was created correctly
            self.assertIsNotNone(turn)
            self.assertEqual(turn.player_input, "test input")
            self.assertEqual(turn.narration_text, "test narration")
            self.assertEqual(turn.campaign_id, campaign.id)
            self.assertEqual(turn.session_id, session.id)
        finally:
            db.close()

    def test_create_session(self):
        """Test create_session method"""
        # First create a campaign
        db = self.db_ops.SessionLocal()
        try:
            world = World(
                name="Test World",
                premise="A test world for testing",
                genre="Fantasy"
            )
            db.add(world)
            db.commit()
            db.refresh(world)

            campaign = self.db_ops.create_campaign(world.id, "Test Campaign")

            # Create a session
            session = self.db_ops.create_session(campaign.id)

            # Verify the session was created correctly
            self.assertIsNotNone(session)
            self.assertEqual(session.campaign_id, campaign.id)
            self.assertIsNotNone(session.start_time)
            self.assertEqual(session.duration, 0.0)
        finally:
            db.close()

    def test_end_session(self):
        """Test end_session method"""
        # First create a session
        db = self.db_ops.SessionLocal()
        try:
            world = World(
                name="Test World",
                premise="A test world for testing",
                genre="Fantasy"
            )
            db.add(world)
            db.commit()
            db.refresh(world)

            campaign = self.db_ops.create_campaign(world.id, "Test Campaign")
            session = self.db_ops.create_session(campaign.id)

            # End the session
            success = self.db_ops.end_session(session.id)

            # Verify the session was ended correctly
            self.assertTrue(success)
        finally:
            db.close()

    def test_save_character_update(self):
        """Test updating an existing character"""
        # First create a character
        initial_data = {
            'name': 'Original Name',
            'description': 'Original description'
        }

        character = self.db_ops.save_character(initial_data)
        char_id = character.id

        # Update the character data
        updated_data = {
            'id': char_id,
            'name': 'Updated Name',
            'description': 'Updated description'
        }

        updated_char = self.db_ops.save_character(updated_data)

        # Verify the update worked correctly
        self.assertEqual(updated_char.id, char_id)
        self.assertEqual(updated_char.name, 'Updated Name')
        self.assertEqual(updated_char.description, 'Updated description')

    def test_save_location_update(self):
        """Test updating an existing location"""
        # First create a location
        initial_data = {
            'name': 'Original Location',
            'description': 'Original description'
        }

        location = self.db_ops.save_location(initial_data)
        loc_id = location.id

        # Update the location data
        updated_data = {
            'id': loc_id,
            'name': 'Updated Location',
            'description': 'Updated description'
        }

        updated_loc = self.db_ops.save_location(updated_data)

        # Verify the update worked correctly
        self.assertEqual(updated_loc.id, loc_id)
        self.assertEqual(updated_loc.name, 'Updated Location')
        self.assertEqual(updated_loc.description, 'Updated description')

    def test_save_item_update(self):
        """Test updating an existing item"""
        # First create an item
        initial_data = {
            'name': 'Original Item',
            'description': 'Original description'
        }

        item = self.db_ops.save_item(initial_data)
        item_id = item.id

        # Update the item data
        updated_data = {
            'id': item_id,
            'name': 'Updated Item',
            'description': 'Updated description'
        }

        updated_item = self.db_ops.save_item(updated_data)

        # Verify the update worked correctly
        self.assertEqual(updated_item.id, item_id)
        self.assertEqual(updated_item.name, 'Updated Item')
        self.assertEqual(updated_item.description, 'Updated description')

    def test_save_quest_update(self):
        """Test updating an existing quest"""
        # First create a quest
        initial_data = {
            'title': 'Original Quest',
            'summary': 'Original summary'
        }

        quest = self.db_ops.save_quest(initial_data)
        quest_id = quest.id

        # Update the quest data
        updated_data = {
            'id': quest_id,
            'title': 'Updated Quest',
            'summary': 'Updated summary'
        }

        updated_quest = self.db_ops.save_quest(updated_data)

        # Verify the update worked correctly
        self.assertEqual(updated_quest.id, quest_id)
        self.assertEqual(updated_quest.title, 'Updated Quest')
        self.assertEqual(updated_quest.summary, 'Updated summary')


if __name__ == '__main__':
    unittest.main()