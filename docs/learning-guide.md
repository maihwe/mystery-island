# Learn Python through the working game

Use the finished game as something to run, inspect, and experiment with. Work
through these sessions in order. The suggested total is 6–10 focused hours;
move on when you can explain the checkpoint, rather than when a timer expires.
For experiments that change code, make a small Git branch and keep the original
tests. A changed rule needs updated documentation and a test for that rule.

## Session 1: variables, values, and input (45–60 minutes)

A variable is a name referring to a value. Assignment such as `coins = 5` binds
that name to the integer value `5`. A string (`str`) represents text; an integer
(`int`) represents a whole number; a boolean (`bool`) is `True` or `False`.
An f-string such as `f"Coins: {coins}"` inserts a value into text.

Read `new_game` in `game.py` and the name prompt in `main.py`.

Your exercises:

1. In an unrelated nickname script, ask for a nickname, print a welcome message,
   and store and display `score = 0`.
2. Predict the types of `"5"`, `5`, `False`, and the value returned by `input()`
   when someone types `5`. Then check with `type()` in a Python shell.
3. Run Mystery Island with your own name, then with a blank name. Explain the
   effect of `.strip() or "Sailor"` after experimenting with an empty string.

Checkpoint: explain why `player["energy"]` is an integer, while a typed command
is a string, even if the player types a number.

## Session 2: dictionaries, lists, and state (45–75 minutes)

A dictionary maps keys to values: `player["location"]` looks up one value by
its key. A list is an ordered collection of values. This game uses a list for
inventory because it stores a small collection of item names. `"rope" in items`
tests whether an equal item is present; it does not add anything. `append` adds
an item, and `not in` lets the game reject duplicates before adding them.

Read `LOCATIONS`, `PICKUPS`, `new_game`, and the pickup branch in `apply_action`.

Your exercises:

1. Make an unrelated list containing `"map"`. Add `"key"` only if absent; try
   twice and inspect the list. Remove the key only if it is present.
2. Draw all five game locations and label every allowed direction. Explain the
   difference between `LOCATIONS["Beach"]` and `LOCATIONS["Beach"]["north"]`.
3. Create two players in a Python shell using `new_game`. Add rope to the first
   player's inventory. Predict and inspect the second player's inventory.

Checkpoint: explain why creating an empty list once outside `new_game` and
reusing it could make one player's pickups appear in another game.

## Session 3: conditions and consequences (45–75 minutes)

An `if` executes its indented block when its condition is true. In an
`if`/`elif`/`else` chain, the first matching branch runs. `==` compares values;
`=` assigns. `and` requires both conditions; `or` requires at least one; `not`
reverses truth. Early `return` statements in `apply_action` stop the current
function call as soon as that command is handled.

Read `can_cross_bridge`, `can_light_beacon`, and their command branches.

Your exercises:

1. Write the unrelated weather drill: print `safe` only when temperature is
   above 15 and it is not raining. Check all four combinations of warm/cold and
   raining/not raining.
2. Make a truth table for being at Old Bridge and holding rope. Then include
   whether the game has ended and whether energy is positive.
3. Play without taking rope, then try crossing. Play another game taking rope
   but leaving the lantern, then try lighting the beacon. Write down the actual
   state before and after each blocked action.

Checkpoint: explain why having a lantern while at Beach cannot win the game.

## Session 4: loops and validation (45–75 minutes)

A `while` loop repeats while its condition is true. A `for` loop visits values
from a collection. `break` exits the nearest enclosing loop; `return` exits a
function. In `main.py`, `prompt_loop` repeats commands while `game_over` is
false, and `main` repeats whole games until the replay answer is no.

`.strip()` removes surrounding whitespace, and `.lower()` makes text lowercase.
Normalization happens before the command comparisons. No broad exception
handler is needed to reject unknown command strings.

Your exercises:

1. Write an unrelated loop accepting only `north`, `south`, and `quit`. Try
   blank input, `NORTH`, `banana`, and `quit`, recording what happens.
2. Trace `prompt_loop` for one invalid command and one legal move. Identify
   exactly when its stopping condition changes after a loss or quit.
3. Run the real game with ` EXIT `, then answer `banana` at the replay prompt,
   followed by `n`. Explain why the retry does not start a new game.

Checkpoint: distinguish stopping the current game from stopping the replay
loop. Explain why invalid input spends no energy.

## Session 5: functions, returns, and mutation (60–90 minutes)

A function packages one task. Parameters are the names receiving the arguments
passed to it. `return` sends a value to the caller. `print` displays text and
returns `None`; printed text is not a replacement for a boolean result.
A docstring describes a function's job. Scope describes where a name can be
used. Passing a dictionary into a function gives it access to that object, so
changing a dictionary entry changes the player's shared state.

Read each function using the responsibility table in `requirements.md`.

Your exercises:

1. Write an unrelated `has_key(inventory)` function that returns a boolean.
   Call it with a key present and absent. Save its return value in a variable.
2. Call `can_cross_bridge` and inspect the player before and after. Do the same
   with a legal `apply_action`. Explain why one reads and the other changes
   state. Both can be tested without typing into a game menu.
3. Read `_move_player`: explain every line and why both normal movement and
   bridge crossing call it. Read `_end_game` and identify its state changes.

Checkpoint: explain why the game dictionary lives outside the input handler
and why a puzzle check returns a boolean instead of printing and spending energy.

## Session 6: tests and a small independent change (60–120 minutes)

A `unittest.TestCase` groups checks. Assertions compare actual behavior with
expected behavior: `assertEqual`, `assertTrue`, and `assertFalse` are examples.
A useful test fails when a requirement is broken. A snapshot for mutation tests
must include a separate inventory list; `deepcopy` also copies nested values.

Your exercises:

1. Write an unrelated `is_even(n)` and two tests with concrete expected answers.
2. Run all game tests. Explain one test each for invalid input, movement,
   pickup, bridge, beacon, exhaustion, and replay. Explain why the starting
   energy test asserts the literal `5`, not only a value imported from the code.
3. Predict what would fail if `_move_player` charged two energy instead of one.
   On a practice branch, make that one-line change, run the suite, read the
   failures, and restore the correct rule. Record that this was an experiment.
4. Choose one small requirement yourself, such as accepting `bag` as an alias
   for `inventory`. Write a test for it **before** implementing it. Run and
   record the failure, attempt the smallest fix, rerun, and update the README.

Use `TestCLI` as evidence that the actual program works beyond isolated
functions. Some unit tests prepare a particular location or energy directly;
the full winning and losing paths check that outcomes are also reachable
through ordinary commands.

Checkpoint: show your independently written test, its failure, the small code
change, and the passing result. Explain why it proves the new requirement.

## Session 7: Git, evidence, and defence (45–75 minutes)

A Git branch gives your change a named line of work. A commit records a snapshot
of tracked changes. A test result is evidence for the version you ran, so run
tests again after changing behavior and record the final commit separately.

Your exercises:

1. Use `git status` and `git diff` to explain your change. Keep `.venv` and
   `__pycache__` untracked. Make a meaningful commit for your independent work.
2. Complete two entries in `learning-log.md` using predictions and experiments
   you actually performed. Write the reflection in your own words.
3. Demonstrate a win, a loss, invalid input recovery, and replay. Run at least
   eight meaningful tests (the full suite is recommended).
4. Ask a mentor or peer for review. Submit the actual repository URL, final
   commit SHA, Python version, run instructions, and test output.

Defence questions to answer without reading a prepared answer:

1. Why did you choose a list for inventory?
2. What stops each of the two game loops?
3. Which function returns a value rather than prints it? Show its caller.
4. What bug or new requirement did you first capture in your own test?
5. What did AI explain, and what experiment did you use to check it?

## How to ask for help during these sessions

Send the session number, your prediction, the smallest relevant code, and the
actual output. Ask for a hint or a review before requesting a solution. For
example: “Session 2: I predicted the second player would also have rope, but
its inventory stayed empty. Here is my experiment. Help me explain why.”

You requested a concrete implementation first, so this repository includes
AI-written changes and tests. Attribute those honestly. Your own exercises,
test-first change, explanations, and experiments are the evidence of mastery
you can carry into your next projects.
