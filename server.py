# Tên file: server.py
# Nhiệm vụ: Thành viên 1 - Server Core

import socket
import threading
import json  # Sẽ dùng từ Day 2 để gửi/nhận data 

# --- Cấu hình Server ---
# Dùng '0.0.0.0' để server có thể lắng nghe kết nối từ mọi IP
# (Khác với ví dụ '192.168.1.100' trong tài liệu [cite: 10]
# nhưng giúp client ở máy khác dễ dàng kết nối để test)
HOST = '0.0.0.0'
PORT = 5555  # Cổng cố định như kế hoạch [cite: 10]
ADDR = (HOST, PORT)
BUFFER_SIZE = 2048

# --- Quản lý trạng thái Server ---
# Danh sách các kết nối (socket) của client
clients = []
# Lock để bảo vệ danh sách clients khi nhiều thread cùng truy cập
clients_lock = threading.Lock()

# TODO Day 3: Cần một cấu trúc dữ liệu (vd: dict) để lưu trạng thái game
# (vị trí rắn, mồi, điểm...) của tất cả người chơi
# game_state = {}


def broadcast(message, _from_conn=None):
    """
    Gửi một tin nhắn cho tất cả các client đã kết nối.
    Đây là nền tảng cho nhiệm vụ Day 2 (broadcast danh sách) 
    và Day 3 (gửi cập nhật vị trí).
    """
    with clients_lock:
        for conn in clients:
            # Không gửi lại cho client vừa gửi lên (trừ khi cần)
            if conn != _from_conn:
                try:
                    conn.sendall(message.encode('utf-8'))
                except socket.error as e:
                    print(f"[LỖI BROADCAST] {e}")


def handle_client(conn, addr):
    """
    Hàm này được chạy trên một thread riêng cho mỗi client.
    Xử lý nhận/gửi dữ liệu cho 1 client.
    """
    print(f"[KẾT NỐI MỚI] {addr} đã tham gia.")

    # Thêm client vào danh sách chung một cách an toàn
    with clients_lock:
        clients.append(conn)

    # --- Nhiệm vụ Day 2: Gửi "Welcome" & broadcast  ---
    try:
        # 1. Gửi "Welcome"
        welcome_msg = json.dumps({"type": "welcome", "id": f"{addr}"})
        conn.send(welcome_msg.encode('utf-8'))

        # 2. Broadcast thông báo có người mới
        # (Tạm thời gửi text, Day 2 sẽ dùng JSON)
        broadcast(f"Player {addr} has joined.", _from_conn=conn)

        # Vòng lặp lắng nghe dữ liệu từ client
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break  # Client ngắt kết nối

            # TODO Day 2: Xử lý dữ liệu nhận được (ví dụ: lệnh di chuyển) 
            # Dữ liệu nên là JSON 
            try:
                message_str = data.decode('utf-8')
                print(f"[{addr}] Gửi: {message_str}")
                
                # Tạm thời broadcast lại cho các client khác
                # broadcast(message_str, _from_conn=conn)

            except UnicodeDecodeError:
                print(f"[LỖI] {addr} gửi dữ liệu không phải utf-8.")
            except Exception as e:
                print(f"[LỖI XỬ LÝ] {addr}: {e}")

    except ConnectionResetError:
        print(f"[NGẮT KẾT NỐI] {addr} ngắt kết nối đột ngột.")
    except Exception as e:
        print(f"[LỖI] {addr}: {e}")
    finally:
        # Dọn dẹp khi client thoát
        print(f"[THOÁT] {addr} đã rời khỏi.")
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
        
        # TODO Day 2: Broadcast thông báo có người thoát
        broadcast(f"Player {addr} has left.", _from_conn=conn)
        
        conn.close()


def start_server():
    """
    Hàm chính khởi tạo và chạy server.
    Thực hiện nhiệm vụ Day 1.
    """
    # 1. Tạo socket TCP 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Cho phép tái sử dụng địa chỉ ngay lập tức
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. Bind địa chỉ và cổng
    try:
        server_socket.bind(ADDR)
    except socket.error as e:
        print(f"Lỗi khi bind: {e}")
        return

    # 3. Lắng nghe kết nối
    server_socket.listen()
    print(f"[SERVER] Đang lắng nghe trên {HOST}:{PORT}")
    print("-----------------------------------------")

    try:
        # Vòng lặp chính của server, luôn chấp nhận kết nối mới
        while True:
            # 4. Chấp nhận kết nối mới
            conn, addr = server_socket.accept()

            # 5. Tạo thread mới để xử lý client 
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True # Thread sẽ tự tắt khi chương trình chính tắt
            thread.start()

            print(f"[HOẠT ĐỘNG] Số client đang kết nối: {len(clients) + 1}")

    except KeyboardInterrupt:
        print("\n[SERVER] Đang tắt...")
    finally:
        # Đóng tất cả các kết nối client
        with clients_lock:
            for conn in clients:
                conn.close()
        # Đóng server socket
        server_socket.close()
        print("[SERVER] Đã tắt hoàn toàn.")


# --- Chạy Server ---
if __name__ == "__main__":
    start_server()