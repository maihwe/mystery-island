"""
Mystery Island — The Lost Lighthouse
Game rules without input() or print(). apply_action changes the supplied state;
the other public functions only read state or create a new one.
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

SCENES = {
    "Beach": "You wake beside the wreck of your boat. A trail leads north into the jungle.",
    "Jungle": "Vines cover the trail. The beach is south; a cave entrance is east.",
    "Cave": "You shelter beneath cool stone. The jungle is west; the old bridge is north.",
    "Old Bridge": "The broken bridge leads to the lighthouse. You need rope to cross safely.",
    "Lighthouse": "The beacon is dark. Use a lantern to light it and signal the rescue boat.",
}


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
    Return commands to show in the menu. Puzzle commands can still be blocked
    by missing items. This function does not change the player.
    """
    if player["game_over"]:
        return []

    loc = player["location"]
    actions = []

    # Movement
    for direction in LOCATIONS.get(loc, {}):
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


def describe_location(player):
    """Return the scene and mention any item that has not been collected."""
    location = player["location"]
    description = SCENES[location]
    item = PICKUPS.get(location)
    if item and item not in player["inventory"]:
        description += f" You see a {item} here."
    return description


def can_cross_bridge(player):
    """Return whether an active player at the bridge has rope and energy."""
    return (
        not player["game_over"]
        and player["energy"] > 0
        and player["location"] == "Old Bridge"
        and "rope" in player["inventory"]
    )


def can_light_beacon(player):
    """Return whether the player can light the beacon before energy runs out."""
    return (
        not player["game_over"]
        and player["energy"] > 0
        and player["location"] == "Lighthouse"
        and "lantern" in player["inventory"]
    )


def is_win(player):
    """Return whether the game ended in a rescue."""
    return player["game_over"] and player["won"]


def _end_game(player, won):
    """Set the end flags and return the outcome message."""
    player["game_over"] = True
    player["won"] = won
    if won:
        return "You lit the beacon! A rescue boat is on its way."
    return "You ran out of energy before rescue. The island claims another sailor."


def _move_player(player, destination, message):
    """Apply one legal move, charge one energy, and check for exhaustion."""
    player["location"] = destination
    player["energy"] = max(0, player["energy"] - 1)
    if player["energy"] == 0:
        message += " " + _end_game(player, won=False)
    return {"ok": True, "message": message, "energy_used": True}


def apply_action(player, action):
    """Apply a text command in place and return ok, message, and energy_used.

    Rejected commands leave the whole player dictionary unchanged.
    """
    action = action.strip().lower()
    result = {"ok": False, "message": "", "energy_used": False}

    if player["game_over"]:
        result["message"] = "The game is over."
        return result

    # Quit changes the end flags; informational commands below do not.
    if action in {"quit", "exit", "q"}:
        player["game_over"] = True
        player["won"] = False
        result.update(ok=True, message="You abandon the island. Game over.")
        return result

    if action == "look":
        result.update(ok=True, message=describe_location(player))
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
        return _move_player(player, dest, f"You travel {direction} to the {dest}.")

    # Bridge
    if action == "cross bridge":
        if player["location"] != "Old Bridge":
            result["message"] = "There is no bridge here."
            return result
        if not can_cross_bridge(player):
            result["message"] = "The bridge is broken. You need a rope to cross safely."
            return result
        return _move_player(
            player, "Lighthouse", "You cross the bridge to the Lighthouse."
        )

    # Beacon
    if action == "light beacon":
        if player["location"] != "Lighthouse":
            result["message"] = "There is no beacon here."
            return result
        if not can_light_beacon(player):
            result["message"] = "You need a lantern and remaining energy to light the beacon."
            return result
        result.update(ok=True, message=_end_game(player, won=True))
        return result

    result["message"] = "I don't understand that action."
    return result

