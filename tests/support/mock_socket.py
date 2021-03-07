class MockSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.connected = False
        self.closed = False

        self.out_buffer = []
        self.in_buffer = []

        self.timeout = None

    def connect(self, addr):
        if addr == (self.host, self.port):
            self.connected = True

    def close(self):
        self.connected = False
        self.closed = True

    def send(self, value):
        assert type(value) == bytes
        self.out_buffer.append(value.decode('ascii'))

    def recv(self, byte_num):
        value = self.in_buffer.pop()
        return value.encode('ascii')

    def settimeout(self, timeout):
        self.timeout = timeout
