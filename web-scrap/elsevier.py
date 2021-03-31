# -*- coding: utf-8 -*-
"""
Elsevier web-scraper. PLEASE use your own API key.
"""

__author__ = "Shu Huang"
__email__ = "sh2009@cam.ac.uk"

import json
import requests
import numpy as np

API_KEY = "example"
query = "battery materials"
base_url = 'https://api.elsevier.com/content/search/sciencedirect'

data = {"qs": query,
        "date": 2021,
        # "volume": 0,
        "display": {
            "show": 10,
            "offset": 0
        }}

headers = {'x-els-apikey': API_KEY,
           'Content-Type': 'application/json',
           'Accept': 'application/json'}


def get_response(url, data, headers):
    """
    Return the response from Elsevier
    :param url: <str> base_url
    :param data: <dict> data parameters
    :param headers: <dict> headers
    :return: response
    """
    response = requests.put(url, data=json.dumps(data), headers=headers)
    response = response.text.replace('false', 'False').replace('true', 'True')
    try:
        response = eval(response)
    except BaseException:
        print(response)
    return response


def get_doi(data, volume, year):
    """
    Get DOIs
    :param data: <dict> data parameters
    :param volume: <int> the volume index
    :param year: <int> the year index
    :return: <list> of <str> list of DOIs
    """
    dois = []
    data['volume'] = volume
    data["date"] = year
    response = get_response(base_url, data, headers)
    if 'resultsFound' in response.keys():
        n = int(np.ceil(response['resultsFound'] / 100))
    else:
        n = 60
    for offset in range(n + 1):
        data["display"]["offset"] = offset
        response = get_response(base_url, data, headers)
        if 'results' in response.keys():
            results = response['results']
            for result in results:
                if 'doi' in result:
                    dois.append(result['doi'])
    return dois


def download_doi(doi):
    """
    Download the paper according to the DOI
    :param doi: <str> DOI
    """
    with open(str(doi) + '.xml', 'w', encoding='utf-8') as f:
        request_url = 'https://api.elsevier.com/content/article/doi/{}?apiKey={}&httpAccept=text%2Fxml'.format(
            doi, API_KEY)
        text = requests.get(request_url).text
        f.write(text)
    return
