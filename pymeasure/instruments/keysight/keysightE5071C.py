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


import logging

from pymeasure.instruments import Instrument, Channel
from pymeasure.instruments.validators import strict_range, strict_discrete_set

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class KeysightE5071C(Instrument):
    """
    Need docstring
    """

    def __init__(self, adapter, name="Keysight E5071C", **kwargs):
        super().__init__(
            adapter, name, includeSCPI=True, **kwargs
        )

        self._manu = ""
        self._model = ""
        self._fw = ""
        self._sn = ""
        self._options = ""

        if name is None:
            # written this way to pass 'test_all_instruments.py' while allowing the
            # *IDN? to populate the name of the VNA
            try:
                self._manu, self._model, self._sn, self._fw = self.id
            except ValueError:
                self._manu = "Keysight"
                self._model = "E5071C"
            self._desc = "Vector Network Analyzer"
            name = self.name = f"{self._manu} {self._model} {self._desc}"
        else:
            self.name = name

    marker_1_position = Instrument.control(
        "CALC1:MARK1:X %e",
        "CALC1:MARK1:X?",
        "Control the position of marker 1",
        cast=float,
        )

    marker_1_value = Instrument.measurement(
        "CALC1:MARK1:Y?",
        """
        Read value of marker 1. (complex)
        """,
        cast=complex)

    id = Instrument.measurement(
        "*IDN?",
        """Get the identification of the instrument""",
        cast=str,
    )

    @property
    def manu(self):
        """Get the manufacturer of the instrument."""
        if self._manu == "":
            self._manu, self._model, self._sn, self._fw = self.id
        return self._manu

    @property
    def model(self):
        """Get the model of the instrument."""
        if self._model == "":
            self._manu, self._model, self._sn, self._fw = self.id
        return self._model

    @property
    def fw(self):
        """Get the firmware of the instrument."""
        if self._fw == "":
            self._manu, self._model, self._sn, self._fw = self.id
        return self._fw

    @property
    def sn(self):
        """Get the serial number of the instrument."""
        if self._sn == "":
            self._manu, self._model, self._sn, self._fw = self.id
        return self._sn