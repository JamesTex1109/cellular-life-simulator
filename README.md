# Cellular Life Simulator

A cellular automaton written in pure Python, in the same family as Conway's Game of Life but with a custom 5-state rule set driven by number theory. Every cell looks at its neighbors, computes an influence score, and then lives, dies, or changes state depending on whether that score is prime, Fibonacci, or a power of two. The grid evolves for 100 generations and the final state is written to a file.

## Cell States

| Symbol | State | Value |
|---|---|---|
| `O` | Strong positive | +3 |
| `o` | Weak positive | +1 |
| `.` | Dead | 0 |
| `x` | Weak negative | -1 |
| `X` | Strong negative | -3 |

## How It Works

**Influence score:** each cell checks a 5×5 window around itself.
- **Inner ring:** the 8 cells touching it
- **Outer ring:** the 16 cells one step further out
- `influence = 2 × inner_sum + outer_sum`

Close neighbors count double, the same way a crowd right next to you affects you more than one across the room.

**Transition rules (applied to every cell each generation):**

| Current | Becomes | When |
|---|---|---|
| `O` | `.` | influence is a power of two |
| | `o` | outer sum < 2 |
| `o` | `O` | inner sum is a Fibonacci number |
| | `.` | influence ≤ 0 |
| `.` | `o` | influence is prime |
| | `x` | influence is negative and \|influence\| is prime |
| `x` | `X` | inner sum is negative and \|inner sum\| is Fibonacci |
| | `.` | influence ≥ 0 |
| `X` | `.` | influence is negative and \|influence\| is a power of two |
| | `x` | outer sum > -2 |

Otherwise the cell stays the same. All cells update at the same time from a copy of the previous grid, so a cell's new state never affects its neighbors within the same generation.

## Run It

Only the Python standard library is needed (no NumPy).

```bash
python3 cellular_life.py -i input.txt -o output.txt
```

The input file is a grid of symbols, one row per line:
```
..O..
.oXo.
O.x.O
.oXo.
..O..
```

| Flag | Meaning |
|---|---|
| `-i` | Input grid file (required) |
| `-o` | Output file (required) |
| `-p` | Process count (reserved for the parallel version) |

## Notes
- This is the serial version. A parallel version using Python's `multiprocessing` splits the grid into row chunks across worker processes.
- Tested for correctness against 15 reference test cases.
