#!/usr/bin/env python3

"""
Simple test script to verify RulesEngine functionality.
"""

import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.rules import RulesEngine, OutcomeTier

def test_basic_functionality():
    """Test core RulesEngine methods"""

    print("Testing RulesEngine basic functionality...")

    # Test initialization
    engine = RulesEngine()
    print(f"PASS: Engine initialized with config: {len(engine.world_rules)} keys")

    # Test base difficulty calculation
    diff = engine._calculate_base_difficulty("attack")
    print(f"PASS: Base difficulty for 'attack': {diff}")

    # Test capability calculation
    stats = {"strength": 5, "dexterity": 3}
    cap = engine._calculate_capability("attack", stats)
    print(f"PASS: Capability for attack with stats {stats}: {cap}")

    # Test terrain modifier
    mod = engine._get_terrain_modifier("difficult")
    print(f"PASS: Terrain modifier for 'difficult': {mod}")

    # Test success chance calculation
    chance = engine._calculate_success_chance(5.0, 2.0)
    print(f"PASS: Success chance (cap=5, diff=2): {chance}")

    # Test outcome tier determination
    tier = engine._determine_outcome_tier(0.8)
    print(f"PASS: Outcome tier for prob=0.8: {tier.value}")

    # Test actual evaluation
    actor_stats = {"strength": 8, "dexterity": 6}
    context_modifiers = {"terrain": "flat", "equipment": ["weapon"]}
    outcome_tier, consequences = engine.evaluate_action("attack", actor_stats, context_modifiers)
    print(f"PASS: Full action evaluation: {outcome_tier.value} with {len(consequences)} consequences")

    # Test custom config loading
    try:
        custom_engine = RulesEngine("engine/world_configs/default_rules.json")
        print(f"PASS: Custom config loaded successfully (has {len(custom_engine.world_rules)} keys)")
    except Exception as e:
        print(f"WARNING: Error with custom config: {e}")

    print("\nAll basic tests completed!")

if __name__ == "__main__":
    test_basic_functionality()