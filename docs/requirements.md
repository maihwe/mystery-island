# Mystery Island: concrete requirements

This is the behavior contract for the implementation in this repository. Check
each rule by running the game or the named tests. Use the README for setup and
controls. The saved verification report records execution; it does not certify
your personal understanding.

## Player state

| Key | Python type | Initial value | Meaning |
| --- | --- | --- | --- |
| `name` | `str` | the entered name, or `Sailor` in the CLI | Display name; retained on replay. |
| `location` | `str` | `Beach` | One of the five names in `LOCATIONS`. |
| `energy` | `int` | `5` | Remaining legal moves. Never becomes negative through gameplay. |
| `inventory` | `list` of strings | `[]` | Collected objects; no duplicates. |
| `game_over` | `bool` | `False` | Stops the current game's menu. |
| `won` | `bool` | `False` | Becomes true only after successfully lighting the beacon. |

`apply_action(player, action)` modifies this dictionary for successful gameplay
actions and returns `{'ok': bool, 'message': str, 'energy_used': bool}`.
`ok=False` means the command was rejected; all player fields must remain
unchanged. `energy_used=True` means a legal movement spent one energy point.
An accepted `look` or `inventory` command also leaves state unchanged.

## Acceptance rules and evidence

| ID | Concrete requirement | Automated evidence |
| --- | --- | --- |
| T1 | `new_game(name)` starts at Beach with exactly 5 energy, empty inventory, and false end flags. | `TestNewGame.test_t1_new_game_defaults` |
| T2 | Unknown, blank, or contextually rejected commands do not change any field or spend energy. | `TestInvalidInput.test_t2_invalid_command_does_not_mutate` |
| T3 | One legal `go` changes to the mapped destination and subtracts exactly one energy. Bridge crossing also costs one. | `TestMovement.test_t3_legal_move_changes_location_and_energy_once`; `TestPuzzles.test_crossing_bridge_costs_exactly_one_energy` |
| T4 | A direction without a route from the current location is rejected without cost. | `TestInvalidInput.test_wrong_direction_rejected_without_cost` |
| T5 | Rope is collected in Jungle once, lantern in Cave once; pickups are free and repeats are rejected. | `TestInventory.test_t5_rope_collected_once`; `test_rope_pickup_is_free`; `test_lantern_collected_once_without_cost` |
| T6 | Crossing requires being at Old Bridge with rope. A normal north move cannot bypass the puzzle. | `TestPuzzles.test_t6_bridge_blocked_without_rope`; `test_t6b_old_bridge_has_no_direct_north_route` |
| T7 | Lighting requires being at Lighthouse with a lantern and positive energy during an active game. | `TestPuzzles.test_t7_beacon_blocked_without_lantern`; `test_cannot_light_beacon_at_wrong_location_with_items`; `TestEnergy.test_beacon_requires_positive_energy_even_in_prepared_state` |
| T8 | The full winning route reaches Lighthouse with 1 energy and sets both end flags when the beacon is lit. Lighting costs zero. | `TestPuzzles.test_t8_win_with_correct_items`; `TestCLI.test_winning_path` |
| T9 | A move using the final energy point completes, clamps energy at zero, and causes immediate loss. Reaching Lighthouse on the final point still loses. | `TestEnergy.test_t9_energy_exhaustion_causes_loss`; `test_final_energy_point_on_bridge_causes_loss_before_beacon`; `TestCLI.test_losing_path` |
| T10 | Replay creates fresh energy, location, end flags, and an independent empty inventory, retaining the name. | `TestReplay.test_t10_replay_resets_state`; `test_new_games_have_independent_inventories`; `TestCLI.test_replay_creates_fresh_state` |

Additional required CLI behavior:

- Print the title, instructions, player name prompt, scenes, and repeating menu.
- Display energy, location, and inventory before each command.
- Accept surrounding whitespace and mixed case; accept `quit`, `exit`, and `q`.
- Show distinct win, loss, and quit messages, followed by a replay prompt.
- Retry invalid replay answers; exit cleanly on end of input or Ctrl+C.
- Do not allow further state changes after `game_over=True`.
- Include all five locations and at least three decisions with consequences:
  collecting rope, collecting lantern, and advancing versus backtracking.

These are covered by the CLI tests and the menu, puzzle, and energy tests. Ctrl+C
handling is implemented at the CLI boundary; the suite checks EOF but does not
automate operating-system signal delivery.

## Function responsibilities you must explain

| Function | Inputs and output | Responsibility |
| --- | --- | --- |
| `new_game(name)` | name string → new dictionary | Create independent starting state. |
| `available_actions(player)` | state → list of command strings | Build a menu without changing state; puzzle choices may still be blocked. |
| `describe_location(player)` | state → scene string | Describe the location and an uncollected item. |
| `can_cross_bridge(player)` | state → boolean | Check active game, positive energy, Old Bridge, and rope. |
| `can_light_beacon(player)` | state → boolean | Check active game, positive energy, Lighthouse, and lantern. |
| `is_win(player)` | state → boolean | Read the two outcome flags. |
| `_end_game(player, won)` | state and boolean → message string | Set outcome flags. |
| `_move_player(player, destination, message)` | state, destination, message → result dictionary | Change location, charge one energy, and trigger loss if exhausted. |
| `apply_action(player, action)` | state and string → result dictionary | Normalize and validate commands, then apply the relevant rule. |
| `print_title()` | no arguments → `None` | Print the introduction and controls. |
| `show_status(player)` | state → `None` | Print status, scene, and menu. |
| `prompt_loop(player)` | state → `None` | Read and apply commands until the current game ends. |
| `ask_yes_no(prompt)` | prompt string → boolean | Retry until a valid replay answer is entered. |
| `main()` | no arguments → `None` | Ask for the name and create a fresh state for every game. |

The leading underscore in a helper name marks an internal convention; Python
does not make the function inaccessible. Functions that reach their end without
a `return` statement return `None`, even when they print text.

## Your mastery requirements

Complete the exercises in the learning guide. You are ready to defend the game
when you can do all of the following without copying an answer:

1. Name the types of all six player fields and explain assignment.
2. Trace the winning route's location, energy, and inventory after every action.
3. Explain why input is a string and why this game needs no integer conversion.
4. Show which loop repeats commands and which loop repeats whole games.
5. Explain why a boolean puzzle check should not spend energy or print a story.
6. Explain list membership and why a new game needs a new inventory list.
7. Predict the state after an invalid command and after a final-energy move.
8. Write a meaningful test yourself, observe a real failure, make a small fix,
   and show that the test then passes.
9. Explain every game and CLI function using the table above as a checklist.
10. Provide actual logs, test results, repository URL, final commit SHA, Python
    version, and your own reflection; do not substitute AI-written claims.
