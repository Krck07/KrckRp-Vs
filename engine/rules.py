"""
Rules module - Evaluates actions, calculates capability vs. difficulty,
applies modifiers, and outputs deterministic "outcome tiers"
"""

import json
import os
from enum import Enum
from typing import Dict, List, Tuple, Any


class OutcomeTier(Enum):
    """Enumeration of possible outcome tiers"""
    FAILURE = "failure"
    PARTIAL_SUCCESS = "partial_success" 
    SUCCESS = "success"
    STRONG_SUCCESS = "strong_success"


class RulesEngine:
    """Main rules engine for action resolution and outcome calculation"""
    
    def __init__(self, world_config_path: str = None):
        """
        Initialize the rules engine with optional world-specific configuration.
        
        Args:
            world_config_path: Path to JSON file containing world rules
        """
        self.world_rules = self._load_world_configuration(world_config_path)
        self.outcome_thresholds = {
            OutcomeTier.FAILURE: 0.0,
            OutcomeTier.PARTIAL_SUCCESS: 0.25,
            OutcomeTier.SUCCESS: 0.75, 
            OutcomeTier.STRONG_SUCCESS: 1.0
        }
    
    def _load_world_configuration(self, config_path: str = None) -> Dict[str, Any]:
        """
        Load world configuration from JSON file or use defaults.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Dictionary with world rules
        """
        # Default configuration that will be overridden by actual world configs
        default_config = {
            "stat_names": ["strength", "dexterity", "constitution", "intelligence"],
            "ability_groups": [
                "offense",
                "defense", 
                "restoration",
                "mobility",
                "perception",
                "influence",
                "manipulation",
                "utility"
            ],
            "difficulty_scaling": 1.0,
            "modifier_ranges": {"positive": 2, "negative": -2},
            "default_difficulties": {
                "move": 1.0,
                "attack": 2.0, 
                "defend": 1.5,
                "persuade": 2.5,
                "stealth": 3.0,
                "heal": 2.0,
                "craft": 2.0
            },
            "terrain_modifiers": {
                "difficult": -1.0,
                "rough": -0.5,
                "flat": 0.0,
                "smooth": 0.5
            },
            "equipment_modifiers": {
                "weapon": 1.0,
                "shield": 1.0,
                "both": 2.0
            }
        }
        
        # If a config path is provided, load it and merge with defaults
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                
                # Merge configurations - user config overrides defaults
                merged_config = default_config.copy()
                merged_config.update(user_config)
                return merged_config
                
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load world configuration from {config_path}: {e}")
                print("Using default rules instead.")
                return default_config
        else:
            # Return default config if no file specified or file doesn't exist
            return default_config
    
    def evaluate_action(self, 
                       action_intent: str, 
                       actor_stats: Dict[str, int], 
                       context_modifiers: Dict) -> Tuple[OutcomeTier, List[str]]:
        """
        Main method to calculate outcome tier for an attempted action.
        
        Args:
            action_intent: The type of action being attempted
            actor_stats: Current character stats and abilities  
            context_modifiers: Environmental, relationship, time modifiers
            
        Returns:
            (outcome_tier, consequences) - Outcome with explanation text
        """
        # Step 1: Determine base difficulty 
        base_difficulty = self._calculate_base_difficulty(action_intent)
        
        # Step 2: Calculate actor's capability  
        capability = self._calculate_capability(action_intent, actor_stats)
        
        # Step 3: Apply context modifiers
        modified_difficulty = self._apply_context_modifiers(base_difficulty, 
                                                           context_modifiers)
        
        # Step 4: Calculate probability of success (0.0 to 1.0)
        success_probability = self._calculate_success_chance(capability, 
                                                            modified_difficulty)
        
        # Step 5: Determine outcome tier
        outcome_tier = self._determine_outcome_tier(success_probability)
        
        # Step 6: Generate consequences based on outcome
        consequences = self._generate_consequences(action_intent, 
                                                   outcome_tier, 
                                                   context_modifiers)
        
        return (outcome_tier, consequences)
    
    def _calculate_base_difficulty(self, action_intent: str) -> float:
        """
        Calculate base difficulty of an action from configuration.
        
        Args:
            action_intent: Type of action
            
        Returns:
            Difficulty score (higher = harder)
        """
        default_difficulties = self.world_rules.get("default_difficulties", {})
        return default_difficulties.get(action_intent.lower(), 2.0)
    
    def _calculate_capability(self, action_intent: str, actor_stats: Dict) -> float:
        """
        Calculate actor's capability to perform the action.
        
        Args:
            action_intent: Type of action  
            actor_stats: Character's stats
            
        Returns:
            Capability score (higher = more capable)
        """
        # Check if there are ability-specific stat mappings
        stat_mappings = self.world_rules.get("stat_mappings", {})
        required_stats = stat_mappings.get(action_intent.lower(), 
                                          self.world_rules.get("stat_names", []))
        
        # Sum up relevant stats for this action
        capability = 0.0
        for stat in required_stats:
            if stat in actor_stats:
                capability += actor_stats[stat]
                
        return capability
    
    def _apply_context_modifiers(self, base_difficulty: float, 
                                modifiers: Dict) -> float:
        """
        Apply environmental and narrative modifiers to difficulty.
        
        Args:
            base_difficulty: Original difficulty calculation  
            modifiers: Contextual modifiers from environment/relationships
            
        Returns:
            Modified difficulty score
        """
        total_modifier = 0
        
        # Apply different types of modifiers
        if "terrain" in modifiers:
            terrain_mod = self._get_terrain_modifier(modifiers["terrain"])
            total_modifier += terrain_mod
            
        if "equipment" in modifiers:
            equipment_mod = self._get_equipment_modifier(modifiers["equipment"])
            total_modifier += equipment_mod
            
        if "relationship" in modifiers:
            relationship_mod = self._get_relationship_modifier(modifiers["relationship"])
            total_modifier += relationship_mod
            
        # Apply modifier range limits
        max_positive_mod = self.world_rules.get("modifier_ranges", {}).get("positive", 2)
        max_negative_mod = self.world_rules.get("modifier_ranges", {}).get("negative", -2)
        
        bounded_modifier = min(max(total_modifier, max_negative_mod), max_positive_mod)
        modified_difficulty = base_difficulty * (1 + bounded_modifier/10)  # Scale by 10
        
        return modified_difficulty
    
    def _get_terrain_modifier(self, terrain_type: str) -> float:
        """Get modifier for specific terrain."""
        modifiers = self.world_rules.get("terrain_modifiers", {})
        return modifiers.get(terrain_type.lower(), 0.0)
    
    def _get_equipment_modifier(self, equipment: List[str]) -> float:
        """Get modifier based on equipment."""
        # Check if it's a list of items or single item
        if isinstance(equipment, str):
            equipment = [equipment]
            
        modifiers = self.world_rules.get("equipment_modifiers", {})
        
        # Simple approach: check for exact matches
        total_modifier = 0.0
        
        # Special case for "both" (weapon + shield)
        if len(equipment) >= 2:
            has_weapon = any(item in equipment or item in ["sword", "blade"] for item in equipment)
            has_shield = any(item in equipment or item in ["shield"] for item in equipment)
            
            if has_weapon and has_shield:
                return modifiers.get("both", 2.0)
        
        # Sum individual modifiers
        for item in equipment:
            item_mod = modifiers.get(item.lower(), 0.0) 
            total_modifier += item_mod
            
        return total_modifier
    
    def _get_relationship_modifier(self, relationship: str) -> float:
        """Get modifier based on character relationships."""
        modifiers = self.world_rules.get("relationship_modifiers", {})
        return modifiers.get(relationship.lower(), 0.0)
    
    def _calculate_success_chance(self, capability: float, difficulty: float) -> float:
        """
        Calculate probability of success (0.0 to 1.0).
        
        Args:
            capability: Actor's capability score  
            difficulty: Modified difficulty
            
        Returns:
            Success probability
        """
        # Simple formula: chance = capability / difficulty 
        if difficulty <= 0:
            return 1.0 if capability > 0 else 0.0
            
        ratio = capability / difficulty
        success_chance = max(0.0, min(ratio, 1.0))  # Clamp between 0 and 1
        
        return success_chance
    
    def _determine_outcome_tier(self, success_probability: float) -> OutcomeTier:
        """
        Determine outcome tier based on success probability.
        
        Args:
            success_probability: Probability of success (0.0 to 1.0)
            
        Returns:
            Outcome tier classification
        """
        # Use thresholds from world rules if available
        threshold_config = self.world_rules.get("outcome_thresholds", self.outcome_thresholds)
        
        if success_probability >= threshold_config[OutcomeTier.STRONG_SUCCESS]:
            return OutcomeTier.STRONG_SUCCESS
        elif success_probability >= threshold_config[OutcomeTier.SUCCESS]:
            return OutcomeTier.SUCCESS
        elif success_probability >= threshold_config[OutcomeTier.PARTIAL_SUCCESS]:
            return OutcomeTier.PARTIAL_SUCCESS
        else:
            return OutcomeTier.FAILURE
    
    def _generate_consequences(self, action_intent: str, 
                              outcome_tier: OutcomeTier,
                              context_modifiers: Dict) -> List[str]:
        """
        Generate specific consequences based on the outcome.
        
        Args:
            action_intent: Type of action
            outcome_tier: Result tier  
            context_modifiers: Context information
            
        Returns:
            List of consequence descriptions
        """
        # Default consequences - could be made configurable too
        default_consequences = {
            OutcomeTier.FAILURE: ["The attempt failed completely."],
            OutcomeTier.PARTIAL_SUCCESS: ["The action had limited success but fell short of full effectiveness."],
            OutcomeTier.SUCCESS: ["The action succeeded as expected."],
            OutcomeTier.STRONG_SUCCESS: ["The action was exceptionally successful, exceeding expectations."]
        }
        
        consequences = default_consequences.get(outcome_tier, [])
        
        # Add context-specific consequences
        if "terrain" in context_modifiers:
            terrain_desc = context_modifiers["terrain"]
            consequences.append(f"The {terrain_desc} terrain made the task more challenging.")
            
        return consequences


# Convenience function for easy usage
def calculate_outcome(action_intent: str, 
                     actor_stats: Dict[str, int], 
                     context_modifiers: Dict,
                     world_config_path: str = None) -> Tuple[OutcomeTier, List[str]]:
    """
    Simple interface to evaluate an action outcome.
    
    Args:
        action_intent: The type of action being attempted
        actor_stats: Character's stats  
        context_modifiers: Contextual modifiers
        world_config_path: Path to configuration file for this world
        
    Returns:
        (outcome_tier, consequences)
    """
    engine = RulesEngine(world_config_path)
    return engine.evaluate_action(action_intent, actor_stats, context_modifiers)


# Example usage and test cases
if __name__ == "__main__":
    # Test with default rules
    stats_1 = {"strength": 8, "dexterity": 6}
    modifiers_1 = {"terrain": "flat", "equipment": ["weapon"]}
    
    tier, conseq = calculate_outcome("attack", stats_1, modifiers_1)
    print(f"Action: Attack, Outcome: {tier.value}, Consequences: {conseq}")
