import socket
import sys
import os.path

HOST = "localhost"
PORT = 5555

RESPOSTA = {200: "HTTP/1.1 200 OK\r\n", 
            404: "HTTP/1.1 404 Not Found\r\n"}

HEADERS = ("Content-Type: text/html\r\n"
"Server: Marti_Lu\r\n"
"\r\n")

def existeix_fitxer(nom_fitxer = "index.html"):
    return os.path.isfile(nom_fitxer)

def contingut_fitxer(nom_fitxer = "index.html"):
    log(f"Obrint fitxer: {nom_fitxer}")
    with open(nom_fitxer, "r") as fitxer:
        contingut = ""
        for linia in fitxer:
            contingut += linia
        return contingut

def log(message):
    print(message)

class GestorCiclePeticioResposta():
    def __init__(self, connexio):
        self.socket_request = Socket_Request(connexio)
    
    def cicle(self):
        log("Cicle iniciat!")
        self.request = self.socket_request.dades
        if self.request:
            self.response = self.make_response()
            self.socket_request.enviar_resposta(self.response)
       

    def make_response(self):
        if self.socket_request.metode == "GET": 
            return self.make_get_response()

    
    def make_get_response(self):
        response = ""
        if existeix_fitxer(self.socket_request.nom_fitxer):
            codi = RESPOSTA[200]
            resposta = contingut_fitxer(self.socket_request.nom_fitxer)

        else:
            codi = RESPOSTA[404]
            resposta = ""
        return f"{codi}{HEADERS}{resposta}"


class Socket_Request():
    def __init__(self, connexio):
        (self.socket, self.adreca) = connexio
        log(f"Connectat des de {self.adreca[0]} (PORT: {self.adreca[1]})")
        self.rebre_request()

        if self.dades:
            log(self.dades)
            self.metode = self.get_metode()
            self.recurs = self.get_recurs()
            self.nom_fitxer = self.get_nom_fitxer()
            log(self.metode)
            log(self.recurs)
            log(self.nom_fitxer)
        else:
            log("Petició buida - Socket tancat!")
            log("""
        ---------------------
            """)

    def rebre_request(self):
        log("Rebent petició...")
        self.dades = self.socket.recv(2048).decode()
        if not self.dades: self.socket.close()
        return self.dades

    def enviar_resposta(self, resposta):
        log("Enviant resposta...")
        log("""
        ---------------------
            """)
        self.socket.sendall(resposta.encode())
        self.socket.close()

    
    def get_metode(self):
        return self.dades.split("\n")[0].split(" ")[0]

    def get_recurs(self):
        return self.dades.split("\n")[0].split(" ")[1]
    
    def get_nom_fitxer(self):
        if len(self.recurs) > 1:
            return self.recurs[1:]
        else:
            return "index.html"


class Servidor():
    def __init__(self, host = HOST, port = PORT):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port

    def executar(self, listeners = 10):
        with self.socket_servidor as s:
            s.bind((self.host, self.port))
            s.listen(listeners)

            while True:
                self.gestor_cicle_peticio_resposta = GestorCiclePeticioResposta(s.accept())
                self.gestor_cicle_peticio_resposta.cicle()


def main():
    print(f"Accedeix per http://{HOST}:{PORT}")
    servidor_local = Servidor()
    servidor_local.executar()

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nTancant el servidor...\n")
        sys.exit(1)
    
    except Exception as exc:
        print("Error:\n")
        print(exc)