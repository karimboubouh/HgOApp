from backend.server import Server

if __name__ == '__main__':
    # Load a server instance
    server = Server(name="ParamServer", model="LR", dataset="mnist")
    server.start()
