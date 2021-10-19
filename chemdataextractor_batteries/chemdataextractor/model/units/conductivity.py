# -*- coding: utf-8 -*-
"""

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Units and models for conductivity.
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


class Conductivitya(Dimension):
    """
    Dimension subclass for electrical current.
    """
    constituent_dimensions = Time()**3 * ElectricalCurrent()**2 / Mass() / Length()**2


class ConductivityaModel(QuantityModel):
    """
    Model for electrical current.
    """
    dimensions = Conductivitya()


class ConductivityaUnit(Unit):
    """
    Base class for units with dimensions of electrical current.
    The standard value for current is defined to be an ampere, implemented in the Ampere class.
    """

    def __init__(self, magnitude=0.0, powers=None):
        super(ConductivityaUnit, self).__init__(Conductivitya(), magnitude, powers)


class Siemens(ConductivityaUnit):
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


class MilliSiemens(ConductivityaUnit):
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

units_dict = {R('(S|s)(iemen(s)?)?', group=0): Siemens,
              R('m(S|s)(iemen(s)?)?',group=0): MilliSiemens}
Conductivitya.units_dict = units_dict