# -*- coding: utf-8 -*-
"""

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Units and models for voltage.
Shu Huang
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .quantity_model import QuantityModel
from .unit import Unit
from .dimension import Dimension
from ...parse.elements import R
import logging
from .mass import Mass
from .length import Length
from .time import Time
from .current import ElectricalCurrent

log = logging.getLogger(__name__)


class Voltage(Dimension):
    """
    Dimension subclass for electrical current.
    """
    constituent_dimensions = Mass() * Length()**2 / ElectricalCurrent() / Time()**3


class VoltageModel(QuantityModel):
    """
    Model for electrical current.
    """
    dimensions = Voltage()


class VoltageUnit(Unit):
    """
    Base class for units with dimensions of electrical current.
    The standard value for current is defined to be an ampere, implemented in the Ampere class.
    """

    def __init__(self, magnitude=0.0, powers=None):
        super(VoltageUnit, self).__init__(Voltage(), magnitude, powers)


class Volt(VoltageUnit):
    """
    class for amps.
    """

    def convert_value_to_standard(self, value):
        return value

    def convert_value_from_standard(self, value):
        return value

    def convert_error_to_standard(self, error):
        return error

    def convert_error_from_standard(self, error):
        return error


class MilliVolt(VoltageUnit):
    """
    class for amps.
    """

    def convert_value_to_standard(self, value):
        return value *1000

    def convert_value_from_standard(self, value):
        return value /1000

    def convert_error_to_standard(self, error):
        return error *1000

    def convert_error_from_standard(self, error):
        return error /1000


units_dict = {R('(V|v)(olt(s)?)?', group=0): Volt,
              R('m(V|v)(olt(s)?)?',group=0): MilliVolt}
Voltage.units_dict = units_dict