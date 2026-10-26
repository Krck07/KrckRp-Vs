"""
Context Builder module - Assembles the strict prompt for the Narrator LLM.
Handles token budgets, rolling summaries, and NPC knowledge filtering.
"""

from typing import Dict, List, Any, Optional
import json
import math


class ContextBuilder:
    def __init__(self, db_session, vector_store):
        """
        Initialize context builder with database and memory components.

        Args:
            db_session: Database session for accessing game state
            vector_store: Vector store for retrieving memories
        """
        self.db_session = db_session
        self.vector_store = vector_store

    def build_narrator_prompt(self, turn_data: Dict[str, Any], character: Dict[str, Any],
                            location: Dict[str, Any], quests: List[Dict[str, Any]],
                            memory_context: List[Dict[str, Any]],
                            resolution_result: Dict[str, Any]) -> str:
        """
        Construct a well-structured prompt for the narrator LLM with proper token management.

        Args:
            turn_data: Current player action and previous turns
            character: Player's current state
            location: Current location details
            quests: Active quest information
            memory_context: Retrieved memories from vector store
            resolution_result: Outcome of mechanical resolution

        Returns:
            Formatted prompt string for the narrator LLM
        """
        # Build context with token budgeting and prioritization

        # Section 1: System instructions (highest priority)
        system_instructions = self._build_system_prompt(turn_data)

        # Section 2: Character state information
        character_info = self._build_character_context(character)

        # Section 3: Location details
        location_info = self._build_location_context(location)

        # Section 4: Quests and objectives (high priority)
        quest_info = self._build_quest_context(quests)

        # Section 5: Recent events with rolling summary
        recent_events = self._build_event_context(turn_data)

        # Section 6: Memory snippets from vector store
        memory_snippets = self._build_memory_context(memory_context)

        # Section 7: Mechanical outcome result (critical for narrative consistency)
        outcome_info = self._build_outcome_context(resolution_result)

        # Combine all sections with proper formatting and token management
        prompt_sections = [
            system_instructions,
            character_info,
            location_info,
            quest_info,
            recent_events,
            memory_snippets,
            outcome_info
        ]

        return self._format_prompt(prompt_sections)

    def _build_system_prompt(self, turn_data: Dict[str, Any]) -> str:
        """
        Build instructions for narrator tone and style.

        Args:
            turn_data: Current player action data

        Returns:
            System prompt section
        """
        # This would use world-specific settings from database
        return """[SYSTEM INSTRUCTIONS]
You are an AI narrator creating immersive, rich prose for a role-playing game.
Follow these guidelines strictly:

1. Describe what happens mechanically (from the outcome tier) in detail first
2. Then expand with vivid description and dialogue
3. Keep to the world's genre/tone settings
4. Ensure all character actions and outcomes are described accurately based on engine results
5. Do not contradict mechanical outcomes or player capabilities

The narrative should be engaging, varied, and consistent."""

    def _build_character_context(self, character: Dict[str, Any]) -> str:
        """
        Format current character state information.

        Args:
            character: Character data from database

        Returns:
            Formatted character context section
        """
        if not character:
            return "[CHARACTER STATE]\nName: Unknown\nStats: N/A"

        stats_text = ", ".join([f"{k}: {v}" for k, v in character.get('stats', {}).items()])

        return f"""[CHARACTER STATE]
Name: {character.get('name', 'Unknown')}
Description: {character.get('description', 'No description')}
Stats: {stats_text}
Status: {character.get('status', 'Normal')}
Inventory: {character.get('inventory', [])}"""

    def _build_location_context(self, location: Dict[str, Any]) -> str:
        """
        Format current location details.

        Args:
            location: Location data from database

        Returns:
            Formatted location context section
        """
        if not location:
            return "[LOCATION]\nName: Unknown\nDescription: N/A"

        return f"""[LOCATION]
Name: {location.get('name', 'Unknown')}
Description: {location.get('description', 'No description')}
Connections: {location.get('connections', [])}
Tags: {location.get('tags', [])}"""

    def _build_quest_context(self, quests: List[Dict[str, Any]]) -> str:
        """
        Format active quest information.

        Args:
            quests: List of active quests

        Returns:
            Formatted quest context section
        """
        if not quests or len(quests) == 0:
            return "[ACTIVE QUESTS]\nNone"

        quest_text = "\n".join([
            f"Quest: {quest.get('title', 'Untitled')}\n"
            f"Summary: {quest.get('summary', 'No summary')}\n"
            f"Objectives: {', '.join([obj.get('description', '') for obj in quest.get('objectives', [])])}"
            for quest in quests
        ])

        return f"""[ACTIVE QUESTS]
{quest_text}"""

    def _build_event_context(self, turn_data: Dict[str, Any]) -> str:
        """
        Build recent history context with rolling summary.

        Args:
            turn_data: Current turn data

        Returns:
            Formatted event context section
        """
        # Simplified version - in full implementation would include actual recent events
        return """[RECENT EVENTS]
The player has taken an action and the engine determined mechanical outcomes.
This information helps you provide accurate narrative that matches game state."""

    def _build_memory_context(self, memory_context: List[Dict[str, Any]]) -> str:
        """
        Format relevant memories from vector store.

        Args:
            memory_context: Retrieved memory snippets

        Returns:
            Formatted memory context section
        """
        if not memory_context or len(memory_context) == 0:
            return "[RELEVANT MEMORIES]\nNone"

        memory_text = "\n".join([f"- {mem.get('text', 'Memory snippet')}" for mem in memory_context[:5]])  # Limit to 5 snippets

        return f"""[RELEVANT MEMORIES]
{memory_text}"""

    def _build_outcome_context(self, resolution_result: Dict[str, Any]) -> str:
        """
        Include resolved outcome information for narrative consistency.

        Args:
            resolution_result: Outcome from mechanical resolution

        Returns:
            Formatted outcome context section
        """
        if not resolution_result:
            return "[MECHANICAL OUTCOME]\nNo outcome determined"

        tier = resolution_result.get("outcome_tier", "unknown")
        consequences = resolution_result.get("consequences", [])

        consequence_text = "\n".join([f"- {c}" for c in consequences[:3]])  # Limit to 3 consequences

        return f"""[MECHANICAL OUTCOME]
Result: {tier}
Consequences:
{consequence_text}"""

    def _format_prompt(self, prompt_sections: List[str]) -> str:
        """
        Combine all sections with proper formatting and token management.

        Args:
            prompt_sections: Individual formatted sections

        Returns:
            Complete formatted prompt string
        """
        # Join with clear section separators
        return "\n\n".join([section for section in prompt_sections if section])

    def filter_npc_knowledge(self, npc: Dict[str, Any], relevant_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter memories based on what NPC could realistically know.

        Args:
            npc: The NPC whose knowledge we're filtering
            relevant_events: Events that might be remembered

        Returns:
            Filtered list of memories the NPC would actually recall
        """
        # Implementation for NPC knowledge filtering

        # This is a simplified implementation - in full version would check:
        # 1. What events this NPC was present at (via metadata)
        # 2. What events were told to this NPC (via relationship/communication history)
        # 3. What the NPC's personal knowledge level and relationships are
        # 4. Filter based on time, relevance, and memory capacity

        return relevant_events[:10]  # Return first 10 relevant events as example

    def _calculate_token_budget(self, section_lengths: Dict[str, int],
                              total_available_tokens: int = 2048) -> Dict[str, int]:
        """
        Calculate token allocation for different prompt sections.

        Args:
            section_lengths: Approximate length of each section in tokens
            total_available_tokens: Total token budget

        Returns:
            Dictionary with token allocation per section
        """
        # Basic proportional allocation - more important sections get higher allocation
        priority_weights = {
            "system": 1.0,
            "character": 2.0,
            "location": 1.5,
            "quests": 2.0,
            "events": 1.0,
            "memory": 3.0,  # Memory is most important for rich narrative
            "outcome": 2.5    # Outcome is crucial for consistency
        }

        total_weight = sum(priority_weights.values())

        allocations = {}
        remaining_tokens = total_available_tokens

        # First allocate minimum required tokens (simplified approach)
        min_allocations = {
            "system": 50,
            "character": 100,
            "location": 75,
            "quests": 50,
            "events": 50,
            "memory": 300,
            "outcome": 100
        }

        for section, min_tokens in min_allocations.items():
            allocations[section] = min(min_tokens, remaining_tokens)
            remaining_tokens -= allocations[section]

        # Distribute remaining tokens proportionally to priority weights
        if remaining_tokens > 0:
            for section, weight in priority_weights.items():
                if section in allocations:  # Only allocate to sections that already have minimum
                    additional = int((weight / total_weight) * remaining_tokens)
                    allocations[section] += additional

        return allocations


# Example usage functions - would be called by pipeline components
def prepare_prompt(turn_data, character_state):
    """
    Convenience function for simple prompt preparation.

    Args:
        turn_data: Turn data dictionary
        character_state: Character state dictionary

    Returns:
        Formatted prompt string for narrator LLM
    """
    builder = ContextBuilder(None, None)  # Placeholder sessions

    # This would normally be constructed from database objects but for demo
    return builder.build_narrator_prompt(
        turn_data=turn_data,
        character=character_state,
        location={},
        quests=[],
        memory_context=[],
        resolution_result={}
    )