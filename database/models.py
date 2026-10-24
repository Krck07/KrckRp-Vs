"""
Database Models - Defines the relational schemas for:
World, Campaign, Character, Location, Item, Faction, Quest, Event log.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()

# World Model - the reusable template
class World(Base):
    __tablename__ = 'worlds'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    premise = Column(Text)
    genre = Column(String(50))
    tone_settings = Column(Text)
    narration_style = Column(Text)
    content_settings = Column(JSON)  # JSON for flexible settings
    rule_configuration = Column(Text)  # JSON or serialized config
    seed_locations = Column(Text)  # JSON array of locations
    seed_characters = Column(Text)  # JSON array of characters
    seed_factions = Column(Text)  # JSON array of factions

# Campaign Model - one playthrough of a World
class Campaign(Base):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)
    world_id = Column(Integer, ForeignKey('worlds.id'))
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    # Additional campaign-specific fields can be added as needed

# Character Model - both player character and NPCs
class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    role = Column(String(50))  # player, npc, etc.
    personality = Column(Text)
    speech_style = Column(Text)
    goals = Column(Text)
    location_id = Column(Integer, ForeignKey('locations.id'))
    stats = Column(JSON)  # JSON for flexible stat system
    status = Column(Text)
    inventory = Column(Text)  # JSON array of item IDs or names
    relationships = Column(Text)  # JSON array of relationship data
    visibility_flags = Column(JSON)  # JSON for knowledge/visibility settings
    portrait_path = Column(String(255))

# Location Model - name, description, parent/children, connections to other locations with distances/travel time, tags, who is present.
class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    parent_location_id = Column(Integer, ForeignKey('locations.id'))  # for hierarchical locations
    connections = Column(Text)  # JSON array of {location_id, distance, travel_time}
    tags = Column(JSON)  # list of string tags
    who_is_present = Column(Text)  # JSON array of character IDs

# Item Model - name, description, properties/tags, owner or location.
class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    properties = Column(JSON)  # JSON for flexible item properties
    tags = Column(JSON)  # list of string tags
    owner_id = Column(Integer, ForeignKey('characters.id'))  # if owned by a character
    location_id = Column(Integer, ForeignKey('locations.id'))  # if in a location

# Ability Model - a spell, skill or power, linked to an ability group
class Ability(Base):
    __tablename__ = 'abilities'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    ability_group = Column(String(50))  # e.g., Offense, Defense, etc.
    cost = Column(JSON)  # JSON for flexible cost system
    requirements = Column(Text)
    progression = Column(Text)  # how it improves over time
    world_id = Column(Integer, ForeignKey('worlds.id'))

# Faction Model - name, goals, relationships to other factions and to the player.
class Faction(Base):
    __tablename__ = 'factions'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    goals = Column(Text)
    relationships = Column(Text)  # JSON for faction relationship data

# Relationship Model - directed link between two characters or factions
class Relationship(Base):
    __tablename__ = 'relationships'

    id = Column(Integer, primary_key=True)
    source_entity_id = Column(Integer)  # character or faction ID
    target_entity_id = Column(Integer)  # character or faction ID
    relationship_type = Column(String(50))  # e.g., trusts, fears, owes a debt
    attitude_value = Column(Float)  # numerical value for attitude (e.g. -10 to +10)
    tags = Column(JSON)  # additional metadata about the relationship

# Quest Model - quests that emerge and update during play
class Quest(Base):
    __tablename__ = 'quests'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    summary = Column(Text)
    giver_character_ids = Column(JSON)  # JSON array of character IDs
    related_locations = Column(JSON)  # JSON array of location IDs
    objectives = Column(Text)  # JSON array of objective data
    state = Column(String(50))  # proposed, active, completed, failed, abandoned, expired
    hooks_consequences = Column(Text)
    origin_turn_id = Column(Integer)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))

# Event Model - immutable record of something that happened
class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    turn_id = Column(Integer)  # The turn that generated this event
    source = Column(String(50))  # engine, extractor, player_correction, assistant_correction, world_creation
    before_values = Column(Text)  # JSON string of previous state values
    after_values = Column(Text)  # JSON string of new state values
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Turn Model - one player input plus the resulting narration, with a link to the events it produced.
class Turn(Base):
    __tablename__ = 'turns'

    id = Column(Integer, primary_key=True)
    player_input = Column(Text)
    narration_text = Column(Text)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    session_id = Column(Integer, ForeignKey('sessions.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Session Model - a continuous stretch of play
class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)
    duration = Column(Float)  # in minutes or hours

# Create relationships
Campaign.world = relationship("World", back_populates="campaigns")
World.campaigns = relationship("Campaign", order_by=Campaign.id, back_populates="world")

Character.location = relationship("Location")
Location.characters = relationship("Character", order_by=Character.id)

Character.items = relationship("Item")
Item.owner = relationship("Character")