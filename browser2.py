import socket

with socket.socket(socket.AF_INET, socket. SOCK_STREAM) as s:
    s.connect(('herrera.lu', 80))
    cmd ="dame algo\r\n".encode()
    s.sendall(cmd)

    while True:
        dades = s.recv(2048)
        if not dades:
            break
        print(dades.decode(), end='')
