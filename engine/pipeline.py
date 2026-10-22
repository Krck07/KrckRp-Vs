"""
Pipeline module - Orchestrates the 8-step turn loop:
1. Receive -> Interpret -> Resolve -> Context -> Narrate -> Extract -> Validate/Commit -> Update UI
"""

class Pipeline:
    def __init__(self):
        pass
    
    def run_turn(self, player_input):
        """
        Execute one complete turn of the game loop.
        This method coordinates all steps in the pipeline.
        """
        # Step 1: Receive input
        # Step 2: Interpret intent  
        # Step 3: Resolve mechanics
        # Step 4: Assemble context for narrator
        # Step 5: Narrate response
        # Step 6: Extract state changes
        # Step 7: Validate and commit changes
        # Step 8: Update UI
        
        pass

# Example of a turn execution flow
def process_turn(player_action):
    pipeline = Pipeline()
    return pipeline.run_turn(player_action)