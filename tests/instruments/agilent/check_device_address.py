import pytest

@pytest.mark.skip(reason="Not meant to be run as a test")

@pytest.fixture
def check_address(connected_device_address):
    if connected_device_address == '':
        raise Exception('No value provided for --device-address')