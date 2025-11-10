# Tên file: test_client.py
# Dùng để test server.py

import socket
import threading
import time

# --- Cấu hình Client ---
# Gõ 'localhost' hoặc '127.0.0.1' nếu chạy client
# cùng máy với server.
# Nếu server chạy ở máy khác, gõ IP của máy đó.
HOST = '127.0.0.1' 
PORT = 5555
ADDR = (HOST, PORT)
BUFFER_SIZE = 2048

def receive_messages(client_socket):
    """
    Một thread riêng chỉ để lắng nghe tin nhắn từ server.
    """
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                print("[KẾT NỐI] Server đã đóng kết nối.")
                break
            
            # In ra mọi thứ server gửi
            print(f"\n[SERVER GỬI]: {data.decode('utf-8')}\nNhập lệnh: ", end="")

    except ConnectionResetError:
        print("[LỖI] Mất kết nối tới server.")
    except Exception as e:
        print(f"[LỖI NHẬN DATA] {e}")
    finally:
        client_socket.close()
        print("Đã ngắt kết nối.")

def start_client():
    # 1. Tạo socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Kết nối tới server
    try:
        client_socket.connect(ADDR)
        print(f"[THÀNH CÔNG] Đã kết nối tới {HOST}:{PORT}")
    except socket.error as e:
        print(f"Lỗi khi kết nối: {e}")
        return

    # 3. Chạy thread để lắng nghe server
    # (Nhiệm vụ Day 3: receive_updates)
    recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    recv_thread.daemon = True
    recv_thread.start()

    # 4. Vòng lặp chính để gửi dữ liệu
    # (Nhiệm vụ Day 2: Gửi lệnh di chuyển)
    try:
        while True:
            # Giả lập gửi lệnh
            message = input("Nhập lệnh (vd: 'UP', 'DOWN', 'exit'): ")
            
            if message.lower() == 'exit':
                break

            try:
                # Gửi dữ liệu lên server
                client_socket.send(message.encode('utf-8'))
            except socket.error as e:
                print(f"[LỖI GỬI] {e}")
                break
            
            time.sleep(0.1) # Ngủ 1 chút

    except KeyboardInterrupt:
        print("\nĐang thoát...")
    finally:
        client_socket.close()
        print("Đã đóng client.")

# --- Chạy Client ---
if __name__ == "__main__":
    start_client()