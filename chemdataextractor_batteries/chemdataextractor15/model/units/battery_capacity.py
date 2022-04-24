# -*- coding: utf-8 -*-
"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Units and models for capacity.

Shu Huang (sh2009@cam.ac.uk)

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .quantity_model import QuantityModel
from .unit import Unit
from .dimension import Dimension
from .mass import Mass
from .current import ElectricalCurrent
from .length import Length
from .time import Time
from ...parse.elements import W, I, R, Optional, Any, OneOrMore, Not, ZeroOrMore
from ...parse.actions import merge, join
import logging

log = logging.getLogger(__name__)


class Capacity(Dimension):
    constituent_dimensions = ElectricalCurrent() * Time() / Mass()


class CapacityModel(QuantityModel):

    dimensions = Capacity()


class CapacityUnit(Unit):

    def __init__(self, magnitude=0.0, powers=None):
        super(CapacityUnit, self).__init__(Capacity(), magnitude, powers)


class CapacityUnits(CapacityUnit):

    def convert_value_to_standard(self, value):
        return value

    def convert_value_from_standard(self, value):
        return value

    def convert_error_to_standard(self, error):
        return error

    def convert_error_from_standard(self, error):
        return error



#units_dict = {(((R('mA') + R('h'))|R('mAh')) + (R(r'^g.*[\-–−]1$')|(R(r'/') + R('g')))): CapacityUnits}
units_dict = {R(r'mAh/g', group=0): CapacityUnits,
              R(r'mAhg-1', group=0): CapacityUnits}
Capacity.units_dict.update(units_dict)
