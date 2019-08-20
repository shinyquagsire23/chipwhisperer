import socket

class LiteGUI:
    __init__(self):
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_DGRAM)

    def write(self, data, port=0x2B3E):
        sock.sendto(data, ("127.0.0.1", port))
