import pygame,random
pygame.init()
screen=pygame.display.set_mode((800,600))
pygame.display.set_caption("Snake UI - Ngày 4: Hiệu ứng chết & reset")
clock=pygame.time.Clock(); BLOCK=20; speed=10

snake=[[100,100],[80,100],[60,100]]
direction="RIGHT"; food=[random.randrange(0,40)*20,random.randrange(0,30)*20]
score=0; dead=False; font=pygame.font.SysFont("Arial",36)

def reset():
    return [[100,100],[80,100],[60,100]],"RIGHT",0

running=True
while running:
    screen.fill((0,0,0))
    for e in pygame.event.get():
        if e.type==pygame.QUIT: running=False
        if e.type==pygame.KEYDOWN and not dead:
            if e.key==pygame.K_UP and direction!="DOWN":direction="UP"
            elif e.key==pygame.K_DOWN and direction!="UP":direction="DOWN"
            elif e.key==pygame.K_LEFT and direction!="RIGHT":direction="LEFT"
            elif e.key==pygame.K_RIGHT and direction!="LEFT":direction="RIGHT"
        if e.type==pygame.KEYDOWN and dead and e.key==pygame.K_SPACE:
            snake,direction,score=reset(); dead=False
    if not dead:
        head=snake[0].copy()
        if direction=="UP":head[1]-=BLOCK
        elif direction=="DOWN":head[1]+=BLOCK
        elif direction=="LEFT":head[0]-=BLOCK
        elif direction=="RIGHT":head[0]+=BLOCK
        snake.insert(0,head)
        if snake[0]==food:
            food=[random.randrange(0,40)*20,random.randrange(0,30)*20];score+=1
        else: snake.pop()
        x,y=head
        if x<0 or x>=800 or y<0 or y>=600 or head in snake[1:]:
            dead=True
    color=(255,0,0) if dead else (0,255,0)
    for x,y in snake: pygame.draw.rect(screen,color,(x,y,BLOCK,BLOCK))
    pygame.draw.rect(screen,(255,50,50),(food[0],food[1],BLOCK,BLOCK))
    if dead:
        t=font.render("YOU DIED - Nhấn SPACE để restart",True,(255,255,255))
        screen.blit(t,(100,250))
    pygame.display.flip(); clock.tick(speed)
pygame.quit()




