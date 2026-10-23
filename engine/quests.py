"""
Quests module - Emergent quest logic, evaluating state changes
to trigger quest creation or objective updates.
"""

from enum import Enum
from typing import Dict, List, Any, Optional
import json


class QuestStatus(Enum):
    """Enumeration of possible quest states"""
    PROPOSED = "proposed"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"
    EXPIRED = "expired"


class Objective:
    """Represents a single objective within a quest"""

    def __init__(self, description: str):
        self.description = description
        self.status = QuestStatus.PROPOSED  # PENDING or COMPLETE

    def complete(self):
        """Mark this objective as completed"""
        self.status = QuestStatus.COMPLETED

    def to_dict(self) -> Dict[str, Any]:
        """Convert objective to dictionary for serialization"""
        return {
            "description": self.description,
            "status": self.status.value
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Objective':
        """Create objective from dictionary"""
        obj = cls(data["description"])
        status_value = data.get("status", "proposed")
        try:
            # Validate that the status value is a valid enum member
            obj.status = QuestStatus(status_value)
        except ValueError:
            # If invalid, default to PROPOSED state for safety
            obj.status = QuestStatus.PROPOSED
        return obj


class Quest:
    """Represents a single quest in the game"""

    def __init__(self, title: str, summary: str, giver: str, objectives: List[Objective] = None):
        self.title = title
        self.summary = summary
        self.giver = giver  # Character who gave the quest
        self.objectives = objectives or []
        self.state = QuestStatus.PROPOSED
        self.locations = []  # Locations relevant to this quest
        self.hooks = []  # Consequences/hooks when quest completes/fails
        self.origin_turn = None  # Turn number where quest was created

    def add_objective(self, description: str):
        """Add a new objective to the quest"""
        obj = Objective(description)
        self.objectives.append(obj)

    def complete_objective(self, index: int):
        """Complete an objective by index"""
        # Handle negative indices properly (Python-style)
        if index < 0:
            index = len(self.objectives) + index
        if not 0 <= index < len(self.objectives):
            raise IndexError(f"Objective index {index} out of range for quest with {len(self.objectives)} objectives")
        self.objectives[index].complete()

    def all_objectives_complete(self) -> bool:
        """Check if all objectives are completed"""
        return all(obj.status == QuestStatus.COMPLETED for obj in self.objectives)

    def activate(self):
        """Activate the quest"""
        self.state = QuestStatus.ACTIVE

    def complete(self):
        """Complete the quest"""
        self.state = QuestStatus.COMPLETED

    def fail(self):
        """Fail the quest"""
        self.state = QuestStatus.FAILED

    def abandon(self):
        """Abandon the quest"""
        self.state = QuestStatus.ABANDONED

    def expire(self):
        """Expire the quest"""
        self.state = QuestStatus.EXPIRED

    def to_dict(self) -> Dict[str, Any]:
        """Convert quest to dictionary for serialization"""
        return {
            "title": self.title,
            "summary": self.summary,
            "giver": self.giver,
            "objectives": [obj.to_dict() for obj in self.objectives],
            "state": self.state.value,
            "locations": self.locations,
            "hooks": self.hooks,
            "origin_turn": self.origin_turn
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Quest':
        """Create quest from dictionary"""
        # Convert objectives back to Objective instances
        objectives = [Objective.from_dict(obj_data) for obj_data in data.get("objectives", [])]

        quest = cls(
            title=data["title"],
            summary=data["summary"],
            giver=data["giver"],
            objectives=objectives
        )

        # Set other properties with validation
        state_value = data.get("state", "proposed")
        try:
            # Validate that the status value is a valid enum member
            quest.state = QuestStatus(state_value)
        except ValueError:
            # If invalid, default to PROPOSED state for safety
            quest.state = QuestStatus.PROPOSED

        quest.locations = data.get("locations", [])
        quest.hooks = data.get("hooks", [])
        quest.origin_turn = data.get("origin_turn")

        return quest


class QuestEngine:
    """Main quest engine for emergent quest creation and management"""

    def __init__(self):
        """Initialize the quest engine"""
        self.active_quests: List[Quest] = []

    def generate_quest(self, npc_goal: str, player_actions: List[str], world_rules: Dict, giver: str = "NPC") -> Optional[Quest]:
        """
        Create new quests based on NPC goals and player behavior.

        Args:
            npc_goal: The goal that triggered quest generation
            player_actions: Recent actions that might trigger quests
            world_rules: Rules for how quests work in this world
            giver: Character who gave the quest (defaults to "NPC")

        Returns:
            New Quest object or None if no quest generated
        """
        # Check for empty NPC goals to prevent errors
        if not npc_goal or not isinstance(npc_goal, str):
            return None

        # Create a simple quest based on the NPC's goal with proper title handling
        title = f"Quest: {npc_goal[:50]}..."  # Truncate long titles properly
        summary = f"Achieve the goal: {npc_goal}"

        # Use provided giver or default to "NPC"
        if not isinstance(giver, str):
            giver = "NPC"

        # Create basic objectives from player actions
        objectives = []
        if player_actions and isinstance(player_actions, list):
            for i, action in enumerate(player_actions[:3]):  # Limit to first 3 actions
                if isinstance(action, str):  # Ensure it's a valid string
                    objectives.append(Objective(f"Action {i+1}: {action}"))
                else:
                    # Skip invalid non-string items gracefully
                    continue

        quest = Quest(title, summary, giver, objectives)
        return quest

    def update_quests(self, event_log: List[Dict]) -> List[Quest]:
        """
        Update active quests based on new events.

        Args:
            event_log: Recent changes to game state

        Returns:
            List of updated quest statuses
        """
        # More efficient implementation that only processes quests that need updates
        if not self.active_quests:
            return []

        # Process the event log to update objectives and check for completed quests
        updated_quests = []

        for quest in self.active_quests:
            # Check if this quest can be updated and needs processing
            if (quest.state == QuestStatus.ACTIVE and
                any(obj.status != QuestStatus.COMPLETED for obj in quest.objectives)):

                # In a real implementation, we would analyze the event_log here to
                # determine which objectives are now complete based on game events.
                # For this basic implementation, we'll just check if all objectives are complete

                # Update based on current state - simplified but more efficient approach
                # Only complete the quest once to prevent redundant state changes
                if quest.all_objectives_complete() and quest.state != QuestStatus.COMPLETED:
                    quest.complete()

            updated_quests.append(quest)

        return updated_quests

    def add_quest(self, quest: Quest):
        """Add a new quest to the active quests list"""
        self.active_quests.append(quest)

    def get_active_quests(self) -> List[Quest]:
        """Get all currently active quests"""
        return [q for q in self.active_quests if q.state == QuestStatus.ACTIVE]

    def get_quest_by_title(self, title: str) -> Optional[Quest]:
        """Find a quest by its title"""
        for quest in self.active_quests:
            if quest.title == title:
                return quest
        return None

# Example usage - corrected function signature to return single Quest not List[Quest]
def process_new_quest(npc_goal: str, player_actions: List[str], giver: str = "NPC") -> Optional[Quest]:
    try:
        engine = QuestEngine()
        return engine.generate_quest(npc_goal, player_actions, {}, giver)
    except Exception:
        # Return None gracefully on any error
        return None


if __name__ == "__main__":
    # Test basic functionality
    print("Testing QuestEngine...")

    # Create a quest manually
    quest = Quest(
        title="Find the Lost Artifact",
        summary="Recover the ancient artifact from the ruins",
        giver="Old Sage"
    )

    # Add objectives
    quest.add_objective("Enter the ruins")
    quest.add_objective("Find the artifact")
    quest.add_objective("Return safely")

    print(f"Quest: {quest.title}")
    print(f"Objectives: {len(quest.objectives)}")

    # Complete first objective
    quest.complete_objective(0)
    print(f"First objective complete: {quest.objectives[0].status.value}")

    # Test error handling for invalid index
    try:
        quest.complete_objective(5)  # This should raise IndexError
    except IndexError as e:
        print(f"Caught expected error: {e}")