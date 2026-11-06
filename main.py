"""
Mystery Island — The Lost Lighthouse
CLI entry point. Handles input()/print() only; delegates to game.py.
Run:  python main.py
"""

from game import new_game, apply_action, available_actions, LOCATIONS


def print_title():
    print("=" * 60)
    print("        MYSTERY ISLAND — THE LOST LIGHTHOUSE")
    print("=" * 60)
    print("You wake on a storm-wrecked beach. The lighthouse is dark,")
    print("the bridge is broken, and a rescue boat needs a beacon to find you.")
    print("Explore, collect what you need, restore the light, and survive.")
    print("Energy starts at 5. Every move costs 1 energy. Invalid input is free.")
    print("Type 'look' to inspect, 'inventory' to check your bag, 'quit' to leave.")
    print("=" * 60)


def show_status(player):
    print(f"\n[{player['name']}] Location: {player['location']} | "
          f"Energy: {player['energy']} | Inventory: "
          f"{player['inventory'] if player['inventory'] else 'empty'}")
    acts = available_actions(player)
    if acts:
        print("Options: " + " | ".join(acts))


def prompt_loop(player):
    """Main game loop. Returns when game_over is True."""
    while not player["game_over"]:
        show_status(player)
        raw = input("\n> ")
        result = apply_action(player, raw)
        print(result["message"])

    # Final message
    if player["won"]:
        print(f"\n*** YOU WIN, {player['name']}! ***")
    else:
        print(f"\n*** GAME OVER, {player['name']}. ***")


def ask_yes_no(prompt):
    """Robust yes/no reader. Loops until a valid answer."""
    while True:
        ans = input(prompt).strip().lower()
        if ans in {"y", "yes"}:
            return True
        if ans in {"n", "no"}:
            return False
        print("Please answer 'y' or 'n'.")


def main():
    print_title()
    name = input("What is your name, sailor? ").strip() or "Sailor"
    while True:
        player = new_game(name)
        prompt_loop(player)
        if not ask_yes_no("Play again? (y/n): "):
            print("Fair winds. Goodbye.")
            break
        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()