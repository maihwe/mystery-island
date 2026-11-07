"""Run the real command line game with scripted player input."""

from pathlib import Path
import subprocess
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class TestCLI(unittest.TestCase):
    def run_game(self, commands):
        """Start main.py and return its output after checking it exited cleanly."""
        result = subprocess.run(
            [sys.executable, str(PROJECT_ROOT / "main.py")],
            input="\n".join(commands) + "\n",
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_winning_path(self):
        output = self.run_game([
            "Ada", "north", "take rope", "east", "take lantern", "north",
            "cross bridge", "light beacon", "n",
        ])
        self.assertIn("MYSTERY ISLAND", output)
        self.assertIn("Options:", output)
        self.assertIn("Location: Lighthouse | Energy: 1", output)
        self.assertIn("YOU WIN, Ada", output)
        self.assertIn("Play again?", output)
        self.assertIn("Fair winds. Goodbye.", output)

    def test_losing_path(self):
        output = self.run_game([
            "Ada", "north", "south", "north", "south", "north", "n",
        ])
        self.assertIn("YOU LOSE, Ada", output)
        self.assertIn("energy ran out", output)
        self.assertIn("Play again?", output)
        self.assertNotIn("YOU WIN", output)

    def test_invalid_input_recovers_and_exit_is_normalized(self):
        output = self.run_game(["Ada", "", "banana", "  NORTH  ", " EXIT ", "n"])
        self.assertEqual(output.count("I don't understand that action."), 2)
        self.assertEqual(output.count("Location: Beach | Energy: 5 | Inventory: empty"), 3)
        self.assertIn("Location: Jungle | Energy: 4", output)
        self.assertIn("YOU QUIT, Ada", output)

    def test_replay_creates_fresh_state(self):
        output = self.run_game([
            "Ada", "north", "take rope", "quit", " YES ", "inventory", "quit", "no",
        ])
        self.assertIn("Inventory: rope", output)
        self.assertEqual(output.count("Location: Beach | Energy: 5 | Inventory: empty"), 3)
        self.assertIn("Inventory: empty", output)
        self.assertEqual(output.count("YOU QUIT, Ada"), 2)

    def test_replay_rejects_unexpected_answer_then_accepts_no(self):
        output = self.run_game(["Ada", "quit", "banana", " N "])
        self.assertIn("Please answer 'y' or 'n'.", output)
        self.assertEqual(output.count("Play again?"), 2)
        self.assertIn("Fair winds. Goodbye.", output)

    def test_blank_name_uses_sailor(self):
        output = self.run_game(["   ", "quit", "n"])
        self.assertIn("[Sailor] Location: Beach", output)

    def test_end_of_input_exits_without_traceback(self):
        output = self.run_game(["Ada"])
        self.assertIn("Input ended. Fair winds. Goodbye.", output)


if __name__ == "__main__":
    unittest.main()
