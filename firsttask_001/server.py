import socket
from datetime import datetime

HOST = "127.0.0.1"   # localhost
PORT = 5050           # arbitrary non-privileged port

def main():
    # 1. Create a stream (TCP) socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allows quick restart of the server without "Address already in use" errors
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. Bind to address and port
    server_socket.bind((HOST, PORT))

    # 3. Listen for incoming connections (always running)
    server_socket.listen()
    print(f"[SERVER] Listening on {HOST}:{PORT} ... (Ctrl+C to stop)")

    try:
        while True:
            # 4. Accept a client connection (blocks until one arrives)
            client_socket, client_address = server_socket.accept()
            print(f"[SERVER] Connection from {client_address}")

            with client_socket:
                # Get current date and time
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Send it to the client (encode string -> bytes)
                client_socket.send(now.encode("utf-8"))
                print(f"[SERVER] Sent: {now}")
            # 'with' block auto-closes the client connection here
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
