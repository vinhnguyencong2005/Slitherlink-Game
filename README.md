# Slitherlink Solver (Pygame)

A simple Slitherlink game UI with step playback for solver algorithms.

## Quick start

### 1) Open project folder
- Open this folder in VS Code: `c:\Study\Slitherlink`

### 2) Create/activate virtual environment (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) Install dependency
```powershell
pip install pygame
```

### 4) Run the game
```powershell
python .\setup.py
```

## How to use in game

- In menu, choose algorithm by mouse click or key:
	- `1` = DFS
	- `2` = Heuristic (Algorithm 2)
- In game:
	- `S` solve using selected algorithm
	- `N` apply next solver step
	- `A` toggle autoplay
	- `R` reset board
	- `M` return to menu
- Mouse:
	- Left click toggles line on/off
	- Right click toggles X mark on/off

## Project structure (important files)

- `setup.py`:
	- Main game loop, event handling, rendering, and solver playback.
- `app_config.py`:
	- Shared app/grid constants (window size, grid size, cell size, autoplay speed).
- `board_utils.py`:
	- Board/coordinate helpers (pixel↔grid conversion, click hit-test, apply step, reset).
- `solver_dfs.py`:
	- Working DFS solver implementation.
- `solver_algorithm2.py`:
	- Template for Algorithm 2 implementation.
- `algorithm_runner.py`:
	- Central solver dispatcher (`run_solver`) and display labels (`ALGORITHM_LABELS`).

## Implementing Algorithm 2 (developer guide)

### Goal
Implement `solve_with_algorithm_2(cells, include_backtracking_steps=True)` in `solver_algorithm2.py`.

### Required return format
Your function must return:

```python
{
		"solved": bool,
		"steps": [
				{"edge": ((x1, y1), (x2, y2)), "value": True|False|None, "reason": "text"},
				...
		],
		"final_state": {edge: True|False|None}
}
```

### Rules for steps
- `edge` must be **grid coordinates** (not pixels).
- `value=True` means draw line.
- `value=False` means mark blocked (shown as X in UI).
- `value=None` means clear/revert step (useful for backtracking visual playback).
- Add a short `reason` so users can understand each decision in step mode.

### Wiring status
This is already connected:
- `setup.py` calls `run_solver(selected_algorithm, cells)`.
- `algorithm_runner.py` already routes:
	- `1 -> solve_with_dfs`
	- `2 -> solve_with_algorithm_2`

So once Algorithm 2 is implemented in `solver_algorithm2.py`, pressing `S` with algorithm 2 selected will run it automatically.

### Suggested implementation workflow
1. Start by returning deterministic steps only (no backtracking).
2. Verify playback with `N` step-by-step.
3. Add backtracking (if needed), emit `None` steps on undo.
4. Ensure `final_state` matches final board decision state.
5. Keep API compatible with DFS output format.

## Notes

- Puzzle clues currently load from `puzzles_example.py` (`example_clues_1`).
- Grid/window sizing is controlled via `app_config.py`.
- If PowerShell blocks script activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
