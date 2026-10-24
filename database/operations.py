"""
Database Operations - Handles standard CRUD operations,
strict append-only event logging, and rollback functionality.
"""

import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database.models import Base, World, Campaign, Character, Location, Item, Ability, Faction, Relationship, Quest, Event, Turn, Session
import datetime

class DatabaseOperations:
    def __init__(self, db_path="sqlite:///krckrp.db"):
        """
        Initialize the database operations with a connection to the SQLite database.

        Args:
            db_path (str): Path to the SQLite database file
        """
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.SessionLocal = SessionLocal

    def create_campaign(self, world_id, campaign_name):
        """
        Create a new campaign from a world template.

        Args:
            world_id (int): The ID of the world to base this campaign on
            campaign_name (str): Name for the new campaign

        Returns:
            Campaign: The newly created campaign object
        """
        db = self.SessionLocal()
        try:
            campaign = Campaign(
                world_id=world_id,
                name=campaign_name,
                created_at=datetime.datetime.utcnow()
            )
            db.add(campaign)
            db.commit()
            db.refresh(campaign)
            return campaign
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def save_character(self, character_data):
        """
        Save character data to database.

        Args:
            character_data (dict): Dictionary containing character information

        Returns:
            Character: The saved character object
        """
        db = self.SessionLocal()
        try:
            # If we have an ID, update existing; otherwise create new
            if 'id' in character_data and character_data['id'] is not None:
                character = db.query(Character).filter(Character.id == character_data['id']).first()
                for key, value in character_data.items():
                    setattr(character, key, value)
            else:
                character = Character(**character_data)
                db.add(character)

            db.commit()
            db.refresh(character)
            return character
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def save_location(self, location_data):
        """
        Save location data to database.

        Args:
            location_data (dict): Dictionary containing location information

        Returns:
            Location: The saved location object
        """
        db = self.SessionLocal()
        try:
            if 'id' in location_data and location_data['id'] is not None:
                location = db.query(Location).filter(Location.id == location_data['id']).first()
                for key, value in location_data.items():
                    setattr(location, key, value)
            else:
                location = Location(**location_data)
                db.add(location)

            db.commit()
            db.refresh(location)
            return location
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def save_item(self, item_data):
        """
        Save item data to database.

        Args:
            item_data (dict): Dictionary containing item information

        Returns:
            Item: The saved item object
        """
        db = self.SessionLocal()
        try:
            if 'id' in item_data and item_data['id'] is not None:
                item = db.query(Item).filter(Item.id == item_data['id']).first()
                for key, value in item_data.items():
                    setattr(item, key, value)
            else:
                item = Item(**item_data)
                db.add(item)

            db.commit()
            db.refresh(item)
            return item
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def save_quest(self, quest_data):
        """
        Save quest data to database.

        Args:
            quest_data (dict): Dictionary containing quest information

        Returns:
            Quest: The saved quest object
        """
        db = self.SessionLocal()
        try:
            if 'id' in quest_data and quest_data['id'] is not None:
                quest = db.query(Quest).filter(Quest.id == quest_data['id']).first()
                for key, value in quest_data.items():
                    setattr(quest, key, value)
            else:
                quest = Quest(**quest_data)
                db.add(quest)

            db.commit()
            db.refresh(quest)
            return quest
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def log_event(self, turn_id, source, before_values, after_values):
        """
        Log an event to the append-only event log.

        Args:
            turn_id (int): The turn that generated this event
            source (str): Where the change came from (engine, extractor, etc.)
            before_values (dict): Previous state values
            after_values (dict): New state values

        Returns:
            Event: The logged event object
        """
        db = self.SessionLocal()
        try:
            # Convert None values to actual None for database storage instead of string "None"
            before_str = str(before_values) if before_values is not None else None
            after_str = str(after_values) if after_values is not None else None

            event = Event(
                turn_id=turn_id,
                source=source,
                before_values=before_str,
                after_values=after_str,
                timestamp=datetime.datetime.utcnow()
            )
            db.add(event)
            db.commit()
            db.refresh(event)
            return event
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def rollback_to_turn(self, target_turn):
        """
        Rollback database to a previous turn state.

        Args:
            target_turn (int): The turn number to roll back to

        Returns:
            bool: True if successful, False otherwise
        """
        db = self.SessionLocal()
        try:
            # Get all events for turns greater than or equal to the target turn
            # (we want to delete all events from that turn onward)
            events_to_delete = db.query(Event).filter(Event.turn_id >= target_turn).all()

            # Delete these events (in reverse order to maintain referential integrity)
            for event in reversed(events_to_delete):
                db.delete(event)

            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error during rollback: {e}")
            return False
        finally:
            db.close()

    def get_campaign_data(self, campaign_id):
        """
        Get all data for a specific campaign.

        Args:
            campaign_id (int): The ID of the campaign

        Returns:
            dict: Dictionary containing campaign data including characters, locations, etc.
        """
        db = self.SessionLocal()
        try:
            # This would be expanded to load all related data
            campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

            if not campaign:
                return None

            # Get related entities
            characters = db.query(Character).filter(Character.campaign_id == campaign_id).all()
            locations = db.query(Location).filter(Location.campaign_id == campaign_id).all()
            items = db.query(Item).filter(Item.campaign_id == campaign_id).all()

            return {
                'campaign': campaign,
                'characters': characters,
                'locations': locations,
                'items': items
            }
        except Exception as e:
            print(f"Error getting campaign data: {e}")
            return None
        finally:
            db.close()

    def create_turn(self, player_input, narration_text, campaign_id, session_id):
        """
        Create a new turn in the database.

        Args:
            player_input (str): The player's input text
            narration_text (str): The generated narration
            campaign_id (int): Campaign ID
            session_id (int): Session ID

        Returns:
            Turn: The created turn object
        """
        db = self.SessionLocal()
        try:
            turn = Turn(
                player_input=player_input,
                narration_text=narration_text,
                campaign_id=campaign_id,
                session_id=session_id,
                created_at=datetime.datetime.utcnow()
            )
            db.add(turn)
            db.commit()
            db.refresh(turn)
            return turn
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def create_session(self, campaign_id):
        """
        Create a new session for a campaign.

        Args:
            campaign_id (int): Campaign ID

        Returns:
            Session: The created session object
        """
        db = self.SessionLocal()
        try:
            session = Session(
                campaign_id=campaign_id,
                start_time=datetime.datetime.utcnow(),
                duration=0.0  # Will be updated when session ends
            )
            db.add(session)
            db.commit()
            db.refresh(session)
            return session
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def end_session(self, session_id):
        """
        End a session and update duration.

        Args:
            session_id (int): Session ID to end

        Returns:
            bool: True if successful
        """
        db = self.SessionLocal()
        try:
            session = db.query(Session).filter(Session.id == session_id).first()
            if session:
                session.end_time = datetime.datetime.utcnow()
                # Calculate duration in minutes (simplified)
                if session.start_time:
                    duration = (session.end_time - session.start_time).total_seconds() / 60
                    session.duration = duration
                db.commit()
                return True
        except Exception as e:
            print(f"Error ending session: {e}")
            db.rollback()
            return False
        finally:
            db.close()

# Example usage
def save_new_character(character_data):
    db_ops = DatabaseOperations()
    return db_ops.save_character(character_data)