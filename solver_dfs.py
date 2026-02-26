from collections import defaultdict


def canonical_edge(edge):
    """Return an edge in canonical (sorted endpoint) order for stable lookups."""
    a, b = edge
    return (a, b) if a <= b else (b, a)


def build_model(cells):
    """Build graph structures used by the solver from the clue grid."""
    max_col = max(pos[0] for pos in cells.keys())
    max_row = max(pos[1] for pos in cells.keys())
    cols = max_col + 1
    rows = max_row + 1

    edges = []
    for y in range(rows + 1):
        for x in range(cols):
            edges.append(((x, y), (x + 1, y)))
    for x in range(cols + 1):
        for y in range(rows):
            edges.append(((x, y), (x, y + 1)))

    cell_to_edges = {}
    edge_to_cells = defaultdict(list)
    for (cx, cy) in cells.keys():
        top = canonical_edge(((cx, cy), (cx + 1, cy)))
        right = canonical_edge(((cx + 1, cy), (cx + 1, cy + 1)))
        bottom = canonical_edge(((cx, cy + 1), (cx + 1, cy + 1)))
        left = canonical_edge(((cx, cy), (cx, cy + 1)))
        surrounding = (top, right, bottom, left)
        cell_to_edges[(cx, cy)] = surrounding
        for edge in surrounding:
            edge_to_cells[edge].append((cx, cy))

    vertex_to_edges = defaultdict(list)
    for edge in edges:
        ce = canonical_edge(edge)
        vertex_to_edges[ce[0]].append(ce)
        vertex_to_edges[ce[1]].append(ce)

    edges = [canonical_edge(edge) for edge in edges]
    return edges, cell_to_edges, edge_to_cells, vertex_to_edges


def solve_with_dfs(cells, include_backtracking_steps=True):
    """Solve a Slitherlink puzzle using propagation + DFS backtracking."""
    edges, cell_to_edges, edge_to_cells, vertex_to_edges = build_model(cells)
    state = {edge: None for edge in edges}
    steps = []

    def assign(edge, value, trail, reason, record_step=True):
        """Assign a value to an edge, recording it for undo and optional step history."""
        current = state[edge]
        if current is not None:
            return current == value
        state[edge] = value
        trail.append(edge)
        if record_step:
            steps.append({"edge": edge, "value": value, "reason": reason})
        return True

    def undo(trail, record_step=True):
        """Undo all assignments in trail (used when backtracking a branch)."""
        while trail:
            edge = trail.pop()
            state[edge] = None
            if record_step:
                steps.append({"edge": edge, "value": None, "reason": "backtrack"})

    def clue_status(cell_pos):
        """Return clue, count of True edges, and count of undecided edges for a cell."""
        clue = cells[cell_pos]
        if clue is None:
            return None, None, None
        around = cell_to_edges[cell_pos]
        true_count = sum(1 for edge in around if state[edge] is True)
        undecided_count = sum(1 for edge in around if state[edge] is None)
        return clue, true_count, undecided_count

    def vertex_status(vertex):
        """Return current vertex degree (True count) and undecided incident edges."""
        incident = vertex_to_edges[vertex]
        true_count = sum(1 for edge in incident if state[edge] is True)
        undecided = [edge for edge in incident if state[edge] is None]
        return true_count, undecided

    def propagate(trail, record_step=True):
        """Apply deterministic cell/vertex rules until no new assignments are found."""
        changed = True
        while changed:
            changed = False

            for cell_pos in cells.keys():
                clue, true_count, undecided_count = clue_status(cell_pos)
                if clue is None:
                    continue
                if true_count > clue or true_count + undecided_count < clue:
                    return False

                if undecided_count == 0:
                    continue

                if true_count == clue:
                    for edge in cell_to_edges[cell_pos]:
                        if state[edge] is None:
                            if not assign(edge, False, trail, f"cell {cell_pos} reached clue {clue}", record_step):
                                return False
                            changed = True

                elif true_count + undecided_count == clue:
                    for edge in cell_to_edges[cell_pos]:
                        if state[edge] is None:
                            if not assign(edge, True, trail, f"cell {cell_pos} must complete clue {clue}", record_step):
                                return False
                            changed = True

            for vertex in vertex_to_edges.keys():
                true_count, undecided = vertex_status(vertex)
                if true_count > 2:
                    return False

                if true_count == 1 and len(undecided) == 0:
                    return False

                if true_count == 2 and undecided:
                    for edge in undecided:
                        if not assign(edge, False, trail, f"vertex {vertex} already has degree 2", record_step):
                            return False
                        changed = True

                if true_count == 1 and len(undecided) == 1:
                    if not assign(undecided[0], True, trail, f"vertex {vertex} cannot end with degree 1", record_step):
                        return False
                    changed = True

                if true_count == 0 and len(undecided) == 1:
                    if not assign(undecided[0], False, trail, f"vertex {vertex} cannot force a dead-end", record_step):
                        return False
                    changed = True

    
        return True

    def all_clues_satisfied_exactly():
        """Check whether every numbered cell currently matches its clue exactly."""
        for cell_pos, clue in cells.items():
            if clue is None:
                continue
            around = cell_to_edges[cell_pos]
            true_count = sum(1 for edge in around if state[edge] is True)
            if true_count != clue:
                return False
        return True

    def single_loop_check():
        """Verify that True edges form one connected cycle with degree 2 at each vertex."""
        true_edges = [edge for edge, value in state.items() if value is True]
        if not true_edges:
            return False

        adjacency = defaultdict(list)
        for a, b in true_edges:
            adjacency[a].append(b)
            adjacency[b].append(a)

        for vertex, neighbors in adjacency.items():
            if len(neighbors) != 2:
                return False

        start = true_edges[0][0]
        seen = set([start])
        stack = [start]
        while stack:
            current = stack.pop()
            for nxt in adjacency[current]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)

        return len(seen) == len(adjacency)

    def choose_edge():
        """Pick the next undecided edge using a simple pressure/tightness heuristic."""
        undecided = [edge for edge, value in state.items() if value is None]
        if not undecided:
            return None

        def edge_priority(edge):
            clue_strength = 0
            clue_tightness = 0
            for cell in edge_to_cells[edge]:
                clue = cells[cell]
                if clue is not None:
                    clue_strength += 1
                    _, true_count, undecided_count = clue_status(cell)
                    slack = undecided_count
                    if true_count is not None:
                        clue_tightness += max(0, 4 - slack)

            a, b = edge
            va_true, va_und = vertex_status(a)
            vb_true, vb_und = vertex_status(b)
            vertex_pressure = (2 - len(va_und)) + (2 - len(vb_und)) + va_true + vb_true
            return (clue_strength, clue_tightness, vertex_pressure)

        undecided.sort(key=edge_priority, reverse=True)
        return undecided[0]

    def dfs():
        """Depth-first search over edge assignments with propagation at each node."""
        trail = []
        if not propagate(trail, record_step=True):
            undo(trail, record_step=include_backtracking_steps)
            return False

        choice = choose_edge()
        if choice is None:
            if all_clues_satisfied_exactly() and single_loop_check():
                return True
            undo(trail, record_step=include_backtracking_steps)
            return False

        for value in (True, False):
            branch_trail = []
            if assign(choice, value, branch_trail, f"dfs guess {value} on {choice}", record_step=True):
                if dfs():
                    return True
            undo(branch_trail, record_step=include_backtracking_steps)

        undo(trail, record_step=include_backtracking_steps)
        return False

    setup_trail = []
    # Fast initialization: a clue of 0 forces all surrounding edges to False.
    for cell_pos, clue in cells.items():
        if clue == 0:
            for edge in cell_to_edges[cell_pos]:
                if not assign(edge, False, setup_trail, f"cell {cell_pos} has clue 0", record_step=True):
                    return {"solved": False, "steps": steps, "final_state": state}

    if not propagate(setup_trail, record_step=True):
        return {"solved": False, "steps": steps, "final_state": state}

    solved = dfs()
    return {"solved": solved, "steps": steps, "final_state": state.copy()}