import pygame
import random

# ===== Khởi tạo Pygame =====
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake UI - Ngày 2: Di chuyển & ăn mồi")
clock = pygame.time.Clock()

# ===== Thông số cơ bản =====
BLOCK = 20               # kích thước mỗi ô
direction = "RIGHT"      # hướng ban đầu
speed = 10               # FPS

# ===== Tạo rắn và mồi =====
snake = [
    [100, 100],
    [80, 100],
    [60, 100]
]
food = [random.randrange(0, 40) * 20, random.randrange(0, 30) * 20]
score = 0

# ===== Hàm di chuyển rắn =====
def move_snake():
    head = snake[0].copy()

    if direction == "UP": head[1] -= BLOCK
    if direction == "DOWN": head[1] += BLOCK
    if direction == "LEFT": head[0] -= BLOCK
    if direction == "RIGHT": head[0] += BLOCK

    snake.insert(0, head)
    snake.pop()

# ===== Hàm vẽ rắn, mồi, điểm =====
def draw_snake():
    for x, y in snake:
        pygame.draw.rect(screen, (0, 255, 0), (x, y, BLOCK, BLOCK))

def draw_food():
    pygame.draw.rect(screen, (255, 50, 50), (food[0], food[1], BLOCK, BLOCK))

def draw_score():
    font = pygame.font.SysFont("Arial", 24)
    text = font.render(f"Điểm: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

# ===== Vòng lặp chính =====
running = True
while running:
    screen.fill((0, 0, 0))

    # --- Xử lý sự kiện phím ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # --- Di chuyển rắn ---
    move_snake()

    # --- Ăn mồi ---
    if snake[0] == food:
        snake.append(snake[-1].copy())
        food = [random.randrange(0, 40) * 20, random.randrange(0, 30) * 20]
        score += 1

    # --- Kiểm tra va chạm tường (reset đơn giản) ---
    x, y = snake[0]
    if x < 0 or x >= 800 or y < 0 or y >= 600:
        snake = [[100, 100], [80, 100], [60, 100]]
        direction = "RIGHT"
        score = 0

    # --- Vẽ ---
    draw_snake()
    draw_food()
    draw_score()

    pygame.display.update()
    clock.tick(speed)

pygame.quit()
