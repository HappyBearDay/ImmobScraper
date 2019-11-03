from flask import render_template, request, Blueprint

import sys
import json
path_lib = "../lib"
sys.path.append(path_lib)

from VirtualScraper import headers
from scraper_leboncoin import *

main = Blueprint("main", __name__)


#Get Location, body, 
def preprocessing_leboncoin( df):
    return df[["location", "body", "images", "url", "subject", "index_date","expiration_date", "first_publication_date"]]



@main.route('/')
@main.route('/home')
@main.route('/leboncoin/<int:page>')
def home(page):
    print("home")
    url_leboncoin = f'https://www.leboncoin.fr/_immobilier_/offres/ile_de_france/p-{page}'
    #page_add_leboncoin = f'&page={page}' 
    scraper_1 = LebonCoin_Scraper(url_leboncoin, page_add_leboncoin)
    list_appt_1 = scraper_1.get_full_list_appt()
    
    df = pd.DataFrame(list_appt_1)
    df = preprocessing_leboncoin(df = df)
    
    return render_template("home.html",title="about", announces = json.loads(df.to_json(orient='records')) )