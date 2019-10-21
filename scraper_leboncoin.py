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
url = 'PUT HERE SEARCH URL'
page_add = '&page='  # '&page=2'

# User agent for not being a robot
headers = {'User-Agent': '*',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'fr-FR,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1'}

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()


def reach_website(url, headers):
    # Create a session for the website
    s = requests.Session()
    s.headers.update(headers)

    r = s.get(url)
    if r.status_code == 200:
        logger.info("WebSite reached")
        return r
    else:
        logging.error(f"WebSite unreachable : {r.text}")
        return None


def parse_reponse(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    logger.debug(f"Raw Soup {soup}")

    script_list = soup.find_all('script')
    logger.debug(f"Script list {script_list}")

    for script_item in script_list:
        if 'window.__REDIAL_PROPS__' in script_item.text:
            logger.debug(f"script_item window.__REDIAL_PROPS__ : {pformat(script_item.text)} ")

            string_data = script_item.text.split('=', 1)[1][4]
            json_data = json.loads(string_data)
            logger.debug(f"Raw JSON : {pformat(json_data)} ")

            return json_data

    logging.error("Non __REDIAL_PROPS__ on loaded Page")
    return None


def get_appt_list(json_data):
    tmp_list_appt_1 = json_data['ads']
    tmp_list_appt_2 = json_data['ads_alu']
    tmp_list_appt = tmp_list_appt_1 + tmp_list_appt_2
    logger.debug(f"List appt : {pformat(tmp_list_appt)} ")

    # list_appt = list(filter(lambda x: x['publicationId'] is not None, list(tmp_list_appt)))

    return tmp_list_appt

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

    logger.info(f"Total appartement scrapped {len(list_appt)} appartements.")
    show_data(list_appt)

