# -*- coding: utf-8 -*-
"""
chemdataextractor.parse.battery_energy.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parser for energy.

"""

import re
import logging
from lxml import etree
import traceback

from . import R, I, W, Optional, merge, join
from .base import BaseSentenceParser
from ..utils import first
from .cem import cem, chemical_label, lenient_chemical_label, solvent_name
from .common import lbrct, dt, rbrct, comma
from .elements import W, I, R, T, Optional, Any, OneOrMore, Not, ZeroOrMore, SkipTo

log = logging.getLogger(__name__)

delim = R(r'^[:;\.,]$')

units = ((((W('Wh') | (W('W') + W('h'))) + R(r'^(k?g|m?(L|l))[\-–−]1$'))) | ((W('Wh') | (W('W') + W('h'))) + W('/') + R('^(k?g)|(L|l)$')))('units').add_action(merge)

joined_range = R(r'^[\+\-–−]?\d+(\.\\d+)?(\(\d\))?[\-––-−~∼˜]\d+(\.\d+)?(\(\d\))?$')('value').add_action(join)
spaced_range = (R(r'^[\+\-–−]?\d+(\.d+)?(\(\d\))?$') + Optional(units).hide() +
                (R(r'^[\-±–−~∼˜]$') + R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$') | R(r'^[\+\-–−]\d+(\.\d+)?(\(\d\))?$')))('value').add_action(join)
to_range = (R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$') + Optional(units).hide() + (I('to') + \
            R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$') | R(r'^[\+\-–−]\d+(\.\d+)?(\(\d\))?$')))('value').add_action(join)
and_range = (
    ZeroOrMore(R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$') + Optional(units).hide() + Optional(comma).hide()) +
    Optional(I('and') | comma).hide() + R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$'))('value').add_action(join)
range = (Optional(R(r'^[\-–−]$')) + (and_range | to_range | spaced_range | joined_range)).add_action(join)
value = (Optional(R(r'^[\-–−]$')) +
         Optional(R(r'^[~∼˜\<\>\≤\≥]$')) +
         Optional(R(r'^[\-\–\–\−±∓⨤⨦±]$')) +
         R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$')).add_action(join)
ordinal = T('JJ').add_action(join)
ener = (range | value | ordinal)('value')

cem_prefix = (
    Optional('oxidized') +
    cem('cem') +
    Optional(I('battery')) +
    Optional(delim).hide())
multi_cem = ZeroOrMore(cem_prefix + Optional(comma).hide()) + Optional(I('and') | comma).hide() + cem_prefix
ener_specifier = (I('energy') | I('energies') + Optional('density'))('specifier')

prefix = (
    Optional(I('the') | I('a') | I('an') | I('its') | I('with')).hide() +
    Optional(I('inherently')).hide() +
    Optional(I('excellent') | I('high') | I('low') | I('stable') | I('superior') | I('maximum') | I('highest')).hide() +
    Optional(I('initial')).hide() +
    ener_specifier +
    Optional(I('varies') + I('from')).hide() +
    Optional(W('=') | W('~') | W('≈') | W('≃') | I('of') | I('was') | I('is') | I('at') | I('as') | I('near') | I('above') | I('below')).hide() +
    Optional(I('reported') | I('determined') | I('measured') | I('calculated') | I('known')).hide() +
    Optional(I('as') | (I('to') + I('be'))).hide() +
    Optional( I('in') + I('the') + I('range') | I('ranging')).hide() +
    Optional(I('of')).hide() +
    Optional(I('about') | I('from') | I('approximately') | I('around') | (I('high') + I('as')) | (I('higher') | I('lower') + I('than')) | (I('up') + I('to') | I('in') + I('excess') + I('of'))).hide())


ener_and_units = (
    Optional(lbrct).hide() +
    ener +
    units +
    Optional(rbrct).hide())('ener')

ener_specifier_and_value = Optional(prefix) + (Optional(delim).hide() + Optional(
    lbrct | I('[')).hide() + ener + units + Optional(rbrct | I(']')).hide())('ener')

prefix_cem_value = (
    Optional(prefix).hide() +
    Optional(I('the') | I('a') | I('an') | I('these') | I('those') | I('this') | I('that')).hide() +
    (multi_cem | cem_prefix | lenient_chemical_label) +
    Optional(lbrct +Optional(cem_prefix | lenient_chemical_label | multi_cem) + rbrct) +
    Optional(I('is') | I('was') | I('were') | I('occurs') | I('of') | I('could') | I('can') | I('remained') | (I('can') + I('be') + I('assigned') + Optional(I('at') | I('to')))).hide() +
    Optional(I('reach') | I('reaching') | I('observed') | I('determined') | I('measured') | I('calculated') | I('found') | I('increased') | I('expected')).hide() +
    Optional(I('in') + I('the') + I('range') + I('of') | I('ranging') + I('from') | I('as') | I('to') | I('to') + I('be') | I('about') | I('over') | ( I('higher') | I('lower')) + I('than') | I('above')).hide() +
    Optional(lbrct).hide() + SkipTo((ener_specifier_and_value | ener_and_units) ) +
    (ener_specifier_and_value | ener_and_units) +
    Optional(rbrct).hide())('ener_phrase')

cem_prefix_value = (
    ((multi_cem | cem_prefix | lenient_chemical_label))
    + Optional(delim).hide()
    + Optional(I('that') | I('which') | I('was') | I('since') | I('the') | I('resulting') + I('in')).hide()
    + Optional(I('typically') | I('also')).hide()
    + Optional(prefix)
    + Optional(I('display') | I('displays') | I('exhibit') | I('exhibited') | I('exhibits') | I('exhibiting') | I('shows') | I('show') | I('showed') | I('gave') | I('demonstrate') | I('demonstrates') | I('are') | I('remains') | I('maintains') | I('delivered') | I('provided') |
               I('undergo') | I('undergoes') | I('has') | I('have') | I('having') | I('determined') | I('with') | I('where') | I('orders') | I('were') | (I('is') + Optional(I('classified') + I('as')))).hide()
    + Optional((I('reported') + I('to') + I('have')) | I('at') | I('with')).hide()
    + Optional(lbrct).hide()
    + (ener_specifier_and_value | ener_and_units) + Optional(rbrct).hide()
    + Optional(I('can') + I('be') + I('achieved'))
)('ener_phrase')

prefix_value_cem = (
    Optional(I('below') | I('at')).hide() +
    Optional(prefix).hide() +
    Optional(I('is') | I('were') | I('was') | I('are')).hide() +
    (ener_specifier_and_value | ener_and_units) +
    Optional(
        Optional(I('has') + I('been') + I('found')) +
        Optional(I('is') | I('were') | I('was') | I('are')) +
        Optional(I('observed') | I('determined') | I('measured') | I('calculated') | I('reported'))).hide() +
    Optional(ener_specifier_and_value | ener_and_units) +
    Optional(I('in') | I('for') | I('of')).hide() +
    Optional(I('the')).hide() +
    Optional(R('^[:;,]$')).hide() +
    Optional(lbrct).hide() +
    Optional(I('of')).hide() + SkipTo(multi_cem | cem_prefix | lenient_chemical_label) +
    (multi_cem | cem_prefix | lenient_chemical_label) +
    Optional(rbrct).hide())('ener_phrase')

value_prefix_cem = (Optional(I('of')).hide() +
                    (ener_specifier_and_value | ener_and_units) +
                    Optional(delim).hide() +
                    Optional(I('which') | I('that')).hide() +
                    Optional(I('has') +
                             I('been') | I('was') | I('is') | I('were')).hide() +
                    Optional(I('found') | I('observed') | I('measured') | I('calculated') | I('determined')).hide() +
                    Optional(I('likely') | I('close') | (I('can') +
                                                         I('be'))).hide() +
                    Optional(I('corresponds') | I('associated')).hide() +
                    Optional(I('to') +
                             I('be') | I('with') | I('is') | I('as')).hide() +
                    Optional(I('the')).hide() +
                    ener_specifier +
                    Optional(I('of') | I('in')).hide() +
                    (multi_cem | cem_prefix | lenient_chemical_label))('ener_phrase')

cem_value_prefix = ((multi_cem | cem_prefix | lenient_chemical_label)
                    + Optional((I('is') | I('was') | I('were')) + Optional(I('reported') | I('found') | I('calculate') | I('measured') | I('shown') | I('found')) + Optional(I('to'))).hide()
                    + Optional(I('display') | I('displays') | I('exhibit') | I('exhibits') | I('exhibiting') | I('shows') | I('show') | I('demonstrate') | I('demonstrates') |
                               I('undergo') | I('undergoes') | I('has') | I('have') | I('having') | I('determined') | I('with') | I('where') | I('orders') | (I('is') + Optional(I('classified') + I('as')))).hide()
                    + Optional(I('the') | I('a') | I('an')).hide()
                    + Optional(I('value') | I('values')).hide()
                    + Optional(I('varies') + I('from')).hide()
                    + Optional(W('=') | W('~') | W('≈') | W('≃') | I('was') | I('is') | I('at') | I('as') | I('near') | I('above') | I('below')).hide()
                    + Optional(I('in') + I('the') + I('range') | I('ranging')).hide()
                    + Optional(I('of') | I('about') | I('from') | I('approximately') | I('around') | (I('high') + I('as')) | (I('higher') | I('lower') + I('than'))).hide()
                    + (ener_specifier_and_value | ener_and_units)
                    + Optional(I('as') | I('of') | I('for')).hide()
                    + Optional(I('its') | I('their') | I('the')).hide() + ener_specifier)('ener_phrase')


bc = (
      value_prefix_cem
      | cem_value_prefix
      | cem_prefix_value
      | prefix_cem_value
      | prefix_value_cem
      )


def print_tree(trees):
    print(trees)
    try:
        print(etree.tostring(trees))
    except BaseException:
        print('no tree')


class EnergyParser(BaseSentenceParser):
    """"""
    root = bc

    def interpret(self, result, start, end):
        # try:
        compound = self.model.fields['compound'].model_class()
        raw_value = first(result.xpath('./ener/value/text()'))
        raw_units = first(result.xpath('./ener/units/text()'))
        try:
            specifier = ' '.join(
                [i for i in (first(result.xpath('./specifier'))).itertext()])
        except BaseException:
            specifier = ''
        # print_tree(first(result.xpath('.')))
        # sh-- If chemical names are not in the tree, don't select.
        # for child in (first(result.xpath('.'))).getchildren():
        #     if child.tag == 'cem':
        #         continue
        battery_energy= self.model(raw_value=raw_value,
                                      raw_units=raw_units,
                                      specifier=specifier,
                                      value=self.extract_value(raw_value),
                                      error=self.extract_error(raw_value),
                                      units=self.extract_units(raw_units),
                                      )
        cem_lists = []
        for cem_el in result.xpath('./cem'):
            # print_tree(cem_el)
            if cem_el is not None:
                log.debug(etree.tostring(cem_el))
                cem_lists.append(''.join(cem_el.xpath('./names/text()')))
            battery_energy.compound = compound
            battery_energy.compound.names = cem_lists
            battery_energy.compound.labels = cem_el.xpath('./labels/text()')
            log.debug(battery_energy.serialize())
        yield battery_energy
        # except TypeError as e:
        #     print('==========Error===============')
        #     traceback.print_exc()
        #     log.debug(e)
