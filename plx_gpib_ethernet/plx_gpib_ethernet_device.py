from plx_gpib_ethernet import PrologixGPIBEthernet


class PrologixGPIBEthernetDevice:
    def __init__(self, address, *args, **kwargs):
        self.address = address
        self.gpib = PrologixGPIBEthernet(*args, **kwargs)

    def connect(self):
        self.gpib.connect()
        self.gpib.select(self.address)

    def close(self):
        self.gpib.close()

    def write(self, *args):
        return self.gpib.write(*args)

    def read(self, *args):
        return self.gpib.read(*args)

    def query(self, *args):
        return self.gpib.query(*args)

    def idn(self):
        return self.query('*IDN?')

    def reset(self):
        self.write('*RST')
