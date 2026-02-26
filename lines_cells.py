from app_config import BOARD_ORIGIN, CELL_SIZE


def get_cell_lines(cell_pos):
    """Returns the 4 lines surrounding a cell as (top, right, bottom, left)"""
    i, j = cell_pos
    base_x = BOARD_ORIGIN + j * CELL_SIZE
    base_y = BOARD_ORIGIN + i * CELL_SIZE
    
    top = ((base_x, base_y), (base_x + CELL_SIZE, base_y))
    right = ((base_x + CELL_SIZE, base_y), (base_x + CELL_SIZE, base_y + CELL_SIZE))
    bottom = ((base_x, base_y + CELL_SIZE), (base_x + CELL_SIZE, base_y + CELL_SIZE))
    left = ((base_x, base_y), (base_x, base_y + CELL_SIZE))
    
    return top, right, bottom, left


# Use to set up the cells dictionary from a matrix of clue numbers
# Example usage:
# matrix = [
#     [1, 0, 2],
#     [0, 3, 0],
#     [2, 0, 1]
# ]
def initialize_cells(matrix):
    buffer = {}
    for j, row in enumerate(matrix):
        for i, value in enumerate(row):
            buffer[(i, j)] = value
    return buffer