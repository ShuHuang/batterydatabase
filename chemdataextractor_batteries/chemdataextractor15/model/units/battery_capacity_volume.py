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


class VolumeCapacity(Dimension):
    constituent_dimensions = ElectricalCurrent() * Time() / Length()**3


class VolumeCapacityModel(QuantityModel):

    dimensions = VolumeCapacity()


class VolumeCapacityUnit(Unit):

    def __init__(self, magnitude=0.0, powers=None):
        super(VolumeCapacityUnit, self).__init__(VolumeCapacity(), magnitude, powers)


class VolumeCapacityUnits(VolumeCapacityUnit):

    def convert_value_to_standard(self, value):
        return value

    def convert_value_from_standard(self, value):
        return value

    def convert_error_to_standard(self, error):
        return error

    def convert_error_from_standard(self, error):
        return error



units_dict = {R(r'mAh/g', group=0): VolumeCapacityUnits,
              R(r'mAhg-1', group=0): VolumeCapacityUnits}
VolumeCapacity.units_dict.update(units_dict)
