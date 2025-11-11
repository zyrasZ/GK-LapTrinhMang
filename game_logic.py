# game_logic.py
import random

# Kích thước bản đồ (ô)
WIDTH = 30   # số ô ngang
HEIGHT = 20  # số ô dọc

# Hướng di chuyển
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

class Snake:
    def __init__(self, player_id, start_pos):
        self.player_id = player_id
        self.body = [start_pos]   # danh sách [ (x,y), ... ] - head là index 0
        self.direction = "RIGHT"  # hướng mặc định
        self.grow_pending = 0     # số lần cần dài thêm (khi ăn mồi)
        self.alive = True
        self.score = 0

    def set_direction(self, new_dir):
        """Đổi hướng di chuyển, tránh quay ngược"""
        if new_dir not in DIRECTIONS:
            return
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if opposites.get(new_dir) != self.direction:
            self.direction = new_dir

    def move(self):
        """Di chuyển 1 bước theo hướng hiện tại. Không cho vòng qua map (đâm tường => chết)."""
        if not self.alive:
            return
        dx, dy = DIRECTIONS[self.direction]
        head_x, head_y = self.body[0]
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)

        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            # nếu chỉ 1 ô thì pop không gây lỗi
            if len(self.body) > 1:
                self.body.pop()

    def grow(self):
        """Khi ăn mồi"""
        self.grow_pending += 1
        self.score += 1

    def check_collision_self(self):
        """Va chạm chính mình"""
        head = self.body[0]
        if head in self.body[1:]:
            self.alive = False
            return True
        return False

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))

class Game:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.snakes = {}  # {player_id: Snake}
        self.food = Food()

    def add_player(self, player_id):
        """Thêm rắn mới vào game với vị trí khởi tạo không trùng"""
        # Tìm vị trí không trùng với rắn khác
        for _ in range(100):
            pos = (random.randint(2, self.width - 3), random.randint(2, self.height - 3))
            collision = False
            for s in self.snakes.values():
                if pos in s.body:
                    collision = True
                    break
            if not collision:
                self.snakes[player_id] = Snake(player_id, pos)
                return self.snakes[player_id]
        # fallback
        self.snakes[player_id] = Snake(player_id, (1,1))
        return self.snakes[player_id]

    def remove_player(self, player_id):
        if player_id in self.snakes:
            del self.snakes[player_id]

    def update(self):
        """Cập nhật toàn bộ game mỗi tick: di chuyển, kiểm tra ăn mồi, va chạm"""
        # move tất cả snakes
        for snake in list(self.snakes.values()):
            if snake.alive:
                snake.move()

        # kiểm tra va chạm vào tường
        for snake in list(self.snakes.values()):
            if not snake.alive:
                continue
            hx, hy = snake.body[0]
            if hx < 0 or hx >= self.width or hy < 0 or hy >= self.height:
                snake.alive = False

        # kiểm tra va chạm rắn với rắn khác (head chạm body của other)
        for pid, snake in self.snakes.items():
            if not snake.alive:
                continue
            head = snake.body[0]
            # với chính nó
            if head in snake.body[1:]:
                snake.alive = False
                continue
            # với others
            for other_id, other in self.snakes.items():
                if other_id == pid:
                    continue
                if head in other.body:
                    snake.alive = False
                    break

        # kiểm tra ăn mồi (nên cho ăn trước/hoặc sau move — ở đây là sau move)
        for snake in self.snakes.values():
            if not snake.alive:
                continue
            if snake.body[0] == self.food.position:
                snake.grow()
                # đảm bảo mồi mới không rơi trùng lên rắn
                for _ in range(100):
                    newpos = self.food.random_position()
                    collision = False
                    for s in self.snakes.values():
                        if newpos in s.body:
                            collision = True
                            break
                    if not collision:
                        self.food.position = newpos
                        break

    def respawn_player(self, player_id):
        """Gọi khi muốn cho người chơi sống lại"""
        if player_id in self.snakes:
            snake = self.snakes[player_id]
            snake.body = [(random.randint(2, self.width-3), random.randint(2, self.height-3))]
            snake.direction = "RIGHT"
            snake.grow_pending = 0
            snake.alive = True
            snake.score = 0

    def get_game_state(self):
        """Trả về trạng thái để gửi cho client (JSON-friendly)"""
        return {
            "type": "update",
            "snakes": {
                pid: {
                    "body": snake.body,
                    "alive": snake.alive,
                    "score": snake.score
                }
                for pid, snake in self.snakes.items()
            },
            "food": self.food.position
        }

# để test logic độc lập
if __name__ == "__main__":
    g = Game()
    g.add_player("p1")
    g.add_player("p2")
    for i in range(10):
        g.snakes["p1"].set_direction("RIGHT")
        g.snakes["p2"].set_direction("DOWN")
        g.update()
        print(g.get_game_state())
