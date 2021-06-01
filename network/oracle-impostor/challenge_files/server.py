from socketserver import ForkingMixIn, TCPServer, BaseRequestHandler
from handler import handle_connection


class Server(ForkingMixIn, TCPServer):
    allow_reuse_address = True


class Handler(BaseRequestHandler):
    def handle(self) -> None:
        handle_connection(self.request)


if __name__ == "__main__":
    with Server(("0.0.0.0", 1024), Handler) as server:
        print("Started")
        server.serve_forever()
