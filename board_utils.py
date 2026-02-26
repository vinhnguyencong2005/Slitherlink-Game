import math

from solver_dfs import canonical_edge
from app_config import BOARD_ORIGIN, CELL_SIZE

# Shared board geometry defaults used across UI helper functions.
origin = BOARD_ORIGIN
cell_size = CELL_SIZE

def build_initial_lines(cols, rows, origin=origin, cell_size=cell_size):
    """Create the board edge dictionary in pixel space, initialized to False."""
    lines = {}

    for x in range(cols):
        for y in range(rows + 1):
            start = (origin + x * cell_size, origin + y * cell_size)
            end = (start[0] + cell_size, start[1])
            lines[(start, end)] = False

    for x in range(cols + 1):
        for y in range(rows):
            start = (origin + x * cell_size, origin + y * cell_size)
            end = (start[0], start[1] + cell_size)
            lines[(start, end)] = False

    return lines


def pixel_to_grid_point(point, origin=origin, cell_size=cell_size):
    """Convert a board pixel coordinate to a grid vertex coordinate."""
    x, y = point
    return ((x - origin) // cell_size, (y - origin) // cell_size)


def grid_to_pixel_point(point, origin=origin, cell_size=cell_size):
    """Convert a grid vertex coordinate to its board pixel coordinate."""
    x, y = point
    return (origin + x * cell_size, origin + y * cell_size)


def pixel_edge_to_grid_edge(edge, origin=origin, cell_size=cell_size):
    """Map a pixel-space edge to canonical grid-space edge coordinates."""
    a, b = edge
    return canonical_edge(
        (
            pixel_to_grid_point(a, origin, cell_size),
            pixel_to_grid_point(b, origin, cell_size),
        )
    )


def grid_edge_to_pixel_edge(edge, origin=origin, cell_size=cell_size):
    """Map a grid-space edge to canonical pixel-space edge coordinates."""
    a, b = edge
    return canonical_edge(
        (
            grid_to_pixel_point(a, origin, cell_size),
            grid_to_pixel_point(b, origin, cell_size),
        )
    )


def apply_solver_step(lines, step, origin=origin, cell_size=cell_size):
    """Apply one solver step to the board edge dictionary."""
    edge = grid_edge_to_pixel_edge(step["edge"], origin, cell_size)
    value = step["value"]

    if edge not in lines:
        return

    if value is True:
        lines[edge] = True
    elif value is False:
        lines[edge] = "X"
    else:
        lines[edge] = False


def reset_board(lines):
    """Reset all board edges to False (empty)."""
    for edge in lines.keys():
        lines[edge] = False


def get_clicked_line(lines, click_pos, threshold=10):
    """Return the nearest line segment if click is within threshold distance."""
    cx, cy = click_pos

    for (start, end) in lines.keys():
        x1, y1 = start
        x2, y2 = end

        dx = x2 - x1
        dy = y2 - y1

        t = max(0, min(1, ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)))

        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        distance = math.sqrt((cx - closest_x) ** 2 + (cy - closest_y) ** 2)

        if distance <= threshold:
            return (start, end)

    return None
