import pygame
import math
from lines_cells import *
from puzzles_example import *
WIDTH, HEIGHT = 800, 800
FPS = 60


lines = {} # Store line states: key = (start, end), value = False (empty), True (drawn), 'X' (marked invalid)
cells = {} # Store cells: key = (col, row), value = number (0-3) or None
# Initialize 5x5 grid of cells
for i in range(5):  # columns
    for j in range(5):  # rows
        cells[(i, j)] = None  # or assign actual puzzle numbers


cells = initialize_cells(example_clues_1)

def main():
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Slitherlink")
    clock = pygame.time.Clock()
    cell_font = pygame.font.SysFont(None, 56)
    lines.clear()

    # Horizontal lines
    for i in range(5):
        for j in range(6):
            start = (150 + i * 100, 150 + j * 100)
            end = (start[0] + 100, start[1])
            lines[(start, end)] = False  # Start empty
    
    # Vertical lines
    for i in range(6):
        for j in range(5):
            start = (150 + i * 100, 150 + j * 100)
            end = (start[0], start[1] + 100)
            lines[(start, end)] = False  # Start empty

    # Load a prebuilt solution to visualize it on the board
    for line, state in solution_1.items():
        if line in lines:
            lines[line] = state
    
    def get_clicked_line(click_pos, threshold=10):
        """Find which line was clicked (within threshold pixels)"""
        cx, cy = click_pos
        
        for (start, end) in lines.keys():
            x1, y1 = start
            x2, y2 = end
            
            dx = x2 - x1
            dy = y2 - y1
            
            t = max(0, min(1, ((cx - x1) * dx + (cy - y1) * dy) / (dx*dx + dy*dy)))
            
            closest_x = x1 + t * dx
            closest_y = y1 + t * dy
            
            distance = math.sqrt((cx - closest_x)**2 + (cy - closest_y)**2)
            
            if distance <= threshold:
                return (start, end)
        
        return None
    
    running = True
    while running:
        SCREEN.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    clicked_line = get_clicked_line(event.pos)
                    if clicked_line:
                        # Toggle: False ↔ True
                        if lines[clicked_line] == False:
                            lines[clicked_line] = True
                        elif lines[clicked_line] == True:
                            lines[clicked_line] = False
                        else:  # 'X' state
                            lines[clicked_line] = True
                        print(f"Left click: {lines[clicked_line]}")
                elif event.button == 3:  # Right click
                    clicked_line = get_clicked_line(event.pos)
                    if clicked_line:
                        # Toggle: False ↔ 'X'
                        if lines[clicked_line] == 'X':
                            lines[clicked_line] = False
                        else:
                            lines[clicked_line] = 'X'
                        print(f"Right click: {lines[clicked_line]}")
        
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
        for i in range(6):
            for j in range(6):
                center_x = 150 + i * 100
                center_y = 150 + j * 100
                pygame.draw.circle(SCREEN, (0, 0, 0), (center_x, center_y), 9)

        # Draw clue numbers centered in each cell
        for (i, j), value in cells.items():
            if value is None:
                continue
            text_surface = cell_font.render(str(value), True, (30, 30, 30))
            text_rect = text_surface.get_rect(center=(150 + i * 100 + 50, 150 + j * 100 + 50))
            SCREEN.blit(text_surface, text_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()