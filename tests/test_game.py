"""Automated tests for Mystery Island game logic."""
import unittest
from copy import deepcopy

from game import (
    new_game,
    apply_action,
    available_actions,
    can_cross_bridge,
    can_light_beacon,
    describe_location,
    is_win,
    LOCATIONS,
    STARTING_ENERGY,
)


class TestNewGame(unittest.TestCase):
    def test_t1_new_game_defaults(self):
        p = new_game("Ada")
        self.assertEqual(p["location"], "Beach")
        self.assertEqual(p["energy"], 5)
        self.assertEqual(p["inventory"], [])
        self.assertFalse(p["game_over"])
        self.assertFalse(p["won"])


class TestInvalidInput(unittest.TestCase):
    def test_t2_invalid_command_does_not_mutate(self):
        p = new_game("Ada")
        for command in (
            "banana", "", "   ", "go sideways", "go south", "take lantern",
            "cross bridge", "light beacon",
        ):
            with self.subTest(command=command):
                p = new_game("Ada")
                before = deepcopy(p)
                result = apply_action(p, command)
                self.assertFalse(result["ok"])
                self.assertFalse(result["energy_used"])
                self.assertEqual(p, before)

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

    def test_lantern_collected_once_without_cost(self):
        p = new_game("Ada")
        apply_action(p, "north")
        apply_action(p, "east")
        result = apply_action(p, "take lantern")
        self.assertTrue(result["ok"])
        self.assertFalse(result["energy_used"])
        self.assertEqual(p["energy"], 3)
        before = deepcopy(p)
        result = apply_action(p, "take lantern")
        self.assertFalse(result["ok"])
        self.assertEqual(p, before)

    def test_rope_pickup_is_free(self):
        p = new_game("Ada")
        apply_action(p, "north")
        result = apply_action(p, "take rope")
        self.assertTrue(result["ok"])
        self.assertFalse(result["energy_used"])
        self.assertEqual(p["energy"], 4)


class TestPuzzles(unittest.TestCase):
    def test_t6_bridge_blocked_without_rope(self):
        p = new_game("Ada")
        apply_action(p, "go north")
        apply_action(p, "go east")
        apply_action(p, "go north")
        self.assertEqual(p["location"], "Old Bridge")
        self.assertFalse(can_cross_bridge(p))
        before = deepcopy(p)
        r = apply_action(p, "cross bridge")
        self.assertFalse(r["ok"])
        self.assertEqual(p, before)

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
        before = deepcopy(p)
        r = apply_action(p, "light beacon")
        self.assertFalse(r["ok"])
        self.assertEqual(p, before)

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
        self.assertEqual(p["location"], "Lighthouse")
        self.assertEqual(p["energy"], 1)
        self.assertFalse(r["energy_used"])
        self.assertTrue(is_win(p))

    def test_cannot_light_beacon_at_wrong_location_with_items(self):
        p = new_game("Ada")
        p["inventory"] = ["rope", "lantern"]
        before = deepcopy(p)
        self.assertFalse(can_light_beacon(p))
        result = apply_action(p, "light beacon")
        self.assertFalse(result["ok"])
        self.assertEqual(p, before)

    def test_crossing_bridge_costs_exactly_one_energy(self):
        p = new_game("Ada")
        p["location"] = "Old Bridge"
        p["inventory"] = ["rope"]
        result = apply_action(p, "cross bridge")
        self.assertTrue(result["ok"])
        self.assertTrue(result["energy_used"])
        self.assertEqual(p["location"], "Lighthouse")
        self.assertEqual(p["energy"], 4)

    def test_puzzle_checks_do_not_change_state(self):
        p = new_game("Ada")
        p["location"] = "Old Bridge"
        p["inventory"] = ["rope", "lantern"]
        before = deepcopy(p)
        self.assertTrue(can_cross_bridge(p))
        self.assertFalse(can_light_beacon(p))
        self.assertEqual(p, before)

    def test_puzzle_checks_reject_finished_game(self):
        for location, check in (
            ("Old Bridge", can_cross_bridge), ("Lighthouse", can_light_beacon),
        ):
            with self.subTest(location=location):
                p = new_game("Ada")
                p["location"] = location
                p["inventory"] = ["rope", "lantern"]
                p["game_over"] = True
                self.assertFalse(check(p))


class TestEnergy(unittest.TestCase):
    def test_t9_energy_exhaustion_causes_loss(self):
        p = new_game("Ada")
        p["energy"] = 1
        apply_action(p, "go north")
        self.assertEqual(p["energy"], 0)
        self.assertTrue(p["game_over"])
        self.assertFalse(p["won"])

    def test_cannot_move_after_game_over(self):
        for command in ("north", "take rope", "light beacon", "quit", "look"):
            with self.subTest(command=command):
                p = new_game("Ada")
                p["game_over"] = True
                before = deepcopy(p)
                result = apply_action(p, command)
                self.assertFalse(result["ok"])
                self.assertEqual(p, before)

    def test_final_energy_point_on_bridge_causes_loss_before_beacon(self):
        p = new_game("Ada")
        p["location"] = "Old Bridge"
        p["inventory"] = ["rope", "lantern"]
        p["energy"] = 1
        result = apply_action(p, "cross bridge")
        self.assertTrue(result["ok"])
        self.assertEqual(p["location"], "Lighthouse")
        self.assertEqual(p["energy"], 0)
        self.assertTrue(p["game_over"])
        self.assertFalse(p["won"])
        before = deepcopy(p)
        self.assertFalse(apply_action(p, "light beacon")["ok"])
        self.assertEqual(p, before)

    def test_losing_path_stops_at_zero(self):
        p = new_game("Ada")
        for command in ("north", "south", "north", "south", "north"):
            apply_action(p, command)
        self.assertEqual(p["energy"], 0)
        self.assertTrue(p["game_over"])
        self.assertFalse(is_win(p))
        self.assertFalse(apply_action(p, "south")["ok"])
        self.assertEqual(p["energy"], 0)

    def test_beacon_requires_positive_energy_even_in_prepared_state(self):
        p = new_game("Ada")
        p["location"] = "Lighthouse"
        p["inventory"] = ["lantern"]
        p["energy"] = 0
        before = deepcopy(p)
        self.assertFalse(can_light_beacon(p))
        self.assertFalse(apply_action(p, "light beacon")["ok"])
        self.assertEqual(p, before)


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
        self.assertIsNot(fresh["inventory"], old["inventory"])

    def test_new_games_have_independent_inventories(self):
        first = new_game("Ada")
        second = new_game("Bea")
        self.assertIsNot(first["inventory"], second["inventory"])
        first["inventory"].append("rope")
        self.assertEqual(second["inventory"], [])


class TestMenuAndInformation(unittest.TestCase):
    def test_menu_and_information_do_not_change_state(self):
        p = new_game("Ada")
        before = deepcopy(p)
        self.assertIn("go north", available_actions(p))
        self.assertIn("trail", describe_location(p))
        for command in ("look", "inventory"):
            result = apply_action(p, command)
            self.assertTrue(result["ok"])
            self.assertFalse(result["energy_used"])
        self.assertEqual(p, before)

    def test_menu_and_scene_stop_offering_collected_item(self):
        p = new_game("Ada")
        apply_action(p, "north")
        self.assertIn("take rope", available_actions(p))
        self.assertIn("You see a rope here.", describe_location(p))
        apply_action(p, "take rope")
        self.assertNotIn("take rope", available_actions(p))
        self.assertNotIn("You see a rope here.", describe_location(p))

    def test_no_actions_after_game_over(self):
        p = new_game("Ada")
        apply_action(p, "quit")
        self.assertEqual(available_actions(p), [])

    def test_quit_aliases_accept_case_and_whitespace_without_energy_cost(self):
        for command in ("quit", " EXIT ", " Q "):
            with self.subTest(command=command):
                p = new_game("Ada")
                result = apply_action(p, command)
                self.assertTrue(result["ok"])
                self.assertFalse(result["energy_used"])
                self.assertEqual(p["energy"], 5)
                self.assertEqual(p["location"], "Beach")
                self.assertEqual(p["inventory"], [])
                self.assertTrue(p["game_over"])
                self.assertFalse(is_win(p))


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
