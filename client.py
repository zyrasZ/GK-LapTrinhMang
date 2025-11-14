# client.py - PHIÊN BẢN HOÀN CHỈNH ĐÃ SỬA LỖI
import socket
import threading
import json
import pygame
import sys
import time

# Cấu hình
HOST = "127.0.0.1"  # đổi thành IP server nếu chạy LAN
PORT = 5555

# Hiển thị
CELL = 20  # bạn có thể giảm xuống 15 hoặc 10 nếu muốn vừa màn hình
WIDTH = 30
HEIGHT = 20
SCREEN_W = CELL * WIDTH
SCREEN_H = CELL * HEIGHT

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Snake Multiplayer Client")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

# trạng thái game nhận từ server
snakes = {}   # pid -> {"body": [(x,y)...], "alive": bool, "score": int}
food = (0,0)
my_id = None
running = True

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST, PORT))
    print("Đã kết nối tới server!")
except Exception as e:
    print(f"Lỗi kết nối server: {e}")
    sys.exit(1)

sock_lock = threading.Lock()

def send_msg(obj):
    data = json.dumps(obj) + '\n'
    with sock_lock:
        try:
            sock.sendall(data.encode())
        except:
            pass

def recv_thread():
    global snakes, food, my_id, running
    buf = ""
    while running:
        try:
            data = sock.recv(4096).decode()
            if not data:
                break
            buf += data
            while '\n' in buf:
                line, buf = buf.split('\n', 1)
                if not line.strip():
                    continue
                try:
                    msg = json.loads(line)
                except:
                    continue
                if msg.get("type") == "id":
                    my_id = msg.get("id")
                    print("Assigned id:", my_id)
                elif msg.get("type") == "update":
                    # cập nhật toàn bộ
                    snakes = msg.get("snakes", {})
                    food = tuple(msg.get("food", (0,0)))
                elif msg.get("type") == "pong":
                    pass
        except Exception:
            break
    running = False

threading.Thread(target=recv_thread, daemon=True).start()

def draw():
    screen.fill((50,50,50))
    # vẽ food
    fx, fy = food
    pygame.draw.rect(screen, (255, 0, 0), (fx*CELL, fy*CELL, CELL, CELL))
    # vẽ snakes
    for pid, info in snakes.items():
        body = info.get("body", [])
        alive = info.get("alive", True)
        # chọn màu khác cho chính mình
        if pid == my_id:
            head_color = (0, 200, 0)
            body_color = (0, 150, 0)
        else:
            head_color = (0, 120, 255)
            body_color = (0, 90, 180)
        if not alive:
            head_color = (120, 120, 120)
            body_color = (90, 90, 90)
        for i, (x,y) in enumerate(body):
            col = head_color if i == 0 else body_color
            pygame.draw.rect(screen, col, (x*CELL, y*CELL, CELL, CELL))
    # vẽ scores góc trên
    y = 5
    for pid, info in snakes.items():
        score = info.get("score", 0)
        text = f"{pid}: {score}"
        img = font.render(text, True, (255,255,255))
        screen.blit(img, (5, y))
        y += 18
    pygame.display.flip()

def main_loop():
    global running
    move_cooldown = 0.08  # giãn gửi phím (s)
    last_sent = 0
    current_dir = None
    while running:
        dt = clock.tick(60) / 1000.0  # 60 FPS cho mượt
        last_sent += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                send_msg({"type":"quit"})
                break
        
        keys = pygame.key.get_pressed()
        dir_to_send = None
        if keys[pygame.K_UP]:
            dir_to_send = "UP"
        elif keys[pygame.K_DOWN]:
            dir_to_send = "DOWN"
        elif keys[pygame.K_LEFT]:
            dir_to_send = "LEFT"
        elif keys[pygame.K_RIGHT]:
            dir_to_send = "RIGHT"
        
        # gửi hướng mới nếu thay đổi và cooldown đủ
        if dir_to_send and dir_to_send != current_dir and last_sent > move_cooldown:
            send_msg({"type": "move", "dir": dir_to_send})
            current_dir = dir_to_send
            last_sent = 0
        
        # QUAN TRỌNG: GỌI DRAW() Ở ĐÂY!
        draw()
    
    pygame.quit()
    sock.close()
    sys.exit()

# CHẠY VÒNG LẶP CHÍNH - ĐÂY LÀ PHẦN BỊ THIẾU!
if __name__ == "__main__":
    print("Khởi động client...")
    main_loop()