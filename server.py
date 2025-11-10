# Tên file: server.py
# Nhiệm vụ: Thành viên 1 - Server Core (Cập nhật Day 2)

import socket
import threading
import json

# --- Cấu hình Server ---
HOST = '0.0.0.0'
PORT = 5555
ADDR = (HOST, PORT)
BUFFER_SIZE = 2048

# --- Quản lý trạng thái Server ---
clients = [] # Chỉ lưu socket
players = {} # Lưu state của người chơi (Nhiệm vụ Day 2)
clients_lock = threading.Lock()

# Biến đếm để tạo ID duy nhất cho người chơi
player_id_counter = 0

def broadcast(message_json, _from_conn=None):
    """
    Gửi một thông điệp (đã ở dạng JSON object) cho tất cả client.
    """
    message_bytes = json.dumps(message_json).encode('utf-8')
    
    with clients_lock:
        for conn in clients:
            if conn != _from_conn:
                try:
                    conn.sendall(message_bytes)
                except socket.error as e:
                    print(f"[LỖI BROADCAST] {e}")

def handle_client(conn, addr):
    """
    Xử lý cho từng client trên một thread riêng.
    """
    global player_id_counter
    
    # --- Nhiệm vụ Day 2: Gán ID và gửi Welcome ---
    with clients_lock:
        player_id = player_id_counter
        player_id_counter += 1
        
        # Tạo state cơ bản cho player (Thành viên 3 sẽ dùng)
        # Tạm thời chỉ lưu ID và addr
        players[player_id] = {"id": player_id, "addr": str(addr)}
        clients.append(conn)
    
    print(f"[KẾT NỐI MỚI] {addr} được gán ID: {player_id}")

    # 1. Gửi "Welcome" cho *chỉ* client này
    # Gửi ID của họ và danh sách TẤT CẢ player hiện có
    welcome_msg = {
        "type": "welcome",
        "id": player_id,
        "all_players": players 
    }
    try:
        conn.send(json.dumps(welcome_msg).encode('utf-8'))
    except socket.error as e:
        print(f"[LỖI GỬI WELCOME] {e}")
        conn.close()
        return # Thoát thread nếu không gửi được

    # 2. Broadcast cho các client *khác*
    # Thông báo có người chơi mới
    new_player_msg = {
        "type": "new_player",
        "data": players[player_id]
    }
    broadcast(new_player_msg, _from_conn=conn)

    # --- Vòng lặp lắng nghe ---
    try:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break  # Client ngắt kết nối

            # --- Mục tiêu Day 2: Nhận lệnh và broadcast lại ---
            try:
                # Giả định client gửi JSON
                message_str = data.decode('utf-8')
                message_json = json.loads(message_str)
                
                # In ra log (Nhiệm vụ Day 5)
                print(f"[NHẬN TỪ ID {player_id}]: {message_json}")

                # Mục tiêu Day 2: "broadcast lại"
                # Thêm 'id' của người gửi vào tin nhắn
                message_json['sender_id'] = player_id 
                
                broadcast(message_json, _from_conn=conn)

            except json.JSONDecodeError:
                print(f"[LỖI] {addr} gửi data không phải JSON.")
            except UnicodeDecodeError:
                print(f"[LỖI] {addr} gửi data không phải utf-8.")

    except ConnectionResetError:
        print(f"[NGẮT KẾT NỐI] {addr} (ID: {player_id}) ngắt đột ngột.")
    except Exception as e:
        print(f"[LỖI] {addr} (ID: {player_id}): {e}")
    finally:
        # Dọn dẹp khi client thoát
        print(f"[THOÁT] {addr} (ID: {player_id}) đã rời.")
        
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
            
            # Xóa khỏi danh sách player
            if player_id in players:
                del players[player_id]
        
        # Broadcast thông báo có người thoát
        player_left_msg = {
            "type": "player_left",
            "id": player_id
        }
        broadcast(player_left_msg, _from_conn=conn)
        
        conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind(ADDR)
    except socket.error as e:
        print(f"Lỗi khi bind: {e}")
        return

    server_socket.listen()
    print(f"[SERVER] Đang lắng nghe trên {HOST}:{PORT}")
    print("-----------------------------------------")

    try:
        while True:
            conn, addr = server_socket.accept()
            
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()

            print(f"[HOẠT ĐỘNG] Số client đang kết nối: {len(clients) + 1}")

    except KeyboardInterrupt:
        print("\n[SERVER] Đang tắt...")
    finally:
        with clients_lock:
            for conn in clients:
                conn.close()
        server_socket.close()
        print("[SERVER] Đã tắt hoàn toàn.")

if __name__ == "__main__":
    start_server()