import socket
import os
import platform

HOST = "127.0.0.1"
PORT = 5555



def receive_full_data(conn):
    data = b''
    while True:
        chunk = conn.recv(1024)
        if len(chunk) < 1024:
            data += chunk
            break
        data += chunk
    return data


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[+] Listening on {HOST}:{PORT}...")

    conn, addr = server.accept()
    print(f"[+] Connected to {addr}")
    initial_data = receive_full_data(conn)
    print(initial_data.decode(errors="ignore"))

    try:
        while True:
            user = os.getenv("USER")
            host = platform.node()
            cwd = os.getcwd()

            command = input(f"{user}@{host}:{cwd}$ ").strip()

            if not command:
                continue

            if command.startswith("cd "):
                try:
                    path = command[3:].strip()
                    os.chdir(path)
                except Exception as e:
                    print(f"[!] cd error: {e}")
                continue

            conn.send(command.encode())

            if command.lower() == "exit":
                print("[+] Closing connection...")
                break

            output = receive_full_data(conn)
            print(output.decode(errors="ignore"))

    except Exception as e:
        print(f"[!] Error: {e}")

    finally:
        conn.close()
        server.close()


if __name__ == "__main__":
    main()