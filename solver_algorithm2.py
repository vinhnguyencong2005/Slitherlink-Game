from collections import defaultdict


def solve_with_algorithm_2(cells, include_backtracking_steps=True):
    """
    Algorithm 2:
    DFS + Propagation như cũ,
    nhưng branch ordering dựa trên heuristic scoring.
    """

    # ===== BUILD MODEL  =====

    def canonical_edge(edge):
        a, b = edge
        return (a, b) if a <= b else (b, a)

    def build_model(cells):
        max_col = max(pos[0] for pos in cells.keys())
        max_row = max(pos[1] for pos in cells.keys())
        cols = max_col + 1
        rows = max_row + 1

        edges = []
        for y in range(rows + 1):
            for x in range(cols):
                edges.append(canonical_edge(((x, y), (x + 1, y))))
        for x in range(cols + 1):
            for y in range(rows):
                edges.append(canonical_edge(((x, y), (x, y + 1))))

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


    edges, cell_to_edges, edge_to_cells, vertex_to_edges = build_model(cells)
    state = {edge: None for edge in edges}
    steps = []


    # ===== ASSIGN / UNDO  =====

    def assign(edge, value, trail, reason, record_step=True):
        current = state[edge]
        if current is not None:
            return current == value
        state[edge] = value
        trail.append(edge)
        if record_step:
            steps.append({"edge": edge, "value": value, "reason": reason})
        return True

    def undo(trail, record_step=True):
        while trail:
            edge = trail.pop()
            state[edge] = None
            if record_step:
                steps.append({"edge": edge, "value": None, "reason": "backtrack"})


    # ===== STATUS FUNCTIONS =====

    def clue_status(cell_pos):
        clue = cells[cell_pos]
        if clue is None:
            return None, None, None
        around = cell_to_edges[cell_pos]
        true_count = sum(1 for edge in around if state[edge] is True)
        undecided_count = sum(1 for edge in around if state[edge] is None)
        return clue, true_count, undecided_count

    def vertex_status(vertex):
        incident = vertex_to_edges[vertex]
        true_count = sum(1 for edge in incident if state[edge] is True)
        undecided = [edge for edge in incident if state[edge] is None]
        return true_count, undecided


    # ===== PROPAGATE =====

    def propagate(trail, record_step=True):
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


    # ===== HEURISTIC SCORE (điểm cho branch ordering) =====

    def evaluate_state():
        score = 0

        # cell heuristic
        for cell_pos in cells:
            clue, true_count, undecided_count = clue_status(cell_pos)
            if clue is None:
                continue
            slack = clue - true_count
            if slack == 0:
                score += 3
            score -= abs(slack)
            # ưu tiên cell gần hoàn tất
            score -= undecided_count * 0.2

        # vertex heuristic
        for vertex in vertex_to_edges:
            true_count, undecided = vertex_status(vertex)
            if true_count == 1:
                score -= 2
            if true_count == 2:
                score += 1

        return score

    def has_small_loop():
        true_edges = [e for e,v in state.items() if v is True]

        visited = set()

        adjacency = defaultdict(list)
        for a,b in true_edges:
            adjacency[a].append(b)
            adjacency[b].append(a)

        for start in adjacency:
            if start in visited:
                continue

            stack = [start]
            component = set([start])
            visited.add(start)

            while stack:
                cur = stack.pop()
                for nxt in adjacency[cur]:
                    if nxt not in visited:
                        visited.add(nxt)
                        component.add(nxt)
                        stack.append(nxt)

            # check if component is closed loop
            is_loop = True
            for v in component:
                if len(adjacency[v]) != 2:
                    is_loop = False
                    break

            if is_loop:
                undecided_exist = any(v is None for v in state.values())
                if undecided_exist:
                    return True

        return False

    # ===== SINGLE LOOP CHECK =====

    def single_loop_check():
        true_edges = [edge for edge, v in state.items() if v is True]
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
            cur = stack.pop()
            for nxt in adjacency[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)

        return len(seen) == len(adjacency)


    # ===== CHOOSE EDGE  =====

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



    # ===== MODIFIED DFS =====

    def dfs():
        trail = []
        if not propagate(trail, record_step=True):
            undo(trail, record_step=include_backtracking_steps)
            return False

        if has_small_loop():
            undo(trail, record_step=include_backtracking_steps)
            return False

        choice = choose_edge()
        if choice is None:
            if all_clues_satisfied_exactly() and single_loop_check():
                return True
            undo(trail, record_step=include_backtracking_steps)
            return False

        # tính điểm cho True/False
        scored_branches = []

        for value in (True, False):
            branch_trail = []
            if assign(choice, value, branch_trail, f"guess {value}", record_step=True):
                if propagate(branch_trail, record_step=False):
                    score = evaluate_state()
                    scored_branches.append((score, value, branch_trail))
            undo(branch_trail, record_step=False)

        # thử nhánh có điểm cao trước
        scored_branches.sort(reverse=True)

        for _, value, _ in scored_branches:
            branch_trail = []
            if assign(choice, value, branch_trail, f"heuristic {value}", record_step=True):
                if dfs():
                    return True
            undo(branch_trail, record_step=include_backtracking_steps)

        undo(trail, record_step=include_backtracking_steps)
        return False


    solved = dfs()

    return {
        "solved": solved,
        "steps": steps,
        "final_state": state.copy()
    }