# -*- coding: utf-8 -*-
"""
Springer web-scraper. PLEASE use your own API key.
"""

__author__ = "Shu Huang"
__email__ = "sh2009@cam.ac.uk"

import urllib.request as request
import json


class SpringerScraper():
    def __init__(
            self,
            query_text,
            start=0,
            year=2021,
            apikey="APIKEY",
            max_return=100):
        """
        :param query_text: query words
        :param start: start page number
        :param year: year of published papers
        :param apikey: Springer APIKEY
        :param max_return: max returned number of papers
        """
        self.apikey = apikey
        self.start = start
        self.max_return = max_return
        self.year = year
        self.query_text = query_text.replace(" ", '%20')

    def FindDois(self):
        """
        :return: <list> of <str> list of DOIs
        """
        url = "http://api.springernature.com/meta/v2/json?&q={}%20type:Journal%20year:{}&s={}&p={}&api_key={}".format(
            self.query_text, self.year, self.start, self.max_return, self.apikey)
        crawl_content = request.urlopen(url).read()
        Content = json.loads(crawl_content.decode('utf8'))
        Dois = []
        for i in range(self.max_return):
            Dois.append(Content['records'][i]['doi'])
        return Dois

    def FindingXml(self, papers):
        """
        :param papers: list of DOIS
        :return: url addresses of papers
        """
        DoiUrls = []
        for doi in papers:
            doiUrls = "https://api.springernature.com/meta/v2/pam?q=doi:{}&p=2&api_key={}".format(
                doi, self.apikey)
            DoiUrls.append(doiUrls)
        return DoiUrls


def download_doi(doi):
    """
    :param doi: DOI
    :return:
    """
    WebContent = request.urlopen(doi).read()
    with open(r'springer_{}.xml'.format(doi), 'wb') as f:
        f.write(WebContent)
        f.close()
    return
