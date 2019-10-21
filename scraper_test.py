import requests
import pprint
from pprint import pformat
from bs4 import BeautifulSoup
import json
import pandas as pd
import logging
import matplotlib.pyplot as plt
import numpy as np
import math

# Search URL
url = 'PUT HERE RESEARCH STRING URL'
page_add = '&LISTING-LISTpg='  # '&LISTING-LISTpg=2'

# User agent for not being a robot
headers = {'User-Agent': '*',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'en-US,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1'}

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()


def reach_website(url, headers):
    # Create a session for the website
    s = requests.Session()
    s.headers.update(headers)
    # s.get('http://www.seloger.com/')

    r = s.get(url)
    if r.status_code == 200:
        logger.info("WebSite reached")
        return r
    else:
        logging.error("WebSite unreachable")
        return None


def parse_reponse(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    logger.debug(f"Raw Soup {soup}")

    script_list = soup.find_all('script')
    logger.debug(f"Script list {script_list}")

    for script_item in script_list:
        if 'initialData' in script_item.text:
            logger.debug(f"script_item initalData : {pformat(script_item.text)} ")

            string_data = script_item.text.split('=', 1)[1].split(";window.tags", 1)[0]
            json_data = json.loads(string_data)
            logger.debug(f"Raw JSON : {pformat(json_data)} ")

            return json_data

    logging.error("Non initialData on loaded Page")
    return None


def get_appt_list(json_data):
    tmp_list_appt = json_data['cards']["list"]
    logger.debug(f"List appt : {pformat(tmp_list_appt)} ")

    # list_appt = list(filter(lambda x: x['publicationId'] is not None, list(tmp_list_appt)))

    return tmp_list_appt


def get_nb_pages(json_data):
    logger.debug(json_data['pagination'])

    nbResults = json_data['pagination']["count"]
    resultsPerPage = json_data['pagination']["resultsPerPage"]
    nbPages = math.ceil(nbResults / resultsPerPage)
    logger.info(f"Total number of results : {nbResults}")
    logger.info(f"Results per page : {resultsPerPage}")
    logger.info(f"Nb of pages to scrap : {nbPages}")

    return nbPages



def show_data(data):
    df = pd.DataFrame(data)
    logger.debug(f" Data Frame : {df}")

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)


def get_app_from_url(url):
    response = reach_website(url, headers)
    json_data = parse_reponse(response)
    list_appt = get_appt_list(json_data)
    logger.info(f"Added {len(list_appt)} appartements.")

    return list_appt, json_data


if __name__ == '__main__':

    logger.info(f"Page scrapped : 1")
    list_appt, json_data = get_app_from_url(url)
    nb_pages = get_nb_pages(json_data)

    for page in range(2, nb_pages + 1):
        logger.info(f"Page scrapped : {page}")

        tmp_list_appt, _ = get_app_from_url(url + page_add + str(page))
        list_appt += tmp_list_appt

    logger.info(f"Total appartement scrapped {len(list_appt)} appartements.")
    show_data(list_appt)

