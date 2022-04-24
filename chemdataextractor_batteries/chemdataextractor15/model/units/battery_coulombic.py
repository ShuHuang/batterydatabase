# -*- coding: utf-8 -*-
"""

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Units and models for coulombic effiency.
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

log = logging.getLogger(__name__)


class Coulombic(Dimension):
    """
    Dimension subclass for electrical current.
    """
    pass


class CoulombicModel(QuantityModel):
    """
    Model for electrical current.
    """
    dimensions = Coulombic()


class CoulombicUnit(Unit):
    """
    Base class for units with dimensions of electrical current.
    The standard value for current is defined to be an ampere, implemented in the Ampere class.
    """

    def __init__(self, magnitude=0.0, powers=None):
        super(CoulombicUnit, self).__init__(Coulombic(), magnitude, powers)


class Percent(CoulombicUnit):
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


units_dict = {R('%', group=0): Percent}
Coulombic.units_dict = units_dict