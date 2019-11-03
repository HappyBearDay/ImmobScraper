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


'''
GET /recherche/?category=10&locations=Paris_75011__48.85978_2.37813_2013,Paris_75003__48.86256_2.35905_1020&real_estate_type=1,2&price=min-1100 HTTP/1.1
Host: www.leboncoin.fr
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36 OPR/64.0.3417.47
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Sec-Fetch-Site: none
Referer: https://lobstr.io/index.php/2018/03/22/scraping-annonces-leboncoin-python-scrapy/
Accep0H2t-Encoding: gzip, deflate, br
Accept-Language: fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: oas_ab=a; xtvrn=$562498$; xtan562498=-undefined; xtant562498=1; euconsent=BOoOp4OOoOp4ODWAACFRCl-AAAAqVr_7__7-_9_-_f__9uj_Ov_v_f__30ecr59v_B_jv-_7fq_22jV4u_1vft9yfm1-7ctD3tp505iakivXmr__b9__3z3_9phP78k89r7337Ew-v-3o8A; consent_allpurpose=cDE9MTtwMj0xO3AzPTE7cDQ9MTtwNT0x; cookieBanner=1; shippableOnboarding=1; saveOnboarding=1; uuid=0befad56-6101-416d-9e60-35a159c791c2; _gcl_au=1.1.911866555.1570957717; cikneeto_uuid=id:a925e007-8e51-4417-b94b-c70056dd76dd; sq=ca=12_s; atidvisitor=%7B%22name%22%3A%22atidvisitor%22%2C%22val%22%3A%7B%22vrn%22%3A%22-562498-%22%2C%22an%22%3A%22NaN%22%2C%22ac%22%3A%220%22%7D%2C%22options%22%3A%7B%22path%22%3A%22%2F%22%2C%22session%22%3A15724800%2C%22end%22%3A15724800%7D%7D; cikneeto_lastad=idlast_ad_analysis:8251102&cookie_date:1571076737; _pulse2data=11f62b29-8d83-41d5-b70b-574141a2b163%2Cv%2C%2C1571683157815%2CeyJpc3N1ZWRBdCI6IjIwMTktMTAtMTBUMTg6MTc6MDhaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..ftolgBw-55waZ_mpBUh68w.2t0NSFPfwdOgK9XnHTukZLUpAZMiAyRz1cRyv6J9KhQe7IjZl-_nX8dEC6LZ8ArC40r8DmlOFC9-vmzI381GX12odBU7c4E2mGvOnRoBQVvnt52RLLgTNDUsAkVs1-gopIWnex2L6Lzz-uk-icq6Rafqya5dtq7a4hU-xTA0d3fQ9LrJfPvQq2H1IKzTx-t-7MjzO-zCEioXZMbocEWyjA.-0uwpYGnXJEYZl_YneqEhA%2C%2C0%2Ctrue%2C%2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..iqXpZZie31rV32D63VCULQrnZcIKfYkR5q_nclqYbdA; utag_main=v_id:016db6e37f040014388237be76750307a004007200bd0$_sn:11$_ss:0$_st:1571684071707$_pn:3%3Bexp-session$ses_id:1571682255257%3Bexp-session; cikneeto=date:1571682311433; datadome=Q8tJEYuXZRNAGWPm1QvYzH4zyXh.HJC81P00N6p-qCDi0bki~6Yr7aPkNEnvN.qSK.11aI4v_h2b2epPbaw3iqnJN-kaV8W2-jaki0Ct3P
'''

# User agent for not being a robot
headers = {
            # 'User-Agent': '*',
            #
            #'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36 OPR/64.0.3417.47',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'fr-FR,en;q=0.5',
           'Accept-Encoding': 'gzip, deflate',
           'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
           'Upgrade-Insecure-Requests': '1'}



logging.basicConfig(level=logging.CRITICAL, format='%(message)s')
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
        print("URL : : : ", url )
        r = s.get(url)
        if r.status_code == 200:
            self.logger.info("WebSite reached")
            return r
        else:
            logging.error(f"WebSite unreachable, response : {r.text}")
            return None

    def find_scripts_on_page(self, response):
        print("response" , response)
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
        #self.show_data(list_appt)
        return list_appt
