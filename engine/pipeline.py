"""
Pipeline module - Orchestrates the 8-step turn loop:
1. Receive -> Interpret -> Resolve -> Context -> Narrate -> Extract -> Validate/Commit -> Update UI
"""

from typing import Dict, Any, Optional, List
import json

# Import required engine components
from engine.rules import RulesEngine, OutcomeTier
from engine.quests import QuestEngine
from database.models import Turn, Character, Location, Quest, Event
from llm.client import LLMClient


class Pipeline:
    def __init__(self, db_session, vector_store):
        """
        Initialize the pipeline with required components.

        Args:
            db_session: Database session for persistence operations
            vector_store: Vector store for memory retrieval
        """
        self.db_session = db_session
        self.vector_store = vector_store
        self.rules_engine = RulesEngine()
        self.quest_engine = QuestEngine()
        # LLM client will be initialized with appropriate endpoints
        self.llm_client = None

    def run_turn(self, player_input: str, campaign_id: int, session_id: int) -> Dict[str, Any]:
        """
        Execute one complete turn of the game loop through 8 steps:
        1. Receive input - Store player action
        2. Interpret intent - Parse action type and target
        3. Resolve mechanics - Calculate outcome using rules engine
        4. Assemble context - Build narrator prompt with all relevant info
        5. Narrate response - Generate narrative text via LLM
        6. Extract state changes - Identify proposed changes from narration
        7. Validate/Commit changes - Check against rules and commit valid events
        8. Update UI - Prepare data for frontend refresh

        Args:
            player_input: Raw text input from the player
            campaign_id: ID of current campaign
            session_id: ID of current session

        Returns:
            Dictionary with results from all steps
        """

        # Step 1: Receive input - Store player turn in database
        turn = self._store_player_turn(player_input, campaign_id, session_id)

        try:
            # Step 2: Interpret intent using LLM or rule-based system
            intent_data = self._interpret_intent(player_input)

            # Step 3: Resolve mechanics with RulesEngine for outcome calculation
            resolution_result = self._resolve_mechanics(intent_data, turn.character_id)

            # Step 4: Assemble context for narrator prompt
            context_prompt = self._assemble_narrator_context(turn, intent_data, resolution_result)

            # Step 5: Generate narration using LLM with assembled context
            narration_response = self._generate_narration(context_prompt)

            # Step 6: Extract state changes from response using extractor LLM
            extraction_result = self._extract_changes(narration_response.get("text", ""), player_input)

            # Step 7: Validate and commit extracted changes to database
            event_log = self._validate_and_commit(extraction_result, turn.id, resolution_result)

            # Step 8: Prepare UI update data for frontend refresh
            ui_state = self._prepare_ui_update(turn.character_id, campaign_id)

        except Exception as e:
            # Handle errors gracefully and log them
            print(f"Error in pipeline execution: {e}")
            raise

        return {
            "turn": turn,
            "narration": narration_response.get("text", ""),
            "events": event_log,
            "ui_state": ui_state,
            "resolution_result": resolution_result
        }

    def _store_player_turn(self, player_input: str, campaign_id: int, session_id: int) -> Turn:
        """
        Store the player's turn input in database.

        Args:
            player_input: Raw text from player
            campaign_id: Current campaign ID
            session_id: Current session ID

        Returns:
            The created Turn object
        """
        # Create a new Turn instance with provided details
        turn = Turn(
            player_input=player_input,
            campaign_id=campaign_id,
            session_id=session_id
        )

        # Add to database and commit
        self.db_session.add(turn)
        self.db_session.commit()
        self.db_session.refresh(turn)  # Get the ID that was assigned

        return turn

    def _interpret_intent(self, player_input: str) -> Dict[str, Any]:
        """
        Parse player input to determine intent (action type and target).

        Args:
            player_input: Raw text from player

        Returns:
            Dictionary with parsed intent information
        """
        # For now this is a placeholder - in the full implementation,
        # This would use an LLM or rule-based approach to classify actions

        # In a real implementation, we'd call the extractor LLM or
        # use NLP rules to determine action type and target
        #
        # The current simple keyword matching serves as a minimal placeholder

        # Basic example of parsing (this could be enhanced)
        action_intent = "generic_action"  # Default action type
        target_entity = None  # What the player is targeting

        # Simple keyword matching for demonstration - real implementation
        # would use LLM or more sophisticated NLP
        if "attack" in player_input.lower():
            action_intent = "attack"
        elif "move" in player_input.lower() or "go" in player_input.lower():
            action_intent = "move"
        elif "use" in player_input.lower():
            action_intent = "use_item"
        elif "talk" in player_input.lower() or "speak" in player_input.lower():
            action_intent = "talk"

        # For now return placeholder data structure
        return {
            "action": action_intent,
            "target": target_entity,
            "raw_input": player_input,
            "confidence": 0.5  # Placeholder confidence score
        }

    def _resolve_mechanics(self, intent_data: Dict[str, Any], character_id: int) -> Dict[str, Any]:
        """
        Calculate mechanical outcome using RulesEngine.

        Args:
            intent_data: Intent information from step 2
            character_id: ID of character performing action

        Returns:
            Dictionary with resolution results
        """
        # Get current character state to use in rules calculation
        character = self.db_session.query(Character).filter_by(id=character_id).first()

        if not character:
            raise ValueError(f"Character with id {character_id} not found")

        # Convert character stats for rules engine
        actor_stats = character.stats or {}

        # Get context modifiers from game state (simplified implementation)
        context_modifiers = {
            "terrain": "flat",  # Placeholder - would use actual location data
            "equipment": [],    # Would come from inventory
            "relationship": None,  # Would be determined by targets
        }

        # Use rules engine to calculate outcome
        try:
            tier, consequences = self.rules_engine.evaluate_action(
                action_intent=intent_data["action"],
                actor_stats=actor_stats,
                context_modifiers=context_modifiers
            )

            return {
                "outcome_tier": tier.value,
                "consequences": consequences,
                "success_probability": 0.5  # Would be calculated by rules engine
            }
        except Exception as e:
            print(f"Error in mechanical resolution: {e}")
            # Return default values on error
            return {
                "outcome_tier": OutcomeTier.FAILURE.value,
                "consequences": ["The action failed due to an internal error."],
                "success_probability": 0.0
            }

    def _assemble_narrator_context(self, turn: Turn, intent_data: Dict[str, Any],
                                 resolution_result: Dict[str, Any]) -> str:
        """
        Build complete context prompt for the narrator LLM.

        Args:
            turn: Current turn object
            intent_data: Intent information
            resolution_result: Mechanical outcome from rules engine

        Returns:
            Formatted string prompt for narrator LLM
        """
        # This would use ContextBuilder to create a proper prompt structure

        # Get character info (simplified)
        character = self.db_session.query(Character).filter_by(id=turn.character_id).first()
        location = self.db_session.query(Location).filter_by(id=character.location_id).first()

        # Get active quests
        quests = self.quest_engine.get_active_quests()

        # Build basic context structure (would be more detailed in full implementation)
        context_data = {
            "player_action": intent_data["raw_input"],
            "character_name": character.name if character else "Unknown",
            "location_name": location.name if location else "Unknown",
            "outcome_tier": resolution_result["outcome_tier"],
            "consequences": resolution_result["consequences"]
        }

        # For now, return a simple formatted string - in real implementation this
        # would call context_builder.build_narrator_prompt()
        prompt = f"""
[PLAYER ACTION]
{context_data['player_action']}

[CHARACTER STATE]
Name: {context_data['character_name']}
Stats: {character.stats if character else 'N/A'}

[LOCATION INFO]
Location: {context_data['location_name']}

[MECHANICAL OUTCOME]
Result: {context_data['outcome_tier']}
Consequences: {' '.join(context_data['consequences'])}
"""

        return prompt

    def _generate_narration(self, context_prompt: str) -> Dict[str, Any]:
        """
        Generate narrative response using narrator LLM.

        Args:
            context_prompt: Formatted prompt for narrator

        Returns:
            Dictionary with narration result
        """
        # In a real implementation this would call the actual LLM client
        # For now return placeholder

        if not self.llm_client:
            # Initialize with default narrator endpoint if not already set
            try:
                from llm.client import LLMClient
                self.llm_client = LLMClient(narrator_endpoint="http://localhost:5001")
            except Exception as e:
                print(f"Could not initialize LLM client: {e}")

        # Placeholder result for demonstration purposes
        return {
            "text": f"The narrator would generate a response here based on '{context_prompt[:50]}...'",
            "tokens_used": 200,
            "model_used": "narrator"
        }

    def _extract_changes(self, narration_text: str, player_input: str) -> Dict[str, Any]:
        """
        Extract state changes from narrative text using extractor LLM.

        Args:
            narration_text: Text generated by narrator LLM
            player_input: Original player input

        Returns:
            Dictionary with extracted change proposals
        """
        # In a real implementation this would use an extractor LLM to parse the narrative

        if not self.llm_client:
            try:
                from llm.client import LLMClient
                self.llm_client = LLMClient(extractor_endpoint="http://localhost:5002")
            except Exception as e:
                print(f"Could not initialize extractor client: {e}")

        # Placeholder result for demonstration purposes
        return {
            "proposed_changes": [],
            "validation_status": "pending"
        }

    def _validate_and_commit(self, extraction_result: Dict[str, Any], turn_id: int,
                           resolution_result: Dict[str, Any]) -> List[Event]:
        """
        Validate proposed changes and commit valid ones to database.

        Args:
            extraction_result: Results from change extraction
            turn_id: ID of the current turn
            resolution_result: Mechanical outcome

        Returns:
            List of committed events
        """
        # In a full implementation, this would validate each proposed change
        # against game rules and state, then create event log entries

        # Placeholder that creates a basic event for demonstration
        events = []

        try:
            if extraction_result["proposed_changes"]:
                # Create an event for the turn with resolution info
                event = Event(
                    turn_id=turn_id,
                    source="engine",
                    before_values=json.dumps({}),
                    after_values=json.dumps({
                        "outcome": resolution_result.get("outcome_tier", "unknown"),
                        "consequences": resolution_result.get("consequences", [])
                    })
                )

                self.db_session.add(event)
                self.db_session.commit()
                events.append(event)
        except Exception as e:
            print(f"Error in validation/commit: {e}")

        return events

    def _prepare_ui_update(self, character_id: int, campaign_id: int) -> Dict[str, Any]:
        """
        Prepare data needed for UI refresh.

        Args:
            character_id: ID of player character
            campaign_id: Current campaign ID

        Returns:
            Dictionary with UI state data
        """
        # Gather necessary information to update frontend
        try:
            character = self.db_session.query(Character).filter_by(id=character_id).first()
            location = self.db_session.query(Location).filter_by(id=character.location_id).first() if character else None

            return {
                "character": {
                    "name": character.name if character else "Unknown",
                    "stats": character.stats if character else {},
                    "location": location.name if location else "Unknown"
                } if character else {},
                "campaign_id": campaign_id
            }
        except Exception as e:
            print(f"Error preparing UI update: {e}")
            return {}

# Example usage function - would be called by FastAPI endpoints
def process_turn(player_action, campaign_id, session_id):
    """
    Process a single turn of gameplay.

    This is an example of how the pipeline might be invoked from
    FastAPI endpoint handlers or other external systems.

    Args:
        player_action: Text input from player
        campaign_id: ID of current campaign
        session_id: Current session ID

    Returns:
        Dictionary with turn results (would contain turn data, narration,
        events, and UI state)
    """
    # This would be called by the FastAPI endpoint handlers
    # Implementation is handled through Pipeline.run_turn()
    pass