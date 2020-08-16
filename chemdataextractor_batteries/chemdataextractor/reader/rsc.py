# -*- coding: utf-8 -*-
"""
Readers for documents from the RSC.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import logging

from ..doc.text import Footnote, Caption
from ..scrape.pub.rsc import replace_rsc_img_chars
from ..scrape.clean import clean, Cleaner
from .markup import HtmlReader
from lxml import etree

log = logging.getLogger(__name__)

# XML stripper that removes the tags around numbers in chemical formulas
strip_rsc_html = Cleaner(strip_xpath='.//b')


def rsc_html_whitespace(document):
    """ Remove whitespace in xml.text or xml.tails for all elements, if it is only whitespace """
    # selects all tags and checks if the text or tail are spaces
    for el in document.xpath('//*'):
        if el.tag == 'b':
            continue
        if str(el.text).isspace():
            el.text = ''
        if str(el.tail).isspace():
            el.tail = ''
        if el.text:
            el.text = el.text.replace('\n', ' ')
    return document


class RscHtmlReader(HtmlReader):
    """Reader for HTML documents from the RSC."""

    cleaners = [clean, rsc_html_whitespace, replace_rsc_img_chars, strip_rsc_html]

    root_css = 'html'
    title_css = 'h1, .title_heading'
    heading_css = 'h2, h3, h4, h5, h6, .a_heading, .b_heading, .c_heading, .c_heading_indent, .d_heading, .d_heading_indent'
    citation_css = 'span[id^="cit"]'
    reference_css = 'small sup a, a[href^="#cit"], a[href^="#fn"], a[href^="#tab"]'
    figure_css = '.image_table'
    figure_caption_css = '.graphic_title'
    ignore_css = '.table_caption + table, .left_head, sup span.sup_ref, small sup a, a[href^="#fn"], .PMedLink'


    def detect(self, fstring, fname=None):
        """"""
        if fname and not (fname.endswith('.html') or fname.endswith('.htm')):
            return False
        if b'meta name="citation_doi" content="10.1039' in fstring:
            return True
        return False