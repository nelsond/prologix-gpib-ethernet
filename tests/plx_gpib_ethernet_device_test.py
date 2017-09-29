from plx_gpib_ethernet import PrologixGPIBEthernetDevice


# .__init__
def test_it_sets_address():
    device = PrologixGPIBEthernetDevice(host='example.com', address=10)

    assert device.address == 10


# .connect
def test_it_calls_gpib_connect():
    class MockGPIB:
        def __init__(self):
            self.has_been_called = False

        def connect(self):
            self.has_been_called = True

        def select(self, *args):
            pass

    device = PrologixGPIBEthernetDevice(host='example.com', address=10)
    device.gpib = MockGPIB()
    device.connect()

    assert device.gpib.has_been_called is True


def test_it_calls_gpib_select_with_address():
    class MockGPIB:
        def __init__(self):
            self.has_been_called_with = None

        def connect(self):
            pass

        def select(self, *args):
            self.has_been_called_with = args

    device = PrologixGPIBEthernetDevice(host='example.com', address=10)
    device.gpib = MockGPIB()
    device.connect()

    assert device.gpib.has_been_called_with == (10,)


# .close
def test_it_calls_gpib_close():
    class MockGPIB:
        def __init__(self):
            self.has_been_called = False

        def close(self):
            self.has_been_called = True

    device = PrologixGPIBEthernetDevice(host='example.com', address=10)
    device.gpib = MockGPIB()

    device.close()

    assert device.gpib.has_been_called is True


# .write
def test_it_calls_gpib_write():
    class MockGPIB:
        def __init__(self):
            self.has_been_called_with = None

        def write(self, *args):
            self.has_been_called_with = args

    device = PrologixGPIBEthernetDevice(host='example.com', address=10)
    device.gpib = MockGPIB()
    device.write('Hello World!')

    assert device.gpib.has_been_called_with == ('Hello World!',)


# .read
def test_it_calls_gpib_read():
    class MockGPIB:
        def __init__(self):
            self.has_been_called_with = None

        def read(self, *args):
            self.has_been_called_with = args

    device = PrologixGPIBEthernetDevice(host='example.com', address=10)
    device.gpib = MockGPIB()
    device.read(1024)

    assert device.gpib.has_been_called_with == (1024,)


def test_it_returns_gpib_read():
    class MockGPIB:
        def read(self, *args):
            return 'Hello World!'

    device = PrologixGPIBEthernetDevice(host='example.com', address=10)
    device.gpib = MockGPIB()
    result = device.read(1024)

    assert result == 'Hello World!'


# .query
def test_it_calls_gpib_query():
    class MockGPIB:
        def __init__(self):
            self.has_been_called_with = None

        def query(self, *args):
            self.has_been_called_with = args

    device = PrologixGPIBEthernetDevice(host='example.com', address=10)
    device.gpib = MockGPIB()
    device.query('*IDN?')

    assert device.gpib.has_been_called_with == ('*IDN?',)


def test_it_returns_gpib_query():
    class MockGPIB:
        def query(self, *args):
            return 'Hello World!'

    device = PrologixGPIBEthernetDevice(host='example.com', address=10)
    device.gpib = MockGPIB()
    result = device.query('*IDN?')

    assert result == 'Hello World!'


# .idn
def test_it_calls_gpib_query_with_idn():
    class MockGPIB:
        def __init__(self):
            self.has_been_called_with = None

        def query(self, *args):
            self.has_been_called_with = args

    device = PrologixGPIBEthernetDevice(host='example.com', address=10)
    device.gpib = MockGPIB()
    device.idn()

    assert device.gpib.has_been_called_with == ('*IDN?',)


def test_it_returns_gpib_query_with_idn():
    class MockGPIB:
        def query(self, *args):
            return 'Hello World!'

    device = PrologixGPIBEthernetDevice(host='example.com', address=10)
    device.gpib = MockGPIB()
    result = device.idn()

    assert result == 'Hello World!'


# .reset
def test_it_calls_gpib_write_with_rst():
    class MockGPIB:
        def __init__(self):
            self.has_been_called_with = None

        def write(self, *args):
            self.has_been_called_with = args

    device = PrologixGPIBEthernetDevice(host='example.com', address=10)
    device.gpib = MockGPIB()
    device.reset()

    assert device.gpib.has_been_called_with == ('*RST',)
