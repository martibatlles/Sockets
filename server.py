import socket 

HOST = 'localhost'
PORT = 1818

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    print(id(s))
    print("--")

    conn, addr = s.accept()
    print(type(conn))
    print(id(conn))

    with conn:
        print(f"Connectat des de {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
            print(repr(data))