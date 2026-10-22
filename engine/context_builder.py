"""
Context Builder module - Assembles the strict prompt for the Narrator LLM.
Handles token budgets, rolling summaries, and NPC knowledge filtering.
"""

class ContextBuilder:
    def __init__(self):
        pass
    
    def build_narrator_prompt(self, turn_data, character, location, quests, memory_context):
        """
        Construct a well-structured prompt for the narrator LLM with proper token management.
        
        Args:
            turn_data: Current player action and previous turns
            character: Player's current state  
            location: Current location details
            quests: Active quest information
            memory_context: Retrieved memories from vector store
            
        Returns:
            Formatted prompt string for the narrator LLM
        """
        # Build context with token budgeting
        
        return "Prompt would be constructed here"
    
    def filter_npc_knowledge(self, npc, relevant_events):
        """
        Filter memories based on what NPC could realistically know.
        
        Args:
            npc: The NPC whose knowledge we're filtering  
            relevant_events: Events that might be remembered
            
        Returns:
            Filtered list of memories the NPC would actually recall
        """
        # Implementation for NPC knowledge filtering
        
        return []

# Example usage
def prepare_prompt(turn_data, character_state):
    builder = ContextBuilder()
    return builder.build_narrator_prompt(turn_data, character_state, None, None, None)