import socket

with socket.socket(socket.AF_INET, socket. SOCK_STREAM) as s:
    s.connect(('hola.es', 80))
    cmd ="GET / HTTP/1.1\r\nHost: hola.es\r\nAccept: text/html\r\nConnection: close\r\n\r\n".encode()
    s.sendall(cmd)

    while True:
        dades = s.recv(2048)
        if not dades:
            break
        print(dades.decode(), end='')
