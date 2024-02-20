#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2024 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import pytest
from pymeasure.instruments.agilent.agilentE4418B import AgilentE4418B
from pymeasure.adapters import PrologixAdapter
from pyvisa.errors import VisaIOError

#pytest.mark.skipif(connected_device_address=='',
#    'Only work with connected hardware', allow_module_level=True)
device_address = pytest.importorskip("check_device_address")

# use this command to run the test without editing it
# for prologix adapters
# pytest '.\tests\instruments\agilent\test_agilentE4418B_with_device.py' --device-address="PrologixAdapter,ASRL4::INSTR,13"
# everyone else, the `--device-address` flag works normally
# pytest '.\tests\instruments\agilent\test_agilentE4418B_with_device.py' --device-address="GPIB::whatever::your::visa::says"


@pytest.fixture(scope="module")
def power_meter(connected_device_address):
    try:
        if 'PrologixAdapter' not in connected_device_address:
            power_meter = AgilentE4418B(connected_device_address)
        else:
            _, prologix_address, gpib_address = connected_device_address.split(',')
            prologix = PrologixAdapter(resource_name=prologix_address, visa_library="@py", auto=1)
            # need to ensure `eot_enable` is set to zero otherwise you will have to read twice to
            # get rid of the extra new line character
            prologix.write('++eot_enable 0')
            power_meter = AgilentE4418B(adapter=prologix.gpib(int(gpib_address)))
    except IOError:
        print("Not able to connect to power meter")
        assert False

    yield power_meter

def test_agilentE4418B_get_instrument_id(power_meter):
    # My E4418B enumerates as the following and likely was an amalgamation of two units
    assert ['HEWLETT-PACKARD', 'E4418A', '', 'A1.08.01\n'] == power_meter.id 
    assert power_meter.name == 'HEWLETT-PACKARD E4418A Power Meter'


def test_agilentE4418B_frequency(power_meter):
    power_meter.frequency = 50e6
    assert power_meter.frequency == 50e6

    power_meter.frequency = 2.3e9
    assert power_meter.frequency == 2.3e9

    power_meter.frequency = 12e6
    assert power_meter.frequency == 12e6

    power_meter.reset()

def test_agilentE4418B_offset(power_meter):
    assert False


def test_agilentE4418B_measurement(power_meter):
    # test the power sensor installed to the reference
    assert False


def test_agilentE4418B_zero_and_cal(power_meter):
    # test the power sensor installed to the reference
    assert False

def test_agilentE4418B_averaging(power_meter):
    # test the power sensor installed to the reference
    assert False
