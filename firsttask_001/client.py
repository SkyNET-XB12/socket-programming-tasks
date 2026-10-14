import socket

HOST = "127.0.0.1"   # server's address (must match server.py)
PORT = 5050           # server's port  (must match server.py)

def main():
    # 1. Create a stream (TCP) socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # 2. Connect to the server
        client_socket.connect((HOST, PORT))

        # 3. Receive data from the server (up to 1024 bytes)
        data = client_socket.recv(1024)

        # 4. Decode bytes -> string and print
        print(f"[CLIENT] Date and time from server: {data.decode('utf-8')}")

    # socket auto-closes when the 'with' block ends

if __name__ == "__main__":
    main()

