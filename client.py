import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Snake Multiplayer - UI Test (Day 1)")

clock = pygame.time.Clock()

snake = pygame.Rect(100, 100, 20, 20)

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.rect(screen, (0, 255, 0), snake)

    pygame.display.update()
    clock.tick(10)

pygame.quit()

