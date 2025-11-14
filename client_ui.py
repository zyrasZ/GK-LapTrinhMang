import pygame, random
pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Snake UI - Ngày 3: Nhiều rắn")
clock = pygame.time.Clock()
BLOCK = 20; speed = 10

# Giả lập nhiều rắn (thay cho dữ liệu server)
snakes = {
    "player1": [[100,100],[80,100],[60,100]],
    "player2": [[300,300],[320,300],[340,300]],
}
colors = {"player1": (0,255,0), "player2": (0,150,255)}
food = [random.randrange(0,40)*20, random.randrange(0,30)*20]
direction = {"player1":"RIGHT","player2":"LEFT"}

def move_snake(key):
    head = snakes[key][0].copy()
    if direction[key]=="UP": head[1]-=BLOCK
    if direction[key]=="DOWN": head[1]+=BLOCK
    if direction[key]=="LEFT": head[0]-=BLOCK
    if direction[key]=="RIGHT": head[0]+=BLOCK
    snakes[key].insert(0,head); snakes[key].pop()

running=True
while running:
    screen.fill((0,0,0))
    for e in pygame.event.get():
        if e.type==pygame.QUIT: running=False
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_UP: direction["player1"]="UP"
            elif e.key==pygame.K_DOWN: direction["player1"]="DOWN"
            elif e.key==pygame.K_LEFT: direction["player1"]="LEFT"
            elif e.key==pygame.K_RIGHT: direction["player1"]="RIGHT"
    for key in snakes: move_snake(key)
    for key,color in colors.items():
        for x,y in snakes[key]:
            pygame.draw.rect(screen,color,(x,y,BLOCK,BLOCK))
    pygame.draw.rect(screen,(255,50,50),(food[0],food[1],BLOCK,BLOCK))
    pygame.display.flip(); clock.tick(speed)
pygame.quit()
