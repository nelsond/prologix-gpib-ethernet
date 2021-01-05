import socket


class PrologixGPIBEthernet:
    PORT = 1234

    def __init__(self, host, timeout=1):
        # see user manual for details on accepted timeout values
        # https://prologix.biz/downloads/PrologixGpibEthernetManual.pdf#page=13

        self.host = host
        self.timeout = 0
        self.socket = socket.socket(socket.AF_INET,
                                    socket.SOCK_STREAM,
                                    socket.IPPROTO_TCP)
        self.set_timeout(timeout)
        self._read_mode = "ascii"

    def set_mode(self, mode):
        self._read_mode = mode

    def set_timeout(self, value):
        if timeout < 1e-3 or timeout > 3:
            raise ValueError('Timeout must be >= 1e-3 (1ms) and <= 3 (3s)')
        self.timeout = value
        self.socket.settimeout(self.timeout)

    def connect(self):
        self.socket.connect((self.host, self.PORT))
        self._setup()

    def close(self):
        self.socket.close()

    def select(self, addr):
        self._send('++addr %i' % int(addr))

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

    def _decode(self, value):
        if self._read_mode == "ascii":
            return value.decode("ascii")
        elif self._read_mode == "binary":
            return value

    def _recv(self, byte_num):
        value = self.socket.recv(byte_num)
        return self._decode(value)

    def _setup(self):
        # set device to CONTROLLER mode
        self._send('++mode 1')

        # disable read after write
        self._send('++auto 0')

        # set GPIB timeout
        self._send('++read_tmo_ms %i' % int(self.timeout*1e3))

        # do not require CR or LF appended to GPIB data
        self._send('++eos 3')
