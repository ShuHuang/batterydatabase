"""
Model classes for physical properties.

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import six

from .base import BaseModel, StringType, ListType, ModelType
from .units.length import LengthModel
from .units.battery_capacity import CapacityModel
from .units.battery_capacity_volume import VolumeCapacityModel
from .units.battery_conductivity import ConductivityModel
from .units.battery_coulombic import CoulombicModel
from .units.battery_voltage import VoltageModel
from .units.battery_energy import BatteryEnergyModel

from ..parse.cem import CompoundParser, CompoundHeadingParser, ChemicalLabelParser, names_only, labels_only, roles_only
from ..parse.elements import R, I, Optional, W
from ..parse.actions import merge, join
from ..model.units.quantity_model import QuantityModel, DimensionlessModel
from ..parse.auto import AutoTableParser, AutoSentenceParser
from ..parse.apparatus import ApparatusParser

from ..parse.battery_capacity import BcParser
from ..parse.battery_voltage import VoltageParser
from ..parse.battery_conductivity import ConductParser
from ..parse.battery_coulombic import CoulombicParser
from ..parse.battery_energy import EnergyParser

log = logging.getLogger(__name__)


class Compound(BaseModel):
    names = ListType(StringType(), parse_expression=names_only)
    labels = ListType(StringType(), parse_expression=labels_only)
    roles = ListType(StringType(), parse_expression=roles_only)
    parsers = [
        CompoundParser(),
        CompoundHeadingParser(),
        ChemicalLabelParser()]

    def merge(self, other):
        """Merge data from another Compound into this Compound."""
        log.debug('Merging: %s and %s' % (self.serialize(), other.serialize()))
        for k in self.keys():
            for new_item in other[k]:
                if new_item not in self[k]:
                    self[k].append(new_item)
        log.debug('Result: %s' % self.serialize())
        return self

    @property
    def is_unidentified(self):
        if not self.names and not self.labels:
            return True
        return False

    @property
    def is_id_only(self):
        """Return True if identifier information only."""
        for key, value in self.items():
            if key not in {'names', 'labels', 'roles'} and value:
                return False
        if self.names or self.labels:
            return True
        return False


class Apparatus(BaseModel):
    name = StringType()
    parsers = [ApparatusParser()]


class ElectrochemicalPotential(BaseModel):
    """An oxidation or reduction potential, from cyclic voltammetry."""
    value = StringType()
    units = StringType(contextual=True)
    type = StringType(contextual=True)
    solvent = StringType(contextual=True)
    concentration = StringType(contextual=True)
    concentration_units = StringType(contextual=True)
    temperature = StringType(contextual=True)
    temperature_units = StringType(contextual=True)
    apparatus = ModelType(Apparatus, contextual=True)


class InteratomicDistance(LengthModel):
    specifier_expression = (R('^bond$') + R('^distance')).add_action(merge)
    specifier = StringType(
        parse_expression=specifier_expression,
        required=False,
        contextual=True)
    rij_label = R(r'^((X|Ac|Ag|Al|Am|Ar|As|At|Au|B|Ba|Be|Bh|Bi|Bk|Br|C|Ca|Cd|Ce|Cf|Cl|Cm|Cn|Co|Cr|Cs|Cu|Db|Ds|Dy|Er|Es|Eu|F|Fe|Fl|Fm|Fr|Ga|Gd|Ge|H|He|Hf|Hg|Ho|Hs|I|In|Ir|K|Kr|La|Li|Lr|Lu|Lv|Mc|Md|Mg|Mn|Mo|Mt|N|Na|Nb|Nd|Ne|Nh|Ni|No|Np|O|Og|Os|P|Pa|Pb|Pd|Pm|Po|Pr|Pt|Pu|Ra|Rb|Re|Rf|Rg|Rh|Rn|Ru|S|Sb|Sc|Se|Sg|Si|Sm|Sn|Sr|Ta|Tb|Tc|Te|Th|Ti|Tl|Tm|Ts|U|V|W|Xe|Y|Yb|Zn|Zr)\-?(X|Ac|Ag|Al|Am|Ar|As|At|Au|B|Ba|Be|Bh|Bi|Bk|Br|C|Ca|Cd|Ce|Cf|Cl|Cm|Cn|Co|Cr|Cs|Cu|Db|Ds|Dy|Er|Es|Eu|F|Fe|Fl|Fm|Fr|Ga|Gd|Ge|H|He|Hf|Hg|Ho|Hs|I|In|Ir|K|Kr|La|Li|Lr|Lu|Lv|Mc|Md|Mg|Mn|Mo|Mt|N|Na|Nb|Nd|Ne|Nh|Ni|No|Np|O|Og|Os|P|Pa|Pb|Pd|Pm|Po|Pr|Pt|Pu|Ra|Rb|Re|Rf|Rg|Rh|Rn|Ru|S|Sb|Sc|Se|Sg|Si|Sm|Sn|Sr|Ta|Tb|Tc|Te|Th|Ti|Tl|Tm|Ts|U|V|W|Xe|Y|Yb|Zn|Zr))$')
    species = StringType(
        parse_expression=rij_label,
        required=True,
        contextual=False)
    compound = ModelType(Compound, required=True, contextual=True)
    another_label = StringType(
        parse_expression=R('^adgahg$'),
        required=False,
        contextual=False)


class CoordinationNumber(DimensionlessModel):
    # something like NTi-O will not work with this, only work if there is
    # space between the label and specifier
    coordination_number_label = R(r'^((X|Ac|Ag|Al|Am|Ar|As|At|Au|B|Ba|Be|Bh|Bi|Bk|Br|C|Ca|Cd|Ce|Cf|Cl|Cm|Cn|Co|Cr|Cs|Cu|Db|Ds|Dy|Er|Es|Eu|F|Fe|Fl|Fm|Fr|Ga|Gd|Ge|H|He|Hf|Hg|Ho|Hs|I|In|Ir|K|Kr|La|Li|Lr|Lu|Lv|Mc|Md|Mg|Mn|Mo|Mt|N|Na|Nb|Nd|Ne|Nh|Ni|No|Np|O|Og|Os|P|Pa|Pb|Pd|Pm|Po|Pr|Pt|Pu|Ra|Rb|Re|Rf|Rg|Rh|Rn|Ru|S|Sb|Sc|Se|Sg|Si|Sm|Sn|Sr|Ta|Tb|Tc|Te|Th|Ti|Tl|Tm|Ts|U|V|W|Xe|Y|Yb|Zn|Zr)\-?(X|Ac|Ag|Al|Am|Ar|As|At|Au|B|Ba|Be|Bh|Bi|Bk|Br|C|Ca|Cd|Ce|Cf|Cl|Cm|Cn|Co|Cr|Cs|Cu|Db|Ds|Dy|Er|Es|Eu|F|Fe|Fl|Fm|Fr|Ga|Gd|Ge|H|He|Hf|Hg|Ho|Hs|I|In|Ir|K|Kr|La|Li|Lr|Lu|Lv|Mc|Md|Mg|Mn|Mo|Mt|N|Na|Nb|Nd|Ne|Nh|Ni|No|Np|O|Og|Os|P|Pa|Pb|Pd|Pm|Po|Pr|Pt|Pu|Ra|Rb|Re|Rf|Rg|Rh|Rn|Ru|S|Sb|Sc|Se|Sg|Si|Sm|Sn|Sr|Ta|Tb|Tc|Te|Th|Ti|Tl|Tm|Ts|U|V|W|Xe|Y|Yb|Zn|Zr))$')
    # specifier = (R('^(N|n|k)$') | (I('Pair') + I('ij')).add_action(merge)
    specifier_expression = R('^(N|n|k)$')
    specifier = StringType(
        parse_expression=specifier_expression,
        required=True,
        contextual=True)

    cn_label = StringType(
        parse_expression=coordination_number_label,
        required=True,
        contextual=True)
    compound = ModelType(Compound, required=True, contextual=True)


class CNLabel(BaseModel):
    # separate model to test automated parsing for stuff that are not
    # quantities
    coordination_number_label = R(r'^((X|Ac|Ag|Al|Am|Ar|As|At|Au|B|Ba|Be|Bh|Bi|Bk|Br|C|Ca|Cd|Ce|Cf|Cl|Cm|Cn|Co|Cr|Cs|Cu|Db|Ds|Dy|Er|Es|Eu|F|Fe|Fl|Fm|Fr|Ga|Gd|Ge|H|He|Hf|Hg|Ho|Hs|I|In|Ir|K|Kr|La|Li|Lr|Lu|Lv|Mc|Md|Mg|Mn|Mo|Mt|N|Na|Nb|Nd|Ne|Nh|Ni|No|Np|O|Og|Os|P|Pa|Pb|Pd|Pm|Po|Pr|Pt|Pu|Ra|Rb|Re|Rf|Rg|Rh|Rn|Ru|S|Sb|Sc|Se|Sg|Si|Sm|Sn|Sr|Ta|Tb|Tc|Te|Th|Ti|Tl|Tm|Ts|U|V|W|Xe|Y|Yb|Zn|Zr)\-?(X|Ac|Ag|Al|Am|Ar|As|At|Au|B|Ba|Be|Bh|Bi|Bk|Br|C|Ca|Cd|Ce|Cf|Cl|Cm|Cn|Co|Cr|Cs|Cu|Db|Ds|Dy|Er|Es|Eu|F|Fe|Fl|Fm|Fr|Ga|Gd|Ge|H|He|Hf|Hg|Ho|Hs|I|In|Ir|K|Kr|La|Li|Lr|Lu|Lv|Mc|Md|Mg|Mn|Mo|Mt|N|Na|Nb|Nd|Ne|Nh|Ni|No|Np|O|Og|Os|P|Pa|Pb|Pd|Pm|Po|Pr|Pt|Pu|Ra|Rb|Re|Rf|Rg|Rh|Rn|Ru|S|Sb|Sc|Se|Sg|Si|Sm|Sn|Sr|Ta|Tb|Tc|Te|Th|Ti|Tl|Tm|Ts|U|V|W|Xe|Y|Yb|Zn|Zr))$')
    specifier = (I('Pair') + I('ij')).add_action(merge)
    label_Juraj = StringType(parse_expression=coordination_number_label)
    compound = ModelType(Compound, required=False)
    parsers = [AutoSentenceParser(), AutoTableParser()]


class BatteryCapacity(CapacityModel):
    value = StringType(contextual=False, required=True)
    units = StringType(contextual=False, required=True)
    specifier = StringType(contextual=False)
    current_value = StringType(contextual=False)
    current_value1 = StringType(contextual=False)
    current_units = StringType(contextual=False)
    cycle_value = StringType(contextual=False)
    cycle_units = StringType(contextual=False)
    compound = ModelType(Compound, contextual=False)
    parsers = [BcParser()]


class BatteryConductivity(ConductivityModel):
    value = StringType(contextual=False, required=True)
    units = StringType(contextual=False, required=True)
    specifier = StringType(contextual=False)
    compound = ModelType(Compound, contextual=False)
    parsers = [ConductParser()]


class BatteryCoulombic(CoulombicModel):
    value = StringType(contextual=False, required=True)
    units = StringType(contextual=False, required=True)
    specifier = StringType(contextual=False)
    compound = ModelType(Compound, contextual=False)
    parsers = [CoulombicParser()]


class BatteryEnergy(BatteryEnergyModel):
    value = StringType(contextual=False, required=True)
    units = StringType(contextual=False, required=True)
    specifier = StringType(contextual=False)
    compound = ModelType(Compound, contextual=False)
    parsers = [EnergyParser()]


class BatteryVoltage(VoltageModel):
    value = StringType(contextual=False, required=True)
    units = StringType(contextual=False, required=True)
    specifier = StringType(contextual=False)
    compound = ModelType(Compound, contextual=False)
    parsers = [VoltageParser()]
