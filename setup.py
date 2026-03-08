import pygame
from lines_cells import *
from puzzles_example import *
from algorithm_runner import run_solver, ALGORITHM_LABELS
from app_config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    GRID_COLS,
    GRID_ROWS,
    CELL_SIZE,
    AUTOPLAY_EVERY_N_FRAMES,
)
from board_utils import (
    build_initial_lines,
    pixel_to_grid_point,
    grid_to_pixel_point,
    pixel_edge_to_grid_edge,
    grid_edge_to_pixel_edge,
    apply_solver_step,
    reset_board,
    get_clicked_line,
)

import time
import tracemalloc



lines = {} # Store line states: key = (start, end), value = False (empty), True (drawn), 'X' (marked invalid)
cells = {} # Store cells: key = (col, row), value = number (0-3) or None
# Initialize grid of cells
for i in range(GRID_COLS):  # columns
    for j in range(GRID_ROWS):  # rows
        cells[(i, j)] = None  # or assign actual puzzle numbers


cells = initialize_cells(example_clues_1)

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Slitherlink")
clock = pygame.time.Clock()
cell_font = pygame.font.SysFont(None, 56)
ui_font = pygame.font.SysFont(None, 28)
lines = build_initial_lines(cols=GRID_COLS, rows=GRID_ROWS)


solver_steps = []
solver_step_index = 0
solver_autoplay = False
autoplay_frame_counter = 0
game_state = "menu"
selected_algorithm = None

menu_title_font = pygame.font.SysFont(None, 64)
menu_option_font = pygame.font.SysFont(None, 40)

algo_1_rect = pygame.Rect(220, 280, 360, 70)
algo_2_rect = pygame.Rect(220, 380, 360, 70)

running = True
while running:
    SCREEN.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if algo_1_rect.collidepoint(event.pos):
                    selected_algorithm = 1
                    game_state = "game"
                    reset_board(lines)
                    solver_steps = []
                    solver_step_index = 0
                    solver_autoplay = False
                elif algo_2_rect.collidepoint(event.pos):
                    selected_algorithm = 2
                    game_state = "game"
                    reset_board(lines)
                    solver_steps = []
                    solver_step_index = 0
                    solver_autoplay = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_algorithm = 1
                    game_state = "game"
                    reset_board(lines)
                    solver_steps = []
                    solver_step_index = 0
                    solver_autoplay = False
                elif event.key == pygame.K_2:
                    selected_algorithm = 2
                    game_state = "game"
                    reset_board(lines)
                    solver_steps = []
                    solver_step_index = 0
                    solver_autoplay = False

        elif game_state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    clicked_line = get_clicked_line(lines, event.pos)
                    if clicked_line:
                        grid_point = pixel_to_grid_point(event.pos)
                        grid_edge = pixel_edge_to_grid_edge(clicked_line)
                        # Toggle: False ↔ True
                        if lines[clicked_line] == False:
                            lines[clicked_line] = True
                        elif lines[clicked_line] == True:
                            lines[clicked_line] = False
                        else:  # 'X' state
                            lines[clicked_line] = True
                        print(f"Left click: {lines[clicked_line]} edge={grid_edge} near_vertex={grid_point}")
                elif event.button == 3:  # Right click
                    clicked_line = get_clicked_line(lines, event.pos)
                    if clicked_line:
                        grid_point = pixel_to_grid_point(event.pos)
                        grid_edge = pixel_edge_to_grid_edge(clicked_line)
                        # Toggle: False ↔ 'X'
                        if lines[clicked_line] == 'X':
                            lines[clicked_line] = False
                        else:
                            lines[clicked_line] = 'X'
                        print(f"Right click: {lines[clicked_line]} edge={grid_edge} near_vertex={grid_point}")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    tracemalloc.start()
                    start_time = time.perf_counter()

                    result = run_solver(selected_algorithm, cells)

                    end_time = time.perf_counter()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()

                    runtime = end_time - start_time
                    memory = peak / 1024 / 1024  # MB
                    solver_steps = result.get("steps", [])
                    solver_step_index = 0
                    solver_autoplay = False
                    reset_board(lines)
                    label = ALGORITHM_LABELS.get(selected_algorithm, f"Algorithm {selected_algorithm}")
                    print(
                        f"{label:<10} | "
                        f"solved={str(result.get('solved', False)):<5} | "
                        f"steps={len(solver_steps):>5} | "
                        f"time={runtime:>10.6f}s | "
                        f"memory={memory:>7.2f} MB"
                    )
                    if "message" in result:
                        print(result["message"])

                elif event.key == pygame.K_n:
                    if solver_step_index < len(solver_steps):
                        pixel_edge = grid_edge_to_pixel_edge(solver_steps[solver_step_index]["edge"])
                        apply_solver_step(lines, solver_steps[solver_step_index])
                        print(solver_steps[solver_step_index]["reason"])
                        print(f"Applied edge in pixels: {pixel_edge}")
                        solver_step_index += 1

                elif event.key == pygame.K_a:
                    solver_autoplay = not solver_autoplay
                    print(f"Autoplay: {solver_autoplay}")

                elif event.key == pygame.K_r:
                    solver_autoplay = False
                    solver_step_index = 0
                    reset_board(lines)

                elif event.key == pygame.K_m:
                    game_state = "menu"
                    solver_autoplay = False

    if game_state == "game" and solver_autoplay and solver_step_index < len(solver_steps):
        autoplay_frame_counter += 1
        if autoplay_frame_counter >= AUTOPLAY_EVERY_N_FRAMES:
            apply_solver_step(lines, solver_steps[solver_step_index])
            solver_step_index += 1
            autoplay_frame_counter = 0

    if game_state == "menu":
        title_surface = menu_title_font.render("Choose Solver Algorithm", True, (30, 30, 30))
        title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 180))
        SCREEN.blit(title_surface, title_rect)

        pygame.draw.rect(SCREEN, (230, 230, 230), algo_1_rect, border_radius=8)
        pygame.draw.rect(SCREEN, (230, 230, 230), algo_2_rect, border_radius=8)

        algo1_text = menu_option_font.render(ALGORITHM_LABELS[1], True, (20, 20, 20))
        algo2_text = menu_option_font.render(ALGORITHM_LABELS[2], True, (20, 20, 20))
        SCREEN.blit(algo1_text, algo1_text.get_rect(center=algo_1_rect.center))
        SCREEN.blit(algo2_text, algo2_text.get_rect(center=algo_2_rect.center))
    else:
        # Draw lines based on their state
        for (start, end), state in lines.items():
            if state == True:  # Draw line
                pygame.draw.line(SCREEN, (0, 0, 0), start, end, 5)
            elif state == 'X':  # Draw X mark
                # Calculate midpoint of line
                mid_x = (start[0] + end[0]) // 2
                mid_y = (start[1] + end[1]) // 2
                size = 8
                # Draw X with red color
                pygame.draw.line(SCREEN, (255, 0, 0),
                                (mid_x - size, mid_y - size),
                                (mid_x + size, mid_y + size), 3)
                pygame.draw.line(SCREEN, (255, 0, 0),
                                (mid_x + size, mid_y - size),
                                (mid_x - size, mid_y + size), 3)

        # Draw dots (after lines, so they're on top)
        for i in range(GRID_COLS + 1):
            for j in range(GRID_ROWS + 1):
                center = grid_to_pixel_point((i, j))
                pygame.draw.circle(SCREEN, (0, 0, 0), center, 9)

        # Draw clue numbers centered in each cell
        for (i, j), value in cells.items():
            if value is None:
                continue
            text_surface = cell_font.render(str(value), True, (30, 30, 30))
            top_left = grid_to_pixel_point((i, j))
            text_rect = text_surface.get_rect(center=(top_left[0] + CELL_SIZE // 2, top_left[1] + CELL_SIZE // 2))
            SCREEN.blit(text_surface, text_rect)

        controls_text = "S: solve   N: next step   A: autoplay   R: reset   M: menu"
        controls_surface = ui_font.render(controls_text, True, (40, 40, 40))
        SCREEN.blit(controls_surface, (20, 20))

        algo_text = f"Algorithm: {ALGORITHM_LABELS.get(selected_algorithm, 'None')}"
        algo_surface = ui_font.render(algo_text, True, (40, 40, 40))
        SCREEN.blit(algo_surface, (20, 50))

        status_text = f"Step: {solver_step_index}/{len(solver_steps)}   Autoplay: {solver_autoplay}"
        status_surface = ui_font.render(status_text, True, (40, 40, 40))
        SCREEN.blit(status_surface, (20, 80))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
