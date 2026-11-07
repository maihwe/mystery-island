"""
Mystery Island — The Lost Lighthouse
CLI entry point. Handles input()/print() only; delegates to game.py.
Run:  python main.py
"""

from game import (
    apply_action,
    available_actions,
    describe_location,
    is_win,
    new_game,
)


def print_title():
    """Display the story, controls, and energy rules."""
    print("=" * 60)
    print("        MYSTERY ISLAND — THE LOST LIGHTHOUSE")
    print("=" * 60)
    print("You wake on a storm-wrecked beach. The lighthouse is dark,")
    print("the bridge is broken, and a rescue boat needs a beacon to find you.")
    print("Explore, collect what you need, restore the light, and survive.")
    print("Energy starts at 5. Every move costs 1 energy. Invalid input is free.")
    print("Pickups, looking, and lighting the beacon are free.")
    print("Type a command shown in Options, such as 'go north' or 'take rope'.")
    print("Use 'look', 'inventory', or 'quit' ('exit' and 'q' also quit).")
    print("=" * 60)


def show_status(player):
    """Display the current state, scene, and command menu."""
    inventory = ", ".join(player["inventory"]) or "empty"
    print(
        f"\n[{player['name']}] Location: {player['location']} | "
        f"Energy: {player['energy']} | Inventory: {inventory}"
    )
    print(describe_location(player))
    actions = available_actions(player)
    if actions:
        print("Options: " + " | ".join(actions))


def prompt_loop(player):
    """Main game loop. Returns when game_over is True."""
    while not player["game_over"]:
        show_status(player)
        raw = input("\n> ")
        result = apply_action(player, raw)
        print(result["message"])

    # Final message
    if is_win(player):
        print(f"\n*** YOU WIN, {player['name']}! ***")
    elif player["energy"] == 0:
        print(f"\n*** YOU LOSE, {player['name']}: your energy ran out. ***")
    else:
        print(f"\n*** YOU QUIT, {player['name']}. ***")


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
    """Ask for a name and run games with a fresh state on each replay."""
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
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput ended. Fair winds. Goodbye.")
