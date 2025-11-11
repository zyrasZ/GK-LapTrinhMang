import pygame

# Khởi tạo pygame
pygame.init()

# Tạo màn hình 800x600
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Multiplayer - UI Test (Day 1)")

clock = pygame.time.Clock()

# Tạo 1 ô vuông đại diện cho thân rắn
snake_block = pygame.Rect(100, 100, 20, 20)

running = True
while running:
    screen.fill((0, 0, 0))  # nền đen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Vẽ 1 ô vuông màu xanh lá
    pygame.draw.rect(screen, (0, 255, 0), snake_block)

    pygame.display.update()
    clock.tick(10)  # FPS = 10

pygame.quit()
