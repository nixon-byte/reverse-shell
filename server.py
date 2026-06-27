import socket
import os
import platform

HOST = "127.0.0.1"
PORT = 5555



def receive_full_data(conn):
    data = b''
    while True:
        chunk = conn.recv(4906)
        if len(chunk) < 4906:
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
    cwd = os.getcwd()

    try:
        while True:
            user = os.getenv("USER")
            host = platform.node()
           

            command = input(f"{user}@{host}:{cwd}$ ").strip()

            if not command:
                continue

            if command.startswith("cd "):
                try:
                    conn.send(command.encode())

                    output = receive_full_data(conn).decode(errors="ignore")

                    if output.startswith("cd error:"):
                        print(output, end="")  

                    else:
                        cwd = output.strip()   

                except Exception as e:
                    print(f"[!] Communication error: {e}")
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