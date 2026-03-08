from lines_cells import *

# Example puzzle clues (None means blank cell)
example_clues_1 = [
    [2, None, None, 2, None],
    [2, None, 1, None, None],
    [2, None, 2, None, 2],
    [None, 2, 0, 2, 1],
    [None, 3, 3, 3, None],
]
'''
example_clues_1 = [
    [None, 3, None, 2, 0],
    [None, None, 2, None, 2],
    [3, 2, 2, None, 3],
    [2, None, None, None, 3],
    [None, None, None, None, None],
]
example_clues_1 = [
    [ 3, 2, 2, 1, None],
    [2, 2, None, 2, 3],
    [3, 2, 2, 0, 3],
    [2, None, None, None, None],
    [None, None, None, 1, None],
]
'''
solution_1 = {
    get_cell_lines((0,0))[0]: True,  # top line of cell (0,0)
    get_cell_lines((0,0))[3]: True,  # left line of cell (0,0)
    get_cell_lines((0,1))[0]: True,  # top line of cell (0,1)
    get_cell_lines((0,2))[0]: True,  # right line of cell (0,2)
    get_cell_lines((0,2))[1]: True,  # top line of cell (0,2)
    get_cell_lines((0,3))[1]: True,  # right line of cell (0,3)
    get_cell_lines((0,4))[0]: True,  # top line of cell (0,4)
    get_cell_lines((0,4))[1]: True,  # right line of cell (0,4)
    get_cell_lines((1,0))[3]: True,  # left line of cell (1,0)
    get_cell_lines((1,0))[2]: True,  # bottom line of cell (1,0)
    get_cell_lines((1,1))[2]: True,  # bottom line of cell (1,1)
    get_cell_lines((1,2))[1]: True,  # right line of cell (1,2)
    get_cell_lines((1,3))[1]: True,  # right line of cell (1,3)
    get_cell_lines((1,4))[1]: True,  # right line of cell (1,4)
    get_cell_lines((2,0))[2]: True,  # bottom line of cell (2,0)
    get_cell_lines((2,1))[1]: True,  # right line of cell (2,1)
    get_cell_lines((2,1))[2]: True,  # bottom line of cell (2,1)
    get_cell_lines((2,2))[1]: True,  # right line of cell (2,2)
    get_cell_lines((2,3))[1]: True,  # right line of cell (2,3)
    get_cell_lines((2,3))[2]: True,  # bottom line of cell (2,3)
    get_cell_lines((2,4))[1]: True,  # right line of cell (2,4)
    get_cell_lines((3,0))[3]: True,  # left line of cell (3,0)
    get_cell_lines((3,1))[2]: True,  # bottom line of cell (3,1)
    get_cell_lines((3,3))[2]: True,  # bottom line of cell (3,3)
    get_cell_lines((3,4))[1]: True,  # right line of cell (3,4)
    get_cell_lines((4,0))[2]: True,  # bottom line of cell (4,0)
    get_cell_lines((4,0))[3]: True,  # left line of cell (4,0)
    get_cell_lines((4,0))[1]: True,  # right line of cell (4,0)
    get_cell_lines((4,1))[1]: True,  # right line of cell (4,1)
    get_cell_lines((4,2))[1]: True,  # right line of cell (4,2)
    get_cell_lines((4,2))[2]: True,  # bottom line of cell (4,2)
    get_cell_lines((4,3))[1]: True,  # right line of cell (4,3)
    get_cell_lines((4,4))[2]: True,  # bottom line of cell (4,4)
    get_cell_lines((4,4))[1]: True,  # right line of cell (4,4)
}