def get_cell_lines(cell_pos):
    """Returns the 4 lines surrounding a cell as (top, right, bottom, left)"""
    i, j = cell_pos
    base_x = 150 + j * 100
    base_y = 150 + i * 100
    
    top = ((base_x, base_y), (base_x + 100, base_y))
    right = ((base_x + 100, base_y), (base_x + 100, base_y + 100))
    bottom = ((base_x, base_y + 100), (base_x + 100, base_y + 100))
    left = ((base_x, base_y), (base_x, base_y + 100))
    
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