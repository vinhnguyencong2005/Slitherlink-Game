from solver_dfs import solve_with_dfs
from solver_algorithm2 import solve_with_algorithm_2

ALGORITHM_LABELS = {
    1: "DFS",
    2: "Heuristic",
}


def run_solver(algorithm_id, cells):
    """Dispatch to the selected solver and return a normalized result dict."""
    if algorithm_id == 1:
        return solve_with_dfs(cells, include_backtracking_steps=True)
    if algorithm_id == 2:
        return solve_with_algorithm_2(cells, include_backtracking_steps=True)
    return {
        "solved": False,
        "steps": [],
        "final_state": {},
        "message": f"Unknown algorithm id: {algorithm_id}",
    }
