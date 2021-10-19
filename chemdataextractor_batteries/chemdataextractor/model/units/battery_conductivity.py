# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Units and models for conductivity.

SHu Huang
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
from .conductivity import Conductivitya
from .length import Length

log = logging.getLogger(__name__)


class Conductivity(Dimension):
    """
    Dimension subclass for electrical current.
    """
    constituent_dimensions = Conductivitya() / Length()


class ConductivityModel(QuantityModel):
    """
    Model for electrical current.
    """
    dimensions = Conductivity()


class ConductivityUnit(Unit):
    """
    Base class for units with dimensions of electrical current.
    The standard value for current is defined to be an ampere, implemented in the Ampere class.
    """

    def __init__(self, magnitude=0.0, powers=None):
        super(ConductivityUnit, self).__init__(Conductivity(), magnitude, powers)


class ConductivityUnits(ConductivityUnit):
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



units_dict = {R(r'S/m', group=0): ConductivityUnits}
ConductivityUnit.units_dict = units_dict