from plx_gpib_ethernet import PrologixGPIBEthernet
import pytest
from support import MockSocket
from random import randint


@pytest.fixture
def plx_with_mock_socket():
    plx = PrologixGPIBEthernet('example.com')
    plx.socket = MockSocket('example.com', 1234)

    return plx, plx.socket


# class variable
def test_it_uses_correct_port():
    plx = PrologixGPIBEthernet('example.com')

    assert plx.PORT == 1234


# .__init__
def test_it_sets_host():
    plx = PrologixGPIBEthernet('example.com')

    assert plx.host == 'example.com'


def test_it_has_default_timeout_of_1s():
    plx = PrologixGPIBEthernet('example.com')

    assert plx.timeout == 1


def test_it_uses_custom_timeout():
    plx = PrologixGPIBEthernet('example.com', timeout=0.5)

    assert plx.timeout == 0.5


def test_it_raises_value_error_for_invalid_timeout():
    for invalid_timeout in (1e-3 - 1e-12, 3 + 1e-12):
        with pytest.raises(ValueError):
            PrologixGPIBEthernet('example.com', timeout=invalid_timeout)


# .connect
def test_it_connects(plx_with_mock_socket):
    plx, mock_socket = plx_with_mock_socket
    plx.connect()

    assert mock_socket.connected is True


def test_it_initializes_adapter(plx_with_mock_socket):
    plx, mock_socket = plx_with_mock_socket
    plx.connect()

    expected_buffer = ['++mode 1\n',
                       '++auto 0\n',
                       '++read_tmo_ms 1000\n',
                       '++eos 3\n']
    assert mock_socket.out_buffer == expected_buffer


# .close
def test_it_closes_socket(plx_with_mock_socket):
    plx, mock_socket = plx_with_mock_socket
    plx.connect()

    plx.close()

    assert mock_socket.closed is True


# .select
def test_it_sets_gpib_address(plx_with_mock_socket):
    plx, mock_socket = plx_with_mock_socket
    plx.connect()

    addr = randint(0, 12)
    plx.select(addr)

    expected_command = '++addr %i\n' % addr
    assert mock_socket.out_buffer[-1] == expected_command


# .write
def test_it_sends_gpib_command(plx_with_mock_socket):
    plx, mock_socket = plx_with_mock_socket
    plx.connect()

    plx.write('*RST')

    expected_command = '*RST\n'
    assert mock_socket.out_buffer[-1] == expected_command


# .read
def test_it_sends_read_command(plx_with_mock_socket):
    plx, mock_socket = plx_with_mock_socket
    plx.connect()

    mock_socket.in_buffer.append('\n')
    plx.read()

    expected_command = '++read eoi\n'
    assert mock_socket.out_buffer[-1] == expected_command


def test_it_read_gpib_response(plx_with_mock_socket):
    plx, mock_socket = plx_with_mock_socket
    plx.connect()

    response = 'Hello World!\n'
    mock_socket.in_buffer.append(response)
    result = plx.read()

    assert result == response


# .query
def test_it_sends_gpib_query(plx_with_mock_socket):
    plx, mock_socket = plx_with_mock_socket
    plx.connect()

    mock_socket.in_buffer.append('\n')
    plx.query('*IDN?')

    expected_commands = ['*IDN?\n', '++read eoi\n']
    assert mock_socket.out_buffer[-2:] == expected_commands


def test_it_reads_gpib_query_response(plx_with_mock_socket):
    plx, mock_socket = plx_with_mock_socket
    plx.connect()

    response = 'Hello World!\n'
    mock_socket.in_buffer.append(response)
    result = plx.query('*IDN?')

    assert result == response


# .set_timeout
def test_it_sets_custom_timeout(plx_with_mock_socket):
    plx, _ = plx_with_mock_socket
    timeout = 2 + (randint(0, 10) / 10)
    plx.set_timeout(timeout)

    assert plx.timeout == timeout
