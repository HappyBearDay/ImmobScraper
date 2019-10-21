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

# User agent for not being a robot
headers = {'User-Agent': '*',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'fr-FR,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate',
           'Connection': 'keep-alive',
           'Upgrade-Insecure-Requests': '1'}

logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger()


class Scraper():
    def __init__(self, url, page_suffix):
        self.logger = logging.getLogger()
        self.headers = headers
        self.url = url
        self.page_suffix = page_suffix

    def reach_website(self, url, headers):
        # Create a session for the website
        s = requests.Session()
        s.headers.update(headers)

        r = s.get(url)
        if r.status_code == 200:
            self.logger.info("WebSite reached")
            return r
        else:
            logging.error(f"WebSite unreachable, response : {r.text}")
            return None

    def find_scripts_on_page(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        self.logger.debug(f"Raw Soup {soup}")

        script_list = soup.find_all('script')
        self.logger.debug(f"Script list {script_list}")

        return script_list

    ## TO OVERLOAD ##
    def find_json_in_scripts(self, script_list):
        self.logger.critical("TO OVERLOAD")

        for script_item in script_list:
            if 'BALISE' in script_item.text:
                json_data = None  ## To replace

                return json_data

        logging.error("No BALISE on loaded Page")
        return None

    ## / TO OVERLOAD ##
    def get_appt_list(self, json_data):
        self.logger.critical("TO OVERLOAD")

        tmp_list_appt_1 = json_data['ads']
        tmp_list_appt_2 = json_data['ads_alu']
        tmp_list_appt = tmp_list_appt_1 + tmp_list_appt_2
        self.logger.debug(f"List appt : {pformat(tmp_list_appt)} ")

        # list_appt = list(filter(lambda x: x['publicationId'] is not None, list(tmp_list_appt)))

        return tmp_list_appt

    def show_data(self, data):
        df = pd.DataFrame(data)
        self.logger.debug(f" Data Frame : {df}")

        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None):  # more options can be specified also
            print(df)

    def get_appt_from_url(self, url):
        response = self.reach_website(url, headers)
        script_list = self.find_scripts_on_page(response)
        json_data = self.find_json_in_scripts(script_list)
        list_appt = self.get_appt_list(json_data)
        self.logger.info(f"Added {len(list_appt)} appartements.")

        return list_appt, json_data

    def get_full_list_appt(self):
        logger.info(f"Page scrapped : 1")
        list_appt, json_data = self.get_appt_from_url(self.url)

        logger.info(f"Total appartement scrapped {len(list_appt)} appartements.")
        self.show_data(list_appt)


if __name__ == '__main__':
    scraper = Scraper('https://None.fr', '&page=')
    scraper.get_full_list_appt()
