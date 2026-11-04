"""
Mystery Island — The Lost Lighthouse
Pure game logic. No print() or input() calls here so functions are testable.
"""

STARTING_ENERGY = 5

# Locations map: name -> dict of direction -> destination
# Moves consume energy. Only listed directions are legal from that location.
LOCATIONS = {
    "Beach": {"north": "Jungle"},
    "Jungle": {"south": "Beach", "east": "Cave"},
    "Cave": {"west": "Jungle", "north": "Old Bridge"},
    "Old Bridge": {"south": "Cave"},
    "Lighthouse": {"south": "Old Bridge"},
}

# Item pickups: location -> item available there (None means nothing to pick up)
PICKUPS = {
    "Beach": None,
    "Jungle": "rope",
    "Cave": "lantern",
    "Old Bridge": None,
    "Lighthouse": None,
}

VALID_DIRECTIONS = {"north", "south", "east", "west"}


def new_game(name):
    """Return a fresh player state dictionary."""
    return {
        "name": name,
        "location": "Beach",
        "energy": STARTING_ENERGY,
        "inventory": [],
        "game_over": False,
        "won": False,
    }


def available_actions(player):
    """
    Return a list of legal action strings for the current state.
    Keeps the game deterministic: same state -> same actions.
    """
    if player["game_over"]:
        return []

    loc = player["location"]
    actions = []

    # Movement
    for direction, dest in LOCATIONS.get(loc, {}).items():
        actions.append(f"go {direction}")

    # Pickup (only if something is there and not already held)
    item = PICKUPS.get(loc)
    if item and item not in player["inventory"]:
        actions.append(f"take {item}")

    # Context actions
    if loc == "Old Bridge":
        actions.append("cross bridge")
    if loc == "Lighthouse":
        actions.append("light beacon")

    actions.append("inventory")
    actions.append("look")
    actions.append("quit")
    return actions


def can_cross_bridge(player):
    """Bridge requires rope. Returns bool."""
    return player["location"] == "Old Bridge" and "rope" in player["inventory"]


def can_light_beacon(player):
    """Beacon requires lantern AND being at the Lighthouse."""
    return (
        player["location"] == "Lighthouse"
        and "lantern" in player["inventory"]
    )


def _end_game(player, won):
    """Set terminal flags. Centralised so rules stay consistent."""
    player["game_over"] = True
    player["won"] = won
    return {"message": "You lit the beacon! A rescue boat is on its way." if won
            else "You ran out of energy before rescue. The island claims another sailor."}


def apply_action(player, action):
    """Apply a single action string to the player dict (mutates in place)."""
    action = action.strip().lower()
    result = {"ok": False, "message": "", "energy_used": False}

    if player["game_over"]:
        result["message"] = "The game is over."
        return result

    # Informational / non-mutating
    if action == "quit":
        player["game_over"] = True
        player["won"] = False
        result.update(ok=True, message="You abandon the island. Game over.")
        return result

    if action == "look":
        result.update(ok=True, message=f"You are at the {player['location']}.")
        return result

    if action == "inventory":
        inv = player["inventory"]
        result.update(ok=True, message="Inventory: " + (", ".join(inv) if inv else "empty"))
        return result

    # Accept bare directions like "north" as shorthand for "go north"
    if action in VALID_DIRECTIONS:
        action = "go " + action

    # Pickup
    if action.startswith("take "):
        item = action[len("take "):].strip()
        here = PICKUPS.get(player["location"])
        if here is None:
            result["message"] = "There is nothing to take here."
            return result
        if item != here:
            result["message"] = f"No {item} here."
            return result
        if item in player["inventory"]:
            result["message"] = f"You already have the {item}."
            return result
        player["inventory"].append(item)
        result.update(ok=True, message=f"You pick up the {item}.")
        return result

    # Movement
    if action.startswith("go "):
        direction = action[len("go "):].strip()
        if direction not in VALID_DIRECTIONS:
            result["message"] = f"'{direction}' is not a direction."
            return result
        dest = LOCATIONS.get(player["location"], {}).get(direction)
        if dest is None:
            result["message"] = f"You cannot go {direction} from here."
            return result
        player["location"] = dest
        player["energy"] -= 1
        result["energy_used"] = True
        result["ok"] = True
        result["message"] = f"You travel {direction} to the {dest}."
        if player["energy"] <= 0:
            player["energy"] = 0
            result["message"] += " " + _end_game(player, won=False)["message"]
        return result

    # Bridge
    if action == "cross bridge":
        if player["location"] != "Old Bridge":
            result["message"] = "There is no bridge here."
            return result
        if not can_cross_bridge(player):
            result["message"] = "The bridge is broken. You need a rope to cross safely."
            return result
        player["location"] = "Lighthouse"
        player["energy"] -= 1
        result.update(ok=True, energy_used=True, message="You cross the bridge to the Lighthouse.")
        if player["energy"] <= 0:
            player["energy"] = 0
            result["message"] += " " + _end_game(player, won=False)["message"]
        return result

    # Beacon
    if action == "light beacon":
        if player["location"] != "Lighthouse":
            result["message"] = "There is no beacon here."
            return result
        if not can_light_beacon(player):
            result["message"] = "The beacon is dark. You need a lantern to light it."
            return result
        _end_game(player, won=True)
        result.update(ok=True, message="You raise the lantern and light the beacon! Its beam cuts through the storm. Rescue is coming.")
        return result

    result["message"] = "I don't understand that action."
    return result

