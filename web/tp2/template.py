import http.server
import socketserver
import socket

#Petit wrapper pour qui crée un serveur TCP/IP permettant d'être interrompu
#en pressant CTRL-C dans la console
class MyHttpServer(socketserver.TCPServer):

    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def serve_until_interrupted(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            self.shutdown()
        finally:
            self.server_close()


if __name__ == "__main__":
    HTTPD = MyHttpServer(("localhost", 8080), http.server.SimpleHTTPRequestHandler)
    HTTPD.serve_until_interrupted()
