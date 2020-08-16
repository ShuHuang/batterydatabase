# -*- coding: utf-8 -*-
"""
chemdataextractor.parse.battery_voltage.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parser for voltage.

"""

import logging
from lxml import etree
import traceback

from . import R, I, W, T, Optional, merge, join, Any, OneOrMore, Not, ZeroOrMore, SkipTo
from .base import BaseParser
from ..utils import first
from .cem import cem, chemical_label, lenient_chemical_label, solvent_name
from .common import lbrct, dt, rbrct, comma
from ..model import BatteryVoltage, Compound
from .extract import extract_value, extract_volt_units

log = logging.getLogger(__name__)

delim = R(r'^[:;\.,]$')

units = (R('^m?V$')('units') +
         Optional(Optional(lbrct).hide() +
                  R('^v(s(.)?|ersus)$') +
                  Optional(R('Li|Na|Ag|K')) +
                  Optional(cem) +
                  Optional(rbrct).hide())('vs') +
         Not(Optional(R('/')) + R('s')) +
         Not(I('dec−1')) +
         Not(I('per'))
         ).add_action(join)

joined_range = R(r'^[\+\-–−]?\d+(\.\\d+)?(\(\d\))?[\-––-−~∼˜]\d+(\.\d+)?(\(\d\))?$')('value').add_action(join)
spaced_range = (R(r'^[\+\-–−]?\d+(\.d+)?(\(\d\))?$') + Optional(units).hide() + (R(r'^[\-±–−~∼˜]$') + R(
    r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$') | R(r'^[\+\-–−]\d+(\.\d+)?(\(\d\))?$')))('value').add_action(join)
to_range = (ZeroOrMore(R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$') + Optional(units).hide()) +
    Optional(I('to')) + R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$'))('value').add_action(join)
and_range = (ZeroOrMore(R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$') + Optional(units).hide() + Optional(comma)) +
    Optional(I('and') | comma) + R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$'))('value').add_action(join)
range = (Optional(R(r'^[\-–−]$')) + (and_range | to_range | spaced_range | joined_range)).add_action(join)
value = (Optional(R(r'^[\-–−]$')) +
         Optional(R(r'^[~∼˜\<\>\≤\≥]$')) +
         Optional(R(r'^[\-\–\–\−±∓⨤⨦±]$')) +
         R(r'^[\+\-–−]?\d+(\.\d+)?(\(\d\))?$')).add_action(join)
ordinal = T('JJ').add_action(join)
power = (Optional((range | value) + R('×')) + (R('10') + W('−') + R(r'\d') | R(r'^10[\-–−]?\d+$'))).add_action(join)
volt = (power | range | value | ordinal)('value')

cem_prefix = (
    Optional(I('oxidized')).hide() + Optional(I('the')).hide() +
    cem('cem') +
    Optional(I('battery')).hide() + Optional(I('couple')).hide() +
    Optional(delim).hide())
multi_cem = ZeroOrMore(cem_prefix + Optional(comma).hide()) + Optional(I('and') | comma).hide() + cem_prefix

volt_specifier = (Optional(I('electronic') | I('electrical')).hide() + (I('voltage') | I('potential') | I('voltages') ))('specifier')

prefix = (
    Optional(I('the') | I('a') | I('an') | I('its') | I('with')).hide() +
    Optional(I('inherently')).hide() +
    Optional(I('excellent') | I('high') | I('low') | I('stable') | I('superior') | I('maximum') | I('highest') | I('peak')).hide() +
    Optional(I('initial')).hide() +
    volt_specifier +
    Optional(I('seperation')).hide() +
    Optional(I('varies') + I('from')).hide() +
    Optional(W('=') | W('~') | W('≈') | W('≃') | I('of') | I('was') | I('is') | I('at') | I('as') | I('near') | I('above') | I('below')).hide() +
    Optional(I('reported') | I('determined') | I('measured') | I('calculated') | I('known')).hide() +
    Optional(I('as') | (I('to') + I('be'))).hide() +
    Optional(I('in') + I('the') + I('range') | I('ranging')).hide() +
    Optional(I('of')).hide() +
    Optional(I('about') | I('from') | I('approximately') | I('around') | ( I('high') + I('as')) | ( I('higher') | I('lower') + I('than')) | ( I('up') + I('to') | I('in') + I('excess') + I('of'))).hide())

volt_and_units = (
    Optional(lbrct).hide() +
    volt + units +
    Optional(rbrct).hide())('volt')

volt_specifier_and_value = Optional(prefix) + (Optional(delim).hide() + Optional(
    lbrct | I('[')).hide() + volt + units + Optional(rbrct | I(']')).hide())('volt')

prefix_cem_value = (
    prefix +
    Optional(I('the') | I('a') | I('an') | I('these') | I('those') | I('this') | I('that')).hide() +
    SkipTo((multi_cem | cem_prefix | lenient_chemical_label)) +
    (multi_cem | cem_prefix | lenient_chemical_label) +
    Optional(lbrct + Optional(cem_prefix | lenient_chemical_label | multi_cem) + rbrct) +
    Optional(I('is') | I('was') | I('were') | I('occurs') | I('of') | I('could') | I('can') | I('remained') | (
            I('can') + I('be') + I('assigned') + Optional( I('at') | I('to')))).hide() +
    Optional(I('reach') | I('reaching') | I('observed') | I('determined') | I('measured') | I('calculated') | I('found') | I('increased') | I('expected')| I('decreases')).hide() +
    Optional(I('in') + I('the') + I('range') + I('of') | I('ranging') + I('from') | I('as') | I('to') | I('from')| I('to') + I('be') | I('about') | I('over') | (I('higher') | I('lower')) + I('than') | I('above')).hide() +
    Optional(lbrct).hide() + SkipTo((volt_specifier_and_value | volt_and_units)) +
    (volt_specifier_and_value | volt_and_units) + Optional(rbrct).hide())('volt_phrase')

cem_prefix_value = (
    ((multi_cem | cem_prefix | lenient_chemical_label))
    + Optional(delim).hide()
    + Optional(I('that') | I('which') | I('was') | I('since') | I('the') | I('resulting') + I('in')).hide()
    + Optional(I('typically') | I('also')).hide()
    + Optional(prefix)
    + Optional(I('display') | I('displays') | I('exhibit') | I('exhibited') | I('exhibits') | I('exhibiting') | I('shows') | I('show') | I('showed') | I('gave') | I('demonstrate') | I('demonstrates') | I('are') | I('remains') | I('maintains') | I('delivered') | I('provided') |
               I('undergo') | I('undergoes') | I('has') | I('have') | I('having') | I('determined') | I('with') | I('where') | I('orders') | I('were') | (I('is') + Optional(I('classified') + I('as')))).hide()
    + Optional((I('reported') + I('to') + I('have')) | I('at') | I('with')).hide()
    + Optional(lbrct).hide() + (volt_specifier_and_value | volt_and_units) + Optional(rbrct).hide()
    + Optional(I('can') + I('be') + I('achieved'))
)('volt_phrase')

prefix_value_cem = (
    Optional(I('below') | I('at')).hide() +
    (prefix) +
    Optional(I('is') | I('were') | I('was') | I('are')).hide() + SkipTo((volt_specifier_and_value | volt_and_units)) +
    (volt_specifier_and_value | volt_and_units) +
    Optional(
        Optional(I('has') + I('been') + I('found')) +
        Optional(I('is') | I('were') | I('was') | I('are')) +
        Optional(I('observed') | I('determined') | I('measured') | I('calculated') | I('reported'))).hide() +
    Optional(volt_specifier_and_value | volt_and_units) +
    Optional(I('in') | I('for') | I('of')).hide() +
    Optional(I('the')).hide() +
    Optional(R('^[:;,]$')).hide() +
    Optional(lbrct).hide() +
    Optional(I('of')).hide() +
    SkipTo((multi_cem | cem_prefix | lenient_chemical_label)) +
    (multi_cem | cem_prefix | lenient_chemical_label) +
    Optional(rbrct).hide())('volt_phrase')

value_prefix_cem = (Optional(I('of')) +
                    (volt_specifier_and_value | volt_and_units) +
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
                    volt_specifier +
                    Optional(I('of') | I('in')).hide() +
                    (multi_cem | cem_prefix | lenient_chemical_label))('volt_phrase')

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
                    + (volt_specifier_and_value | volt_and_units)
                    + Optional(I('as') | I('of') | I('for')).hide()
                    + Optional(I('its') | I('their') | I('the')).hide() + volt_specifier)('volt_phrase')

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


class VoltageParser(BaseParser):
    """"""
    root = bc

    def interpret(self, result, start, end):
        #print(etree.tostring(result))
        #print (result.tag)
        raw_value = first(result.xpath('./volt/value/text()'))
        raw_units = first(result.xpath('./volt/units/text()'))
        try:
            specifier = ' '.join(
                [i for i in (first(result.xpath('./specifier'))).itertext()])
        except BaseException:
            specifier = ''

        battery_voltage = Compound(
            voltages=[
                BatteryVoltage(
                    raw_value=raw_value,
                    raw_units=raw_units,
                    specifier=specifier,
                    value=extract_value(raw_value),
                    units=extract_volt_units(raw_units),
                )
            ]
        )

        cem_el = first(result.xpath('./cem'))
        if cem_el is not None:
            battery_voltage.names = cem_el.xpath('./name/text()')
            battery_voltage.labels = cem_el.xpath('./label/text()')
        yield battery_voltage