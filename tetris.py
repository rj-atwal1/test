import pygame
import random

# Initialize pygame
pygame.init()


# Screen and play area dimensions

# Wider play area: 20 columns
BLOCK_SIZE = 30
MARGIN = 20
PLAY_WIDTH = BLOCK_SIZE * 20  # 20 columns
PLAY_HEIGHT = BLOCK_SIZE * 20  # Keep height at 20 rows
SCREEN_WIDTH = PLAY_WIDTH + 200  # Extra space for score/side panel
SCREEN_HEIGHT = PLAY_HEIGHT + 2*MARGIN


# Define primary colors (RGB)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (30, 30, 40)  # Modern dark background
GRID_COLOR = (60, 60, 80)  # Subtle grid lines
SHADOW_COLOR = (0, 0, 0, 80)  # For block shadow

# List of primary colors for tetrominoes
COLORS = [RED, BLUE, YELLOW]

# Define the shapes of the tetrominoes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
]

# Tetromino class
def rotate(shape):
    return [ [ shape[y][x] for y in range(len(shape)) ] for x in range(len(shape[0]) - 1, -1, -1) ]

class Tetromino:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.rotation = 0

    def image(self):
        img = self.shape
        for _ in range(self.rotation % 4):
            img = rotate(img)
        return img

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

# Game grid

class Tetris:
    def __init__(self, width, height):
        self.width = width // BLOCK_SIZE
        self.height = height // BLOCK_SIZE
        self.grid = [[BLACK for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0
        self.game_over = False
        self.new_tetromino()

    def new_tetromino(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        self.tetromino = Tetromino(self.width // 2 - len(shape[0]) // 2, 0, shape, color)
        if self.collision(self.tetromino):
            self.game_over = True

    def collision(self, tetromino):
        img = tetromino.image()
        for y, row in enumerate(img):
            for x, cell in enumerate(row):
                if cell:
                    px = tetromino.x + x
                    py = tetromino.y + y
                    if px < 0 or px >= self.width or py >= self.height:
                        return True
                    if py >= 0 and self.grid[py][px] != BLACK:
                        return True
        return False

    def freeze(self):
        img = self.tetromino.image()
        for y, row in enumerate(img):
            for x, cell in enumerate(row):
                if cell:
                    px = self.tetromino.x + x
                    py = self.tetromino.y + y
                    if py >= 0:
                        self.grid[py][px] = self.tetromino.color
        self.clear_lines()
        self.new_tetromino()

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        lines_cleared = self.height - len(new_grid)
        for _ in range(lines_cleared):
            new_grid.insert(0, [BLACK for _ in range(self.width)])
        self.grid = new_grid
        self.score += lines_cleared

    def move(self, dx, dy):
        self.tetromino.x += dx
        self.tetromino.y += dy
        if self.collision(self.tetromino):
            self.tetromino.x -= dx
            self.tetromino.y -= dy
            if dy:
                self.freeze()

    def rotate(self):
        self.tetromino.rotate()
        if self.collision(self.tetromino):
            for _ in range(3):
                self.tetromino.rotate()

    def drop(self):
        while not self.collision(self.tetromino):
            self.tetromino.y += 1
        self.tetromino.y -= 1
        self.freeze()

# Draw functions

# Draw a rounded rectangle with optional shadow
def draw_block(screen, color, x, y, r=6, shadow=True):
    rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
    if shadow:
        shadow_rect = rect.move(3, 3)
        s = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(s, (0,0,0,60), s.get_rect(), border_radius=r)
        screen.blit(s, shadow_rect)
    pygame.draw.rect(screen, color, rect, border_radius=r)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=r)

def draw_grid(screen, tetris):
    # Draw play area background
    pygame.draw.rect(screen, BG_COLOR, (MARGIN, MARGIN, PLAY_WIDTH, PLAY_HEIGHT), border_radius=10)
    # Draw grid lines
    for y in range(tetris.height):
        for x in range(tetris.width):
            cell_color = tetris.grid[y][x]
            px = MARGIN + x*BLOCK_SIZE
            py = MARGIN + y*BLOCK_SIZE
            if cell_color != BLACK:
                draw_block(screen, cell_color, px, py)
            else:
                pygame.draw.rect(screen, GRID_COLOR, (px, py, BLOCK_SIZE, BLOCK_SIZE), 1, border_radius=4)


def draw_tetromino(screen, tetromino):
    img = tetromino.image()
    for y, row in enumerate(img):
        for x, cell in enumerate(row):
            if cell:
                px = MARGIN + (tetromino.x + x)*BLOCK_SIZE
                py = MARGIN + (tetromino.y + y)*BLOCK_SIZE
                draw_block(screen, tetromino.color, px, py)



def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris - Primary Colors')
    clock = pygame.time.Clock()
    tetris = Tetris(PLAY_WIDTH, PLAY_HEIGHT)
    fall_time = 0
    fall_speed = 0.5

    running = True
    while running:
        screen.fill(BG_COLOR)
        fall_time += clock.get_rawtime() / 1000
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    tetris.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    tetris.move(0, 1)
                elif event.key == pygame.K_UP:
                    tetris.rotate()
                elif event.key == pygame.K_SPACE:
                    tetris.drop()

        if fall_time > fall_speed:
            tetris.move(0, 1)
            fall_time = 0

        draw_grid(screen, tetris)
        draw_tetromino(screen, tetris.tetromino)

        # Display score in a modern box to the right
        font = pygame.font.SysFont('Arial', 28, bold=True)
        score_box = pygame.Rect(PLAY_WIDTH + MARGIN*2, MARGIN, SCREEN_WIDTH - PLAY_WIDTH - 3*MARGIN, 80)
        pygame.draw.rect(screen, (40, 40, 60), score_box, border_radius=10)
        pygame.draw.rect(screen, WHITE, score_box, 2, border_radius=10)
        score_text = font.render(f'Score', True, WHITE)
        value_text = font.render(f'{tetris.score}', True, YELLOW)
        screen.blit(score_text, (score_box.x + 18, score_box.y + 8))
        screen.blit(value_text, (score_box.x + 18, score_box.y + 40))

        if tetris.game_over:
            over_font = pygame.font.SysFont('Arial', 48, bold=True)
            over_text = over_font.render('Game Over', True, RED)
            # Centered overlay
            overlay = pygame.Surface((PLAY_WIDTH, 100), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            overlay.blit(over_text, (PLAY_WIDTH//2 - over_text.get_width()//2, 25))
            screen.blit(overlay, (MARGIN, SCREEN_HEIGHT//2 - 50))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
