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

from time import sleep
from time import time as now

import numpy as np
from pyvisa import VisaIOError

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import strict_discrete_set, truncated_range, strict_range


class AgilentE4418B(Instrument):
    """Represents the Agilent E4418B Power Meter for measuring RF/Microwave
    power at a given frequency.

    This device has one or two channels which would be displaced in one or two of the
    windows on the display.

    Keyword arguements:
    :param pymeasure.adapter adapter: Adapter used to connect to instrument
    :param str name: Name of the device or generated from the `AgilentE4418B.id` call on `__init__`
    """

    def __init__(
        self,
        adapter=None,
        name=None,
        **kwargs,
    ):
        super().__init__(adapter=adapter, name=None, includeSCPI=True, **kwargs)

        self._manu = ""
        self._model = ""
        self._fw = ""
        self._sn = ""
        self._options = ""


        if name is None:
            # written this way to pass 'test_all_instruments.py' while allowing the
            # *IDN? to populate the name of the VNA
            try:
                self._manu, self._model, _, self._fw = self.id
            except ValueError:
                self._manu = "Agilent"
                self._model = "E4418B"
            self._desc = "Power Meter"
            name = self.name = f"{self._manu} {self._model} {self._desc}"
        else:
            self.name = name

    def ask(self, command, query_delay=None):
        self.adapter.write(command)
        if query_delay is not None:
            sleep(query_delay)
        return self.adapter.read()

    @property
    def id(self):
       self._manu, self._model, _, self._fw = self.ask('*IDN?').split(',')
       return [self._manu, self._model, '', self._fw]
    # id = Instrument.measurement('*IDN?', """Get the id of the device""")


    frequency = Instrument.control('SENS:FREQ?',
                                   'SENS:FREQ %e',
                                   """Control the frequency the power meter corrects its
                                    measurement for in Hz. Value range can be changed based
                                    on the power head used.

                                    Type: :code:`float`

                                    .. code-block:: python

                                        # set the frequency to 1.21GHz 
                                        instr.frequency = 1.21e9

                                        if instr.frequency == 10e6:
                                            pass

                                    """,
                                   values=[10e6, 18e9],
                                   validator=strict_range,
                                   dynamic=True,
                                   cast=float)

    offset = Instrument.control('CORR:LOSS2?',
                                'CORR:LOSS2 %e',
                                """
                                Control the offset applied (in dB) to the power sensor measurement
                                to account for cable and other losses to the power meter. (float) 
                                """,
                                cast=float,
                                validator=strict_range,
                                values=[-100,100])

    enable_offset = Instrument.control('CORR:LOSS2:STAT?',
                                       'CORR:LOSS2:STAT %s',
                                       """
                                       Control the offset applied (in dB) to the power sensor measurement
                                       to account for cable and other losses to the power meter. (float) 
                                       """,
                                       cast=bool,
                                       values={True: 'ON',
                                               False: 'OFF'}
                                       )

    average_count = None
    averaging_enable = None
    auto_averaging = None
    filter = None
    filter_enabled = None
    filter_mode = None
    trigger_auto_delay = None
    trigger_source = None
    trigger_immediate = None
    trigger_continuous = None
    read = None
    measure = None
    resolution = None
    zero = None
    calibrate = None
    power_reference_enabled = None # Enable/Disable
    step_determination_enabled = None
    relative_offset = None
    relative_offset_enabled = None
    upper_window_unit = Instrument.control('UNIT1:POW?',
                                           'UNIT1:POW %s',
                                           """
                                           Control the measurement units for the upper window. (string)
                                           """,
                                           cast=str,

                                    )
    lower_window_unit = Instrument.control('UNIT2:POW?',
                                           'UNIT2:POW %s',
                                           """
                                           Control the measurement units for the lower window. (string)
                                           """,
                                           cast=str,

                                    )
