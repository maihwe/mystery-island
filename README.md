# Mystery Island — The Lost Lighthouse

A Python terminal adventure. Explore five locations, collect rope and a lantern,
cross the broken bridge, and restore the lighthouse beacon before your energy
runs out. The game uses only the Python standard library.

## Prerequisites

- Python 3.9 or newer.
- A terminal opened in this repository.
- No external packages, network connection, or API keys.

## How to run

If your terminal already has a `python` command:

```bash
python main.py
```

On Linux or macOS, if only `python3` is available, create and activate a local
environment. This also gives you the `python` command used in the assignment:

```bash
python3 -m venv --without-pip .venv
source .venv/bin/activate
python main.py
```

`--without-pip` is sufficient because this project needs no installed packages.
After reopening your terminal, activate the environment again. Alternatively,
run `python3 main.py` directly. On Windows, `py main.py` is also an option.

## Controls

Enter a command displayed after `Options:` and press Enter. The menu repeats
after each action until you win, lose, or quit. Enter your name at startup; a
blank name becomes `Sailor`.

| Command | Effect |
| --- | --- |
| `go north`, `go south`, `go east`, `go west` | Move along a route from your current location. |
| `north`, `south`, `east`, `west` | Short forms of the movement commands. |
| `take rope` | Collect rope in the Jungle, once per game. |
| `take lantern` | Collect the lantern in the Cave, once per game. |
| `cross bridge` | Travel from Old Bridge to Lighthouse if you have rope. |
| `light beacon` | Win at Lighthouse if you have a lantern and energy remaining. |
| `look` | Read the current scene and see any uncollected object. |
| `inventory` | Display your collected objects. |
| `quit`, `exit`, `q` | End the current game without winning. |

Commands ignore case and surrounding spaces: `  NORTH  ` and ` EXIT ` work.
This is a text-command menu; numbers such as `1` are rejected. Unknown commands,
blank commands, unavailable directions, and blocked puzzle actions display a
message and leave all player state unchanged.

## Map and game rules

```text
Beach -> Jungle -> Cave -> Old Bridge -> Lighthouse
  north     east     north      cross bridge (requires rope)
```

| Location | Normal routes | Object |
| --- | --- | --- |
| Beach | north to Jungle | none |
| Jungle | south to Beach; east to Cave | rope |
| Cave | west to Jungle; north to Old Bridge | lantern |
| Old Bridge | south to Cave; use `cross bridge` to reach Lighthouse | none |
| Lighthouse | south to Old Bridge | none |

- Every new game starts at Beach with **5 energy**, an empty inventory, and
  `game_over=False`, `won=False`.
- Every successful movement costs **exactly 1 energy**, including crossing the
  bridge and going back. Being at a location does not charge extra energy.
- Picking up objects, inspecting, checking inventory, and lighting the beacon
  cost **0 energy**. There is no free starting move or energy refill.
- Rope and lantern can each be collected only once. They are kept after use.
  A repeated pickup is rejected without changing state.
- Old Bridge has no normal north route: you must use `cross bridge` with rope.
  The menu shows puzzle commands even when an item is missing, so you can try
  them and learn what is required.
- You win only by using `light beacon` at Lighthouse with a lantern while
  energy is greater than zero. Arriving at Lighthouse alone does not win.
- Spending your final energy point completes that move, then immediately
  causes a loss. Energy stops at zero; later actions cannot change the state.
- After a win, loss, or quit, answer `y`/`yes` to replay or `n`/`no` to leave.
  Other replay answers are retried. Replay keeps your name but creates a new
  state and a new empty inventory list.
- Ctrl+C or end of input closes the CLI with a goodbye message.
- The rules are deterministic: the same state and command give the same result.

Three decisions have concrete consequences: taking or leaving the rope changes
whether you can cross; taking or leaving the lantern changes whether you can
light the beacon; moving forward or backtracking spends limited energy and can
determine whether you survive.

## Demonstration paths

Winning example, with energy after each move:

```text
Name: Ada
> north          # Jungle, energy 4
> take rope
> east           # Cave, energy 3
> take lantern
> north          # Old Bridge, energy 2
> cross bridge   # Lighthouse, energy 1
> light beacon
*** YOU WIN, Ada! ***
Play again? (y/n): n
```

The `#` annotations above are explanations; type only the command before them.

Losing path: `north`, `south`, `north`, `south`, `north`. The fifth move exhausts
energy and displays `YOU LOSE`. Invalid-input path: enter a blank command, then
`banana`, then `  NORTH  `; you stay at Beach with 5 energy after the first two
commands and move to Jungle with 4 energy after the third.

## Run tests

```bash
python -m unittest discover -s tests -v
```

If you run without the environment and only have `python3`, use
`python3 -m unittest discover -s tests -v`. The suite contains **36 tests**:
29 for game rules and 7 that launch the real CLI with scripted input. These
cover all ten acceptance rules, win/loss paths, unique pickups, input handling,
bridge energy costs, finished-game protection, and replay.

Actual test output and game transcripts are saved in
[verification.txt](docs/verification.txt). They describe the tested working
tree; rerun tests after changing code.

## Understand and explain the code

| File | Responsibility |
| --- | --- |
| `main.py` | Print the story and menus, read commands, repeat games, and handle terminal interruption. |
| `game.py` | Store the map and apply deterministic rules to the player dictionary. |
| `tests/test_game.py` | Check decisions and state changes without interactive typing. |
| `tests/test_cli.py` | Run complete terminal sessions, including replay and invalid input. |

`apply_action` changes the supplied player dictionary and returns a result
dictionary. It is testable without terminal input, but it is not a pure
function: it mutates state. Functions such as `can_cross_bridge` only read state
and return a boolean. `new_game` creates a new dictionary and inventory each
time. These distinctions matter when explaining the implementation.

Use [the concrete requirements](docs/requirements.md) to check behavior and
[the learning guide](docs/learning-guide.md) to practice the Python concepts in
this game. Record your own experiments in [the learning log](docs/learning-log.md).

## Known limits

- Terminal text only; one player, one winning route, and no saved progress.
- No random events, combat, item dropping, or energy recovery.
- Commands use the documented English words; arbitrary natural-language
  sentences and extra spaces inside `cross bridge` are not understood.
- The game API expects a player dictionary created by `new_game` and a string
  command. It does not validate every possible manually corrupted dictionary.
- The built game and passing tests do not verify your understanding. The
  explanations, learning-log entries, personal bug fix, and oral defence are
  still work you must demonstrate yourself.

## Git and submission evidence

The repository includes a `.gitignore` for virtual environments and Python
cache files. Before submitting your own work:

1. Run the game demonstrations and tests above.
2. Record `python --version` and the test output for your final code.
3. Make your own meaningful commits, and record the final `git rev-parse HEAD`.
4. Supply your actual GitHub repository URL after pushing your work.
5. Complete two learning-log entries and the reflection paragraph.
6. Ask a mentor or peer to review your changes and explain the functions aloud.

The learning log distinguishes AI contributions from your own experiments;
its blank fields must be filled with real evidence.
