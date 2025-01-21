import pygame
import random

# تهيئة pygame
pygame.init()

# الألوان
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# أحجام النوافذ
WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 15

# إنشاء النافذة
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ludo Game")

# خطوط الكتابة
font = pygame.font.SysFont("Arial", 30)

# لوحة اللعب
board = [
    [-1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 0, 2, 2, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 2, 2, 0, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 0, 2, 0, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 0, 2, 0, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 0, 2, 0, -1, -1, -1, -1, -1, -1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 5, 0, 4, 4, 4, 4, 4, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
    [-1, -1, -1, -1, -1, -1, 0, 3, 0, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 0, 3, 0, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 0, 3, 0, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 0, 3, 3, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 3, 3, 0, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1]
]

# مواقع القطع
pieces = {
    "Red": [(1, 1), (1, 4), (4, 1), (4, 4)],
    "Green": [(10, 1), (13, 1), (10, 4), (13, 4)],
    "Blue": [(1, 10), (4, 10), (1, 13), (4, 13)],
    "Yellow": [(10, 10), (10, 13), (13, 10), (13, 13)]
}

# وظيفة لرسم اللوحة
def draw_board():
    for row in range(15):
        for col in range(15):
            color = WHITE
            if board[row][col] == 0:
                color = WHITE
            elif board[row][col] == 1:
                color = RED
            elif board[row][col] == 2:
                color = GREEN
            elif board[row][col] == 3:
                color = YELLOW
            elif board[row][col] == 4:
                color = BLUE
            elif board[row][col] == 5:
                color = BLACK
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# وظيفة لرسم القطع
def draw_pieces():
    for color, positions in pieces.items():
        for pos in positions:
            row, col = pos
            if color == "Red":
                piece_color = RED
            elif color == "Green":
                piece_color = GREEN
            elif color == "Blue":
                piece_color = BLUE
            elif color == "Yellow":
                piece_color = YELLOW
            pygame.draw.circle(screen, piece_color, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

# وظيفة لرسم النرد
def draw_dice(value):
    dice_x, dice_y = WIDTH - 100, HEIGHT - 100
    pygame.draw.rect(screen, WHITE, (dice_x, dice_y, 80, 80))
    pygame.draw.rect(screen, BLACK, (dice_x, dice_y, 80, 80), 2)
    if value == 1:
        pygame.draw.circle(screen, BLACK, (dice_x + 40, dice_y + 40), 5)
    elif value == 2:
        pygame.draw.circle(screen, BLACK, (dice_x + 20, dice_y + 20), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 60, dice_y + 60), 5)
    elif value == 3:
        pygame.draw.circle(screen, BLACK, (dice_x + 20, dice_y + 20), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 40, dice_y + 40), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 60, dice_y + 60), 5)
    elif value == 4:
        pygame.draw.circle(screen, BLACK, (dice_x + 20, dice_y + 20), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 60, dice_y + 20), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 20, dice_y + 60), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 60, dice_y + 60), 5)
    elif value == 5:
        pygame.draw.circle(screen, BLACK, (dice_x + 20, dice_y + 20), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 60, dice_y + 20), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 40, dice_y + 40), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 20, dice_y + 60), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 60, dice_y + 60), 5)
    elif value == 6:
        pygame.draw.circle(screen, BLACK, (dice_x + 20, dice_y + 20), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 60, dice_y + 20), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 20, dice_y + 40), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 60, dice_y + 40), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 20, dice_y + 60), 5)
        pygame.draw.circle(screen, BLACK, (dice_x + 60, dice_y + 60), 5)

# وظيفة لعرض الرسائل
def draw_message(message):
    text = font.render(message, True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))

# الوظيفة الرئيسية
def main():
    clock = pygame.time.Clock()
    dice_value = 1
    running = True

    while running:
        screen.fill(WHITE)
        draw_board()
        draw_pieces()
        draw_dice(dice_value)
        draw_message("Press SPACE to roll the dice")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dice_value = random.randint(1, 6)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()