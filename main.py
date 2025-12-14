import pygame
import random
#Inputs
a = input("Enter Player 1 : ")
b = input("Enter Player 2 : ")
print("Press q to quit.")
#Maze Creation Functions
def get_index(x, y):
    if x < 0 or x >= columns or y < 0 or y >= rows:
        return -1
    return x + y * columns

def remove_walls(current, next_cell):
    dx = current['x'] - next_cell['x']
    dy = current['y'] - next_cell['y']
    if dx == 1:
        current['walls']['left'] = False
        next_cell['walls']['right'] = False
    elif dx == -1:
        current['walls']['right'] = False
        next_cell['walls']['left'] = False

    if dy == 1:
        current['walls']['top'] = False
        next_cell['walls']['bottom'] = False
    elif dy == -1:
        current['walls']['bottom'] = False
        next_cell['walls']['top'] = False

def create_maze():
    grid = []
    for y in range(rows):
        for x in range(columns):
            grid.append({
                'x': x, 'y': y,
                'walls': {'top': True, 'right': True, 'bottom': True, 'left': True},
                'visited': False
            })

    stack = []
    current = grid[0]
    current['visited'] = True
    while True:
        neighbors = []
        x, y = current['x'], current['y']
        index = [get_index(x, y - 1), get_index(x + 1, y), get_index(x, y + 1), get_index(x - 1, y)]

        for i in index:
            if i != -1 and not grid[i]['visited']:
                neighbors.append(grid[i])

        if neighbors:
            next_cell = random.choice(neighbors)
            remove_walls(current, next_cell)
            next_cell['visited'] = True
            stack.append(current)
            current = next_cell
        elif stack:
            current = stack.pop()
        else:
            break
    return grid
#Constants
WIDTH, HEIGHT = 500, 500
TILE = 40
columns, rows = WIDTH // TILE, HEIGHT // TILE
SCREEN_WIDTH = WIDTH * 2 + 20
SCREEN_HEIGHT = HEIGHT + 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30, bold=True)
large_font = pygame.font.SysFont("Arial", 60, bold=True)

def draw_maze(grid, offset_x):
    for cell in grid:
        x = cell['x'] * TILE + offset_x
        y = cell['y'] * TILE + 60  # +60 pushes it down below the score text

        walls = cell['walls']
        if walls['top']:    pygame.draw.line(screen, WHITE, (x, y), (x + TILE, y), 2)
        if walls['right']:  pygame.draw.line(screen, WHITE, (x + TILE, y), (x + TILE, y + TILE), 2)
        if walls['bottom']: pygame.draw.line(screen, WHITE, (x + TILE, y + TILE), (x, y + TILE), 2)
        if walls['left']:   pygame.draw.line(screen, WHITE, (x, y + TILE), (x, y), 2)

grid1 = create_maze()
grid2 = create_maze()
p1_x, p1_y = 0, 0
p2_x, p2_y = 0, 0
score1 = 0
score2 = 0
start_time = pygame.time.get_ticks()
running = True
#Game Running
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for key_input in pygame.event.get():
        if key_input.type == pygame.QUIT:
            running = False

        if key_input.type == pygame.KEYDOWN:

            idx1 = get_index(p1_x, p1_y)
            walls1 = grid1[idx1]['walls']
            if key_input.key == pygame.K_q:
                running = False

            if key_input.key == pygame.K_a and not walls1['left']:
                p1_x -= 1
            if key_input.key == pygame.K_d and not walls1['right']:
                p1_x += 1
            if key_input.key == pygame.K_w and not walls1['top']:
                p1_y -= 1
            if key_input.key == pygame.K_s and not walls1['bottom']:
                p1_y += 1

            idx2 = get_index(p2_x, p2_y)
            walls2 = grid2[idx2]['walls']

            if key_input.key == pygame.K_LEFT and not walls2['left']:
                p2_x -= 1
            if key_input.key == pygame.K_RIGHT and not walls2['right']:
                p2_x += 1
            if key_input.key == pygame.K_UP and not walls2['top']:
                p2_y -= 1
            if key_input.key == pygame.K_DOWN and not walls2['bottom']:
                p2_y += 1

    winner = None
    if p1_x == columns - 1 and p1_y == rows - 1:
        winner = a
    if p2_x == columns - 1 and p2_y == rows - 1:
        winner = b

    if winner:
        if winner == a:
            score1 += 1
        if winner == b:
            score2 += 1
        #Winner Display
        win_msg = f"{winner} Wins!"
        text = large_font.render(win_msg, True, GREEN if winner == a else CYAN)

        l = 510 - text.get_width() // 2
        m = 280 - text.get_height() // 2

        pygame.draw.rect(screen, BLACK, (l - 10, m - 10, text.get_width() + 20, text.get_height() + 20))
        screen.blit(text, (l, m))

        pygame.display.flip()
        pygame.time.delay(2000)

        grid1 = create_maze()
        grid2 = create_maze()
        p1_x, p1_y = 0, 0
        p2_x, p2_y = 0, 0
        start_time = pygame.time.get_ticks()

    draw_maze(grid1, 10)
    draw_maze(grid2, WIDTH + 20)
    timer = (pygame.time.get_ticks() - start_time) // 1000

    pygame.draw.rect(screen, GREEN, (p1_x * TILE + 15, p1_y * TILE + 65, TILE - 10, TILE - 10))
    pygame.draw.rect(screen, CYAN, (p2_x * TILE + WIDTH + 25, p2_y * TILE + 65, TILE - 10, TILE - 10))
    pygame.draw.rect(screen, RED, ((columns - 1) * TILE + 15, (rows - 1) * TILE + 65, TILE - 10, TILE - 10))
    pygame.draw.rect(screen, RED, ((columns - 1) * TILE + WIDTH + 25, (rows - 1) * TILE + 65, TILE - 10, TILE - 10))

    text_p1 = font.render(f"{a}: {score1}", True, GREEN)
    text_time = font.render(f"Time: {timer} s", True, WHITE)
    text_p2 = font.render(f"{b}: {score2}", True, CYAN)

    screen.blit(text_p1, (50, 10))
    screen.blit(text_time, (SCREEN_WIDTH // 2 - 50, 10))
    screen.blit(text_p2, (SCREEN_WIDTH - 150, 10))

    pygame.display.flip()
pygame.quit()
#End
if score1>score2:
    c = a
    d = score1-score2
    print(f"The winner is {c} by {d} points.")
elif score2>score1:
    c = b
    d = score2-score1
    print(f"The winner is {c} by {d} points.")
else:
    print("It is a draw.")

print("Thank you for playing.")