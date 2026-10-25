"""
Test file for verifying the quest system fixes.
"""

import sys
import os

# Add the project root to the path so we can import from engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.quests import QuestEngine, Quest, Objective, QuestStatus


def test_objective_status_enum():
    """Test that Objective now uses QuestStatus enum instead of strings"""
    obj = Objective("Test objective")

    # Should be using the enum value, not a string
    assert obj.status == QuestStatus.PROPOSED

    # Complete the objective
    obj.complete()
    assert obj.status == QuestStatus.COMPLETED

    print("[PASS] Objective status enum test passed")


def test_complete_objective_bounds_checking():
    """Test that complete_objective properly handles invalid indices"""
    quest = Quest("Test Quest", "Test summary", "NPC")
    quest.add_objective("Objective 1")
    quest.add_objective("Objective 2")

    # This should work
    quest.complete_objective(0)
    assert quest.objectives[0].status == QuestStatus.COMPLETED

    # This should raise IndexError
    try:
        quest.complete_objective(5)  # Out of bounds
        assert False, "Should have raised IndexError"
    except IndexError:
        print("[PASS] Bounds checking test passed")


def test_quest_update_efficiency():
    """Test that quest update logic is more efficient"""
    engine = QuestEngine()

    # Add a few quests with different states
    quest1 = Quest("Quest 1", "Summary 1", "NPC")
    quest1.add_objective("Objective 1")
    quest1.activate()

    quest2 = Quest("Quest 2", "Summary 2", "NPC")
    quest2.add_objective("Objective 1")
    quest2.complete()  # Already completed

    engine.add_quest(quest1)
    engine.add_quest(quest2)

    # Should handle update without errors
    result = engine.update_quests([])
    assert len(result) == 2

    print("[PASS] Quest update efficiency test passed")


def test_process_new_quest_return_type():
    """Test that process_new_quest returns correct type"""
    from engine.quests import process_new_quest

    quest = process_new_quest("Find the treasure", ["explore", "search"])

    # Should return a Quest object, not a list
    assert isinstance(quest, Quest)

    print("[PASS] Process new quest return type test passed")


def test_empty_npc_goal_handling():
    """Test handling of empty NPC goals"""
    engine = QuestEngine()
    result = engine.generate_quest("", ["action"], {})
    assert result is None

    result = engine.generate_quest(None, ["action"], {})
    assert result is None

    print("[PASS] Empty NPC goal handling test passed")


def test_title_truncation():
    """Test title truncation works properly"""
    long_goal = "This is a very long quest goal that should be truncated appropriately to avoid issues with title length"

    engine = QuestEngine()
    quest = engine.generate_quest(long_goal, [], {})

    # Title should be truncated
    assert len(quest.title) <= 53  # "Quest: " + first 50 chars + "..."
    assert quest.title.endswith("...")

    print("[PASS] Title truncation test passed")


def run_all_tests():
    """Run all tests"""
    try:
        test_objective_status_enum()
        test_complete_objective_bounds_checking()
        test_quest_update_efficiency()
        test_process_new_quest_return_type()
        test_empty_npc_goal_handling()
        test_title_truncation()

        print("\n🎉 All tests passed! The fixes are working correctly.")
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    run_all_tests()