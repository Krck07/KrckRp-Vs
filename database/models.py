"""
Database Models - Defines the relational schemas for:
World, Campaign, Character, Location, Item, Faction, Quest, Event log.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

# Example models (more would be defined based on full spec)
class World(Base):
    __tablename__ = 'worlds'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    premise = Column(Text)
    genre = Column(String(50))
    tone_settings = Column(Text)

class Campaign(Base):
    __tablename__ = 'campaigns'
    
    id = Column(Integer, primary_key=True)
    world_id = Column(Integer, ForeignKey('worlds.id'))
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime)

class Character(Base):
    __tablename__ = 'characters'
    
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    location_id = Column(Integer, ForeignKey('locations.id'))

class Location(Base):
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    name = Column(String(100), nullable=False)
    description = Column(Text)

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    name = Column(String(100), nullable=False)
    description = Column(Text)

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    turn_id = Column(Integer)
    source = Column(String(50))  # engine, extractor, player_correction, etc.
    before_values = Column(Text)
    after_values = Column(Text)
    timestamp = Column(DateTime)

# Additional models would be defined here based on full requirements