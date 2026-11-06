"""Automated tests for Mystery Island game logic."""
import unittest

from game import (
    new_game,
    apply_action,
    available_actions,
    can_cross_bridge,
    can_light_beacon,
    LOCATIONS,
    STARTING_ENERGY,
)


class TestNewGame(unittest.TestCase):
    def test_t1_new_game_defaults(self):
        p = new_game("Ada")
        self.assertEqual(p["location"], "Beach")
        self.assertEqual(p["energy"], STARTING_ENERGY)
        self.assertEqual(p["inventory"], [])
        self.assertFalse(p["game_over"])
        self.assertFalse(p["won"])


class TestInvalidInput(unittest.TestCase):
    def test_t2_invalid_command_does_not_mutate(self):
        p = new_game("Ada")
        before = dict(p)
        before["inventory"] = list(p["inventory"])
        apply_action(p, "banana")
        self.assertEqual(p["location"], before["location"])
        self.assertEqual(p["energy"], before["energy"])
        self.assertEqual(p["inventory"], before["inventory"])
        self.assertFalse(p["game_over"])

    def test_wrong_direction_rejected_without_cost(self):
        p = new_game("Ada")
        r = apply_action(p, "go south")
        self.assertFalse(r["ok"])
        self.assertEqual(p["location"], "Beach")
        self.assertEqual(p["energy"], STARTING_ENERGY)

    def test_whitespace_and_case_insensitive(self):
        p = new_game("Ada")
        r = apply_action(p, "  NORTH  ")
        self.assertTrue(r["ok"])
        self.assertEqual(p["location"], "Jungle")


class TestMovement(unittest.TestCase):
    def test_t3_legal_move_changes_location_and_energy_once(self):
        p = new_game("Ada")
        r = apply_action(p, "go north")
        self.assertTrue(r["ok"])
        self.assertEqual(p["location"], "Jungle")
        self.assertEqual(p["energy"], STARTING_ENERGY - 1)
        self.assertTrue(r["energy_used"])


class TestInventory(unittest.TestCase):
    def test_t5_rope_collected_once(self):
        p = new_game("Ada")
        apply_action(p, "go north")
        r1 = apply_action(p, "take rope")
        self.assertTrue(r1["ok"])
        self.assertIn("rope", p["inventory"])
        r2 = apply_action(p, "take rope")
        self.assertFalse(r2["ok"])
        self.assertEqual(p["inventory"].count("rope"), 1)


class TestPuzzles(unittest.TestCase):
    def test_t6_bridge_blocked_without_rope(self):
        p = new_game("Ada")
        apply_action(p, "go north")
        apply_action(p, "go east")
        apply_action(p, "go north")
        self.assertEqual(p["location"], "Old Bridge")
        self.assertFalse(can_cross_bridge(p))
        r = apply_action(p, "cross bridge")
        self.assertFalse(r["ok"])
        self.assertEqual(p["location"], "Old Bridge")

    def test_t6b_old_bridge_has_no_direct_north_route(self):
        p = new_game("Ada")
        p["location"] = "Old Bridge"
        r = apply_action(p, "go north")
        self.assertFalse(r["ok"])
        self.assertEqual(p["location"], "Old Bridge")
        self.assertEqual(p["energy"], STARTING_ENERGY)

    def test_t7_beacon_blocked_without_lantern(self):
        p = new_game("Ada")
        p["location"] = "Lighthouse"
        p["inventory"] = ["rope"]
        self.assertFalse(can_light_beacon(p))
        r = apply_action(p, "light beacon")
        self.assertFalse(r["ok"])
        self.assertFalse(p["won"])

    def test_t8_win_with_correct_items(self):
        p = new_game("Ada")
        apply_action(p, "go north")
        apply_action(p, "take rope")
        apply_action(p, "go east")
        apply_action(p, "take lantern")
        apply_action(p, "go north")
        apply_action(p, "cross bridge")
        r = apply_action(p, "light beacon")
        self.assertTrue(r["ok"])
        self.assertTrue(p["won"])
        self.assertTrue(p["game_over"])
        self.assertGreaterEqual(p["energy"], 0)


class TestEnergy(unittest.TestCase):
    def test_t9_energy_exhaustion_causes_loss(self):
        p = new_game("Ada")
        p["energy"] = 1
        apply_action(p, "go north")
        self.assertEqual(p["energy"], 0)
        self.assertTrue(p["game_over"])
        self.assertFalse(p["won"])

    def test_cannot_move_after_game_over(self):
        p = new_game("Ada")
        p["game_over"] = True
        before = p["location"]
        apply_action(p, "go north")
        self.assertEqual(p["location"], before)


class TestReplay(unittest.TestCase):
    def test_t10_replay_resets_state(self):
        old = new_game("Ada")
        old["inventory"].append("rope")
        old["location"] = "Lighthouse"
        old["energy"] = 1
        old["game_over"] = True

        fresh = new_game("Ada")
        self.assertEqual(fresh["location"], "Beach")
        self.assertEqual(fresh["energy"], STARTING_ENERGY)
        self.assertEqual(fresh["inventory"], [])
        self.assertFalse(fresh["game_over"])
        self.assertFalse(fresh["won"])


class TestMapIntegrity(unittest.TestCase):
    def test_all_destinations_exist(self):
        for src, moves in LOCATIONS.items():
            for direction, dest in moves.items():
                self.assertIn(dest, LOCATIONS,
                              f"{src} -> {direction} points to missing {dest}")

    def test_five_locations_present(self):
        for name in ("Beach", "Jungle", "Cave", "Old Bridge", "Lighthouse"):
            self.assertIn(name, LOCATIONS)


if __name__ == "__main__":
    unittest.main()