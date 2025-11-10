# Tên file: test_client.py
# Dùng để test server.py (Day 2)

import socket
import threading
import json
import time

# --- Cấu hình Client ---
HOST = '127.0.0.1' # Dùng IP của server nếu chạy 2 máy
PORT = 5555
ADDR = (HOST, PORT)
BUFFER_SIZE = 2048

my_id = -1 # Server sẽ gán ID

def receive_messages(client_socket):
    """
    Thread này lắng nghe tất cả tin nhắn từ server.
    """
    global my_id
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                print("\n[KẾT NỐI] Server đã đóng.")
                break
            
            try:
                message_json = json.loads(data.decode('utf-8'))
                
                # In ra log (Nhiệm vụ Day 5)
                print(f"\n[SERVER GỬI]: {message_json}")

                # Xử lý tin nhắn "welcome"
                if message_json.get('type') == 'welcome':
                    my_id = message_json.get('id')
                    print(f"Server chào mừng! ID của tôi là: {my_id}")
                    print(f"Các player đang chơi: {message_json.get('all_players')}")

                # In ra các tin nhắn broadcast khác
                elif message_json.get('type') == 'new_player':
                    print(f"Người chơi mới (ID: {message_json['data']['id']}) vừa vào.")
                elif message_json.get('type') == 'player_left':
                    print(f"Người chơi (ID: {message_json['id']}) vừa thoát.")
                elif message_json.get('type') == 'move':
                    print(f"Người chơi (ID: {message_json['sender_id']}) di chuyển: {message_json['direction']}")
                
                print("Nhập lệnh (UP/DOWN/LEFT/RIGHT, hoặc exit): ", end="")

            except json.JSONDecodeError:
                print(f"\n[LỖI] Server gửi data không phải JSON: {data.decode('utf-8')}")
            except Exception as e:
                print(f"\n[LỖI XỬ LÝ]: {e}")

    except ConnectionResetError:
        print("\n[LỖI] Mất kết nối tới server.")
    finally:
        client_socket.close()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(ADDR)
        print(f"[THÀNH CÔNG] Đã kết nối tới {HOST}:{PORT}")
    except socket.error as e:
        print(f"Lỗi khi kết nối: {e}")
        return

    # Chạy thread để lắng nghe server
    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    recv_thread.daemon = True
    recv_thread.start()

    # Vòng lặp chính để gửi lệnh (Nhiệm vụ Day 2 - Client 2)
    try:
        while True:
            message = input("Nhập lệnh (UP/DOWN/LEFT/RIGHT, hoặc exit): ")
            
            if message.lower() == 'exit':
                break

            # Gửi lệnh di chuyển (Theo chuẩn JSON)
            move_cmd = {
                "type": "move",
                "direction": message.upper()
            }
            
            try:
                client_socket.send(json.dumps(move_cmd).encode('utf-8'))
            except socket.error as e:
                print(f"[LỖI GỬI] {e}")
                break
            
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nĐang thoát...")
    finally:
        client_socket.close()
        print("Đã đóng client.")

if __name__ == "__main__":
    start_client()