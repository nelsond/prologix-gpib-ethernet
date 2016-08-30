import socket

class PrologixGPIBEthernet:
    PORT = 1234

    def __init__(self, host, timeout=1):
        self.host = host
        self.timeout = timeout

        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM,
                                    socket.IPPROTO_TCP)
        self.socket.settimeout(self.timeout)

    def connect(self):
        self.socket.connect( (self.host, self.PORT) )

        self._setup()

    def close(self):
        self.socket.close()

    def select(self, addr):
        self._send( '++addr %i' % int(addr) )

    def write(self, cmd):
        self._send(cmd)

    def read(self, num_bytes=1024):
        self._send('++read eoi')
        return self._recv(num_bytes)

    def query(self, cmd, buffer_size=1024*1024):
        self.write(cmd)
        return self.read(buffer_size)

    def _send(self, value):
        encoded_value = ('%s\n' % value).encode('ascii')
        self.socket.send(encoded_value)

    def _recv(self, byte_num):
        value = self.socket.recv(byte_num)
        return value.decode('ascii')

    def _setup(self):
        # set device to CONTROLLER mode
        self._send('++mode 1')

        # disable read after write
        self._send('++auto 0')

        # set GPIB timeout
        self._send( '++read_tmo_ms %i' % int(self.timeout*1e3) )

        # do not require CR or LF appended to GPIB data
        self._send('++eos 3')
