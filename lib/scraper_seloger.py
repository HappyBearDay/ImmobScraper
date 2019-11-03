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
from VirtualScraper import Scraper
from Parameters import url_seloger, page_add_seloger


class SeLoger_Scraper(Scraper):
    def find_json_in_scripts(self, script_list):
        for script_item in script_list:
            if 'initialData' in script_item.text:
                self.logger.debug(f"script_item initalData : {pformat(script_item.text)} ")

                string_data = script_item.text.split('=', 1)[1].split(";window.tags", 1)[0]
                json_data = json.loads(string_data)
                self.logger.debug(f"Raw JSON : {pformat(json_data)} ")

                return json_data

        logging.error("Non initialData on loaded Page")
        return None

    def get_appt_list(self, json_data):
        tmp_list_appt = json_data['cards']["list"]
        self.logger.debug(f"List appt : {pformat(tmp_list_appt)} ")

        # list_appt = list(filter(lambda x: x['publicationId'] is not None, list(tmp_list_appt)))

        return tmp_list_appt

    def get_nb_pages(self, json_data):
        self.logger.debug(json_data['pagination'])

        nbResults = json_data['pagination']["count"]
        resultsPerPage = json_data['pagination']["resultsPerPage"]
        nbPages = math.ceil(nbResults / resultsPerPage)
        self.logger.info(f"Total number of results : {nbResults}")
        self.logger.info(f"Results per page : {resultsPerPage}")
        self.logger.info(f"Nb of pages to scrap : {nbPages}")

        return nbPages

    def get_full_list_appt(self):
        self.logger.info(f"Page scrapped : 1")
        list_appt, json_data = self.get_appt_from_url(self.url)
        nb_pages = self.get_nb_pages(json_data)

        for page in range(2, nb_pages + 1):
            self.logger.info(f"Page scrapped : {page}")

            tmp_list_appt, _ = self.get_appt_from_url(self.url + self.page_suffix + str(page))
            list_appt += tmp_list_appt

        self.logger.info(f"Total appartement scrapped {len(list_appt)} appartements.")
        self.show_data(list_appt)


