# Prologix GPIB-to-Ethernet Python wrapper [![Build Status](https://travis-ci.org/nelsond/prologix-gpib-ethernet.svg?branch=master)](https://travis-ci.org/nelsond/prologix-gpib-ethernet) [![Build status](https://ci.appveyor.com/api/projects/status/5xg4cwnyh5y0sk2e/branch/master?svg=true)](https://ci.appveyor.com/project/nelsond/prologix-gpib-ethernet/branch/master)

Simple wrapper for the Prologix GPIB-to-Ethernet adapter. Also includes
a simple device wrapper class.

**Currently only supports the `CONTROLLER` mode of the Prologix
GPIB-to-Ethernet adapter.**

## Requirements

Make sure you can reach/ping the adapter before you start using this
library.

## Install

Install with pip

```shell
pip install git+git://github.com/nelsond/prologix-gpib-ethernet.git
```

## Example usage

### Using the adapter directly

```python
from plx_gpib_ethernet import PrologixGPIBEthernet

gpib = PrologixGPIBEthernet('192.168.1.14')

# open connection to Prologix GPIB-to-Ethernet adapter
gpib.connect()

# select gpib device at address 10
gpib.select(10)

# send a query
gpib.query('*IDN?')
# => 'Stanford_Research_Systems,SR760,s/n41456,ver139\n'

# write without reading
gpib.write('*RST')

# close connection
gpib.close()
```

### Using the device wrapper

Also see [`examples/`](examples/).

```python
from plx_gpib_ethernet import PrologixGPIBEthernetDevice

class ExampleDevice(PrologixGPIBEthernetDevice):
  def start(self):
    self.write('STRT')

  def get_span(self):
    return float( self.query('SPAN?') )

my_device = ExampleDevice(host='192.168.1.14', address=10)

# open connection
my_device.connect()

# run predefined commands
my_device.idn()
# => 'Stanford_Research_Systems,SR760,s/n41456,ver139\n'
my_device.reset()

# run custom commands
my_device.start()
my_device.get_span() # => 0.191

# close connection
mydevice.close()
```

## Development

Install requirements for development environment

```shell
$ pip install -r requirements/dev.txt
```

Run tests

```shell
$ py.test tests/
```

Generate coverage report

```shell
$ py.test --cov=plx_gpib_ethernet tests/
```

## License

MIT License, see file `LICENSE`.
