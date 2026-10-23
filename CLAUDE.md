# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

KrckRP is a local, single-player AI-narrated role-playing game platform built with Python and FastAPI. The system follows a clear separation of concerns:

- **Engine Layer**: Core game logic that simulates world state, resolves actions using rules, manages quests, tracks character states and relationships
- **Storage Layer**: SQLite database for persistent state, vector store for episodic memory  
- **LLM Layer**: KoboldCpp instances serving narrator and extractor models via HTTP API
- **Frontend**: Vite + Vue.js web UI served by FastAPI backend

## Core Components

### Engine Modules (`engine/` directory)
- `rules.py`: Action resolution engine with outcome tier calculation based on capability vs difficulty
- `quests.py`: Quest management system for emergent quest creation and lifecycle 
- `pipeline.py`: Main turn processing pipeline coordinating all engine components
- `context_builder.py`: Assembles narrator prompts from game state

### Data Model Structure
The core entities include World, Campaign (save slot), Character, Location, Item, Ability, Faction, Relationship, Quest, Event, Turn, and Session. All mutable state belongs to a campaign.

## Development Commands

- Run tests: `python -m pytest tests/` or run specific test files like `python test_rules_simple.py`
- Execute the main application: `python main.py`  
- Lint code: Use Python linter (flake8, pylint) with configured rules
- Run individual test modules: `python tests/rules_engine/test_rules_comprehensive.py`

## Key Patterns

1. **Data-driven Configuration**: World-specific rules and abilities are loaded from JSON files rather than hard-coded values
2. **Event Logging**: All state changes are logged as immutable events for undo/rewind functionality  
3. **Deterministic Engine**: The engine makes all truth decisions, while LLMs provide narrative language
4. **Modular Architecture**: Each component has clear separation of concerns and interfaces

## File Organization

- `engine/`: Core game logic (rules, quests, pipeline, context)
- `database/`: Database models and operations  
- `llm/`: LLM client integrations
- `tests/`: Test suites for engine components
- `world_configs/`: Per-world rule configurations